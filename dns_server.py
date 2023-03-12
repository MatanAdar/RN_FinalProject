from scapy.all import *
import time
from scapy.layers.dns import DNSQR, DNS, DNSRR
from scapy.layers.inet import UDP, IP
import threading
import socket

global cache_of_domains
cache_of_domains = {}
lock = threading.Lock()

def handle_dns_query(query, client_addr):
    domain = query.decode("utf-8")

    print("Checking if the domain in the cache:")
    with lock:
        if domain not in cache_of_domains:
            try:
                print("The domain is NOT in the cache")
                # get the info of the domain from the DNS server
                info = socket.getaddrinfo(domain, 53, socket.AF_INET, socket.SOCK_DGRAM)

                # found the ip in the touple
                ip_address = info[0][4][0]

                ip_address_to_send = ip_address.encode("utf-8")

                # sending the ip to the client
                dns_server_socket.sendto(ip_address_to_send, client_addr)
                print("found the ip address from the DNS")

                # We added to the cache the domain
                cache_of_domains[domain] = ip_address
                print("The domain added to the cache successfully")

                print(cache_of_domains)

                print("\n")
            except socket.error as e:
                print("The error is: %s" % e)
                print("there is no ip for this domain! the domain not found in DNS server")
                print("\n")
        else:
            print("The domain is in the cache")
            ip_address = cache_of_domains[domain].encode("utf-8")
            dns_server_socket.sendto(ip_address, client_addr)
            print("send the ip_address:", ip_address.decode("utf-8"), "to the client")
            print("\n")

def dns_server2():
    global dns_server_socket
    dns_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # making that the addr will not say "the addr is already in use"
    dns_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    dns_server_socket.bind(("127.0.0.1", 53))

    while True:
        query, client_addr = dns_server_socket.recvfrom(4096)
        threading.Thread(target=handle_dns_query, args=(query, client_addr)).start()

if __name__ == "__main__":
    dns_server2()
