# Port-Scanner
· A high-level, simple designed port scanning, service detection tool developed with Python programming language.

· It detects port activity and version information of the application running on the port and this application by using various network packets.

· A high-level, simple designed port scanning, service detection tool developed with Python programming language.

· As a result of the research it has done on the internet with the application version information it has determined, it presents the possible weakness, the reason and how it can be solved to the user. (Still in design phase)

· There are two operating modes. PING Scan and TCP scan.

General use: python reds.py -i "target ip, ip block" -p "target port, port range" action
python reds.py -i 192.168.70.0/24 -p 1-1000 --tcpsyn

PING SC4N
A ping scan can be done with the "--ping" parameter. In this way, you can detect whether the host is active or not.

TCP SC4N
With the "--tcpsyn" parameter, you can perform operations according to the version information of the applications running on the active ports on the client that you have determined to be active...
