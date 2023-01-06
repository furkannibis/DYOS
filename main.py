import optparse
import ipaddress
import socket
import logging
import nmap 
import exploitdb
from bs4 import BeautifulSoup
import requests

logging.getLogger("scapy.runtime").setLevel(logging.ERROR)

class PortScanner:
    def __init__(self):
        self.take_arguments()
        self.ip_list, self.port_list = self.input_processing()
        
        if self.option.ping:
            self.ping_scan()
        if self.option.tcpsyn:
            self.tcp_syn_scan()

    def get_exploit_db_url(self, port, version):
        links = []
        search_url = f"https://www.exploit-db.com/search?cve={version}"
        search_results = requests.get(search_url)
        search_results.raise_for_status()
        soup = BeautifulSoup(search_results.text, 'html.parser')
        for result in soup.find_all('a', class_='title'):
            if result.text.lower().find(f"port {port}") != -1:
                links.append(f"https://www.exploit-db.com{result['href']}")
        return links

    def check_vulnerability(self, port, version):
        edb = exploitdb.ExploitDB()
        result = edb.search(f"{port} {version}")
        if result:
            self.get_exploit_db_url(port, version)
            return "Bir zafiyet bulundu!"
        else:
            return "Bir zafiyet bulunamadı."

    def take_arguments(self):
        parser = optparse.OptionParser()
        parser.add_option('-i', '--ip', help='Targets IP address.', dest='ip', default='', type='str')
        parser.add_option('-p', '--port', dest='port', help='Targets port.', default='80', type='str')
        parser.add_option('-f', '--ff', dest='file', help='Target from txt file.', default='', type='str')
        parser.add_option('--ping', dest='ping', help='Use this for make PING scan.', default=False, action='store_true')
        parser.add_option('--tcpsyn', dest='tcpsyn', help='Use this for make TCP SYN scan.', default=False, action='store_true')
        self.option, self.addr = parser.parse_args()

    def input_processing(self):
        if self.option.file:
            with open(self.option.file, 'r', encoding='utf-8') as f:
                ip_list = [x.replace('\n','').split(':')[0] for x in f.readlines()]
            with open(self.option.file, 'r', encoding='utf-8') as f:
                port_list = [x.replace('\n','').split(':')[1] for x in f.readlines()]
        else:
            try:
                ipaddress.ip_address(self.option.ip)
                ip_list = [self.option.ip]
            except:
                ip_list = [str(x) for x in ipaddress.ip_network(self.option.ip)]
            if ',' in self.option.port:
                port_list = [int(x) for x in self.option.port.split(',')]
            elif '-' in self.option.port:
                start_point, end_point = self.option.port.split('-')
                port_list = [int(x) for x in range(int(start_point), int(end_point)+1)]
            else:
                port_list = [int(self.option.port)]
        return ip_list, port_list

    def nmap_scan(self, ip, port):
        nm = nmap.PortScanner()
        nm.scan(ip, port)
        protocol = nm[ip].all_protocols()[0]
        port_state = nm[ip][protocol][int(port)]['state']
        service = nm[ip][protocol][int(port)]['name']
        version = nm[ip][protocol][int(port)]['product']
        return port_state, service, version

    def ping_scan(self):
        for ip in self.ip_list:
            try:
                response = sr1(IP(dst=ip)/ICMP(), timeout=1, verbose=False)
                print(f"{ip} is alive")
            except:
                print(f"{ip} is not alive")

    def tcp_syn_scan(self):
        for ip in self.ip_list:
            for port in self.port_list:
                try:
                    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    s.connect((ip, port))
                except:
                    print(f"{ip}:{port} is closed")
                else:
                    print(f"{ip}:{port} is open")
                    port_state, service, version = self.nmap_scan(ip, port)
                    print(f"{ip}:{port} is {port_state} ({service}, version: {version})")
                    self.check_vulnerability(port,version)
                finally:
                    s.close()
print("""
 ___    ___
( _<    >_ )
//        \\
\\___..___//
 `-(    )-'
   _|__|_
  /_|__|_\
  /_|__|_\
  /_\__/_\
   \ || /  _)
     ||   ( )
ERK  \\___//
      `---'

""")
scanner = PortScanner()