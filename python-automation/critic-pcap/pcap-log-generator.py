# pcap-log-generator.py
# Gera demo.pcap totalmente compatível c/ Wireshark e Scapy (Ethernet + IP + TCP/UDP)

from scapy.all import Ether, IP, TCP, UDP, DNS, DNSQR, Raw, wrpcap

pkts = []

def tcp(src, dst, sport, dport, payload):
    return Ether()/IP(src=src, dst=dst)/TCP(sport=sport, dport=dport)/Raw(load=payload)

def udp(src, dst, sport, dport, payload):
    return Ether()/IP(src=src, dst=dst)/UDP(sport=sport, dport=dport)/payload

# 1) HTTP Basic Auth
http_req = (
    b"GET /private HTTP/1.1\r\n"
    b"Host: example.com\r\n"
    b"Authorization: Basic dXNlcjpwYXNzd29yZA==\r\n\r\n"
)
pkts.append(tcp("192.168.1.10","93.184.216.34",50100,80,http_req))

# 2) HTTP POST com senha
http_post = (
    b"POST /login HTTP/1.1\r\nHost: insecure.local\r\n\r\n"
    b"username=alice&password=Summer2026!"
)
pkts.append(tcp("192.168.1.10","198.51.100.20",50102,80,http_post))

# 3) FTP USER/PASS
pkts.append(tcp("192.168.1.10","203.0.113.77",50110,21,b"USER demo\r\n"))
pkts.append(tcp("192.168.1.10","203.0.113.77",50110,21,b"PASS demo123\r\n"))

# 4) Telnet
pkts.append(tcp("192.168.1.10","203.0.113.55",50120,23,b"login: bob\r\nPassword: qwerty\r\n"))

# 5) DNS longo
long_name = ("a"*30 + "." + "b"*30 + "." + "c"*30 + ".example.com")
dns_query = DNS(rd=1, qd=DNSQR(qname=long_name))
pkts.append(udp("192.168.1.10","8.8.8.8",53000,53,dns_query))

# 6) POP3 sem TLS
pkts.append(tcp("192.168.1.10","203.0.113.88",50130,110,b"USER carol\r\nPASS 123456\r\n"))

# Salvar
wrpcap("demo.pcap", pkts)
print("demo.pcap gerado com", len(pkts), "pacotes!")