from scapy.all import *
import time
import  random

from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

global dhcp_ip, END_IP, ips_in_used, offer_client_ip
dhcp_ip = "10.0.0.1"
END_IP = 0
ips_in_used = ["10.0.2.15"]


# checking if the ip is already in used or if there is no more ips available
def get_unused_ip():
    """
    Returns an unused IP address for a client to use.
    """
    #End_IP - find what number in the end of the ip can we append to the start of that ip that unused already
    # ips_in_used - array of all the ips that already in used
    global END_IP, ips_in_used

    # Check if there are any more IPs available to use
    # if there is no more ips to use we make the ip to "0.0.0.0"
    if END_IP == 255:
        print("Cant make more ips")
        return "0.0.0.0"

    # Find an unused IP address
    while True:
        ip = f"10.0.2.{END_IP}"
        if ip not in ips_in_used:
            END_IP += 1
            print(f"Found that ip {ip} is not in use")
            print(f"Offering the client this ip: {ip}")
            return ip
        else:
            print("the ip:", ip, "in use already")
            END_IP += 1


# Define a function to handle DHCP requests
def got_dhcp_discover():

    global END_IP, ips_in_used

    pkt = sniff(filter="udp and port 67", count=1, iface="enp0s3")[0]

    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:
        print("DHCP Discover received")

        # we found an unused ip to give to the client in the help func 'get_unused_ip()'
        global offer_client_ip
        offer_client_ip = get_unused_ip()

        # Craft DHCP Offer and offer the client ip to the client that the server find
        dhcp_offer1 = Ether(dst="ff:ff:ff:ff:ff:ff", src=get_if_hwaddr("enp0s3")) / \
                      IP(src="0.0.0.0", dst="255.255.255.255") / \
                      UDP(sport=67, dport=68) / \
                      BOOTP(op=2, yiaddr=offer_client_ip, siaddr="10.0.0.1", giaddr="0.0.0.0", chaddr=pkt[Ether].src, xid=pkt[BOOTP].xid) / \
                      DHCP(options=[("message-type", "offer"),
                                    ("subnet_mask", "255.255.255.0"),
                                    ("router", "10.0.0.1"),
                                    ("name_server", "10.0.0.1"),
                                    "end"])

        time.sleep(1)

        print("sending dhcp offer to client")
        # Send DHCP Offer to the client
        sendp(dhcp_offer1)


def dhcp_ack():

    pkt = sniff(filter="udp and port 67", count=1, iface="enp0s3")[0]

    if DHCP in pkt and pkt[DHCP].options[0][1] == 3:
        print("DHCP Request received")

        print("yes. you can lease this ip address:", offer_client_ip)

        print("adding this ip to the list of used ip:")

        # adding to the array the ip address that the client will use
        ips_in_used.append(offer_client_ip)

        # Craft DHCP Ack
        dhcp_ack1 = Ether(dst="ff:ff:ff:ff:ff:ff", src=get_if_hwaddr("enp0s3")) / \
                    IP(src="0.0.0.0", dst="255.255.255.255") / \
                    UDP(sport=67, dport=68) / \
                    BOOTP(op=2, yiaddr=pkt[BOOTP].yiaddr, siaddr="10.0.0.1", giaddr="0.0.0.0",
                          chaddr=pkt[Ether].src, xid=pkt[BOOTP].xid) / \
                    DHCP(options=[("message-type", "ack"),
                                  ("subnet_mask", "255.255.255.0"),
                                  ("router", "10.0.0.1"),
                                  ("name_server", "10.0.0.1"),
                                  "end"])

        time.sleep(1)

        print("sending dhcp ack to the client")
        # Send DHCP Ack to the client
        sendp(dhcp_ack1)


# main
if __name__ == "__main__":

    while True:
        got_dhcp_discover()
        dhcp_ack()
