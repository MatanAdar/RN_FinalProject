from scapy.all import *
import time
import  random

from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether

global dhcp_ip, end_ip, ips_in_used, find_unused_ip_for_client, offer_client_ip
dhcp_ip = "10.0.0.1"
end_ip= 0
ips_in_used=["10.0.2.15"]


# Define a function to handle DHCP requests
def got_dhcp_discover():

    global end_ip, find_unused_ip_for_client, ips_in_used

    pkt = sniff(filter="udp and port 67", count=1, iface="enp0s3")[0]

    if DHCP in pkt and pkt[DHCP].options[0][1] == 1:
        print("DHCP Discover received")

        # checking if the ip is in use already or if there is no more ips available
        find_unused_ip_for_client = "10.0.2."+str(end_ip)  # check if to change this to a diffrent way(maybe with random)???
        while find_unused_ip_for_client in ips_in_used:
            # the list that the server have to keep up what ips is in use (ips_in_used)
            print("the ip:", find_unused_ip_for_client, "in use already")
            end_ip += 1
            if end_ip == 255:
                print("we cant make anymore ip's")
                end_ip = 0
                find_unused_ip_for_client = "0.0.0.0"  # if there is no more available ips with the 10.0.5. we make the client ip back to 0.0.0.0
                break
            find_unused_ip_for_client = "10.0.2."+str(end_ip)  # update the client ip with +1 in the end_ip to check if it not in the ips

        # after we found an unused ip to give to the client
        global offer_client_ip
        offer_client_ip = find_unused_ip_for_client

        # Craft DHCP Offer and offer the client ip to the client that the server find
        dhcp_offer1 = Ether(dst="ff:ff:ff:ff:ff:ff", src="4a:e4:66:e8:7a:00") / \
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
        dhcp_ack1 = Ether(dst="ff:ff:ff:ff:ff:ff", src="4a:e4:66:e8:7a:00") / \
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
