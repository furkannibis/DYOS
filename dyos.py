import os
from datetime import datetime
import argparse
import ipaddress
import sys
import ping3
import nmap
import socket
import requests
from bs4 import BeautifulSoup
import sqlite3

def askdb(version):
    conn = sqlite3.connect("DB/cve.db")
    curr = conn.cursor()

    curr.execute("SELECT * FROM cve WHERE cve_name LIKE '%'||:parameter||'%'", {"parameter": version})
    cve_list = curr.fetchall()
    for i in cve_list:
        print(f"[*] - VULN NAME: {i[1]}, VULN LINK: {i[2]}")
    curr.close()


def ask_to_rapit7(page_num, version):
    a = 1
    while True:
        URL = f"https://www.rapid7.com/db/?q={version}&type=nexpose&page={a}"
        r = requests.get(URL)

        soup = BeautifulSoup(r.content, 'lxml')

        vulns_name = soup.findAll("div", attrs={'class': 'resultblock__info-title'})
        vulns_link = soup.findAll("a", attrs={'class': 'vulndb__result resultblock'})

        if a == page_num + 1:
            break
        elif len(vulns_name) >= 1:
            a += 1
        elif len(vulns_name) <= 0:
            break

        for i, j in zip(vulns_name, vulns_link):
            print(f"[*] - VULN NAME: {i.text.strip()}, VULN LINK: https://www.rapid7.com/{j.get('href')}")




class Dyos:
    def __init__(self):
        self.banner()
        self.take_inp()

    def banner(self):
        os.system("clear")
        print("""
        ______  ______  _____
       / __ \ \/ / __ \/ ___/
      / / / /\  / / / /\__ \ 
     / /_/ / / / /_/ /___/ /    
    /_____/ /_/\____//____/     
    
    DYOS - Simple effective port scanner
                          
    """)

        print(f"[*] - DYOS started at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}.\n".upper())

    def take_inp(self):
        parser = argparse.ArgumentParser(description="DYOS is an enhanced port scanner.")

        parser.add_argument("--ip", help="Enter the IP information of the destination you want to scan.")
        parser.add_argument("--port", help="Enter the port information of the destination you want to scan.")
        parser.add_argument("--file", help="You can give the ip and port information related to the target or targets you want to process via a txt file. When you use this argument, you don't need to use the '--ip' and '--port' arguments.")
        parser.add_argument("--ping", help="Ping scan detects if your target is in an active state and presents it to you.", action="store_true")
        parser.add_argument("--tcpsyn", help="TCP SYN scan is a type of scan used to scan for open TCP ports available on a network.", action="store_true")
        parser.add_argument("--os", help="It is used to detect the operating system of the target system.", action="store_true")
        parser.add_argument("--showcve", help="DYOS can collect information from various sources on the web according to the version or application information it detects on the ports for you. This information contains relevant CVEs.")
        parser.add_argument("--askdb", help="DYOS stores CVEs obtained from various sources. Use this parameter to get a simple result without doing a web search.", action="store_true")

        self.args = parser.parse_args()

        if self.args.file != None and self.args.ip != None and self.args.port != None:
            print(
                "[WARNING] - You have already given a destination file path, you don't need to specify extra ip and port.")
            self.args.ip = None
            self.args.port = None

        if self.args.file == None:
            self.args.ip = self.ip_control()
            self.args.port = self.port_control()

        if self.args.file != None:
            self.split_file()

        if self.args.ping and self.args.port != None:
            print(
                "[WARNING] - You have given the port information, but I will not need the port information in the ping scan.")
            self.args.port = None

        if self.args.tcpsyn and self.args.port == None:
            print("[ERROR] - I need port information to scan TCP SYN")
            sys.exit(1)

        if not self.args.tcpsyn and self.args.showcve:
            print(
                "[ERROR] - I need to tcpsyn scan to list CVEs. You can use the --tcpsyn parameter to scan for TCP syn.")
            sys.exit(1)

        if self.args.ping:
            self.ping_scan()

        if self.args.tcpsyn:
            self.tcp_syn_scan()

    def ip_control(self):
        try:
            return [ipaddress.ip_address(self.args.ip).exploded]
        except ValueError:
            try:
                return [x.exploded for x in list(ipaddress.ip_network(self.args.ip))]
            except:
                if self.args.ip == None:
                    pass
                else:
                    print("[ERROR] - IP information not given correctly")
                    sys.exit(1)

    def port_control(self):
        if self.args.port != None:
            if "-" in self.args.port:
                start_point = int(self.args.port.split("-")[0])
                end_point = int(self.args.port.split("-")[1])
                return [x for x in range(start_point, end_point + 1)]

            elif "," in self.args.port:
                return [int(x) for x in self.args.port.split(",")]

            elif "," and "-" not in self.args.port:
                try:
                    return [int(self.args.port)]
                except:
                    print("[ERROR] - Port information is not given correctly")
                    sys.exit(1)

    def ping_scan(self):
        for ip in self.args.ip:
            sock = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
            sock.settimeout(1)
            try:
                sock.bind((ip, 80))
                print(f"[*] - {ip} is UP!")
            except socket.timeout:
                continue
            except Exception as e:
                continue

    def detect_os(self, ip):
        nm = nmap.PortScanner()
        nm.scan(ip, arguments='-O')
        return nm[ip]['osmatch'][0]['osclass'][0]['vendor'], nm[ip]['osmatch'][0]['osclass'][0]['osgen'], \
            nm[ip]['osmatch'][0]['osclass'][0]['cpe'][0]

    def tcp_syn_scan(self):
        for ip in self.args.ip:
            for port in self.args.port:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, port))
                except:
                    pass
                else:
                    port_state, service, version = self.nmap_scan(ip, str(port))
                    print("\n")
                    print(f"[*] - {ip}:{port} is {port_state} ({service}, version: {version})")
                    if self.args.showcve != None:
                        ask_to_rapit7(page_num=int(self.args.showcve), version=version)
                    if self.args.askdb:
                        if version != '':
                            askdb(version=version)
                finally:
                    s.close()
            if self.args.os:
                print(f"\n[*] - OS: {' '.join(self.detect_os(ip))}")

    def nmap_scan(self, ip, port):
        nm = nmap.PortScanner()
        nm.scan(ip, port)
        protocol = nm[ip].all_protocols()[0]
        port_state = nm[ip][protocol][int(port)]['state']
        service = nm[ip][protocol][int(port)]['name']
        version = nm[ip][protocol][int(port)]['product']
        return port_state, service, version

    def split_file(self):
        with open(self.args.file, "r", encoding="utf-8") as file:
            list_ = file.readlines()
        self.args.ip = list(set([x.split(":")[0] for x in list_]))
        self.args.port = [int(x.split(":")[1][:-1]) for x in list_]


scan = Dyos()
