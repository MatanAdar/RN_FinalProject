import socket
from scapy.layers.dns import DNS, DNSQR, DNSRR
from scapy.layers.inet import IP, UDP

# Function that replies to DNS query

# Import scapy libraries
from scapy.all import *
from scapy.layers.l2 import Ether



# Set the interface to listen and respond on
net_interface = "lo"

# Packet Filter for sniffing specific DNS packet only
packet_filter = "udp port 53"       # Filter UDP port 53

# Function that replies to DNS query
# Create a collection to serve as the cache
dns_cache = {}

def dns_reply(packet):

    # Get the domain name from the DNS query
    domain_name = packet[DNSQR].qname.decode('utf-8')

    print(domain_name)

    # Check if the domain name is in the cache
    if domain_name in dns_cache:
        print('domain is in cache')
        ip_address = dns_cache[domain_name]
    else:
        # Perform a DNS lookup for the domain name
        dns_res = sr1(IP(dst='8.8.8.8')/UDP()/DNS(rd=1, qd=DNSQR(qname=domain_name)), verbose=0)

        # Extract the IP address from the DNS response
        ip_address = dns_res[DNSRR].rdata

        # Add the IP address to the cache
        dns_cache[domain_name] = ip_address
        print('add domain to cache')

    print(str(dns_cache))
    # Construct the DNS response
    dns_response = DNS(
        id=packet[DNS].id,
        qr=1,  # Response
        aa=1,  # Authoritative Answer
        ancount=1,  # One Answer
        qd=packet[DNS].qd,
        an=DNSRR(rrname=domain_name, type='A', rclass='IN', ttl=600, rdata=ip_address)
    )

    # Construct the UDP packet
    udp_packet = UDP(
        sport=packet[UDP].dport,  dport=packet[UDP].sport )

    # Construct the IP packet
    ip_packet = IP(
        dst=packet[IP].src, src=packet[IP].dst )

    # Construct the Ethernet packet
    ether_packet = Ether(
        dst=packet[Ether].src,  src=packet[Ether].dst)

    # Put the packets together
    response_packet = ether_packet / ip_packet / udp_packet / dns_response

    # Send the DNS response
    sendp(response_packet, iface=net_interface)
    print('sent ip '+str(ip_address))


if __name__ == "__main__":
    while True:
        sniff(filter=packet_filter, prn=dns_reply, store=0, iface=net_interface, count=1)
