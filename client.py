from scapy.all import *
import time
import socket
from scapy.layers.dhcp import DHCP, BOOTP
from scapy.layers.dns import DNSRR, DNS, DNSQR
from scapy.layers.inet import UDP, IP
from scapy.layers.l2 import Ether
from scapy.sendrecv import sendp
import requests
from PIL import Image


global client_ip_from_server


def dhcp_discover():

    dhcp_discover1 = Ether(dst="ff:ff:ff:ff:ff") / \
                    IP(src='0.0.0.0', dst='255.255.255.255') / \
                    UDP(sport=68, dport=67) / \
                    BOOTP(op=1, chaddr="4a:e4:66:e8:7a:00", xid=23567342) / \
                    DHCP(options=[("message-type", "discover"), "end"])

    # send DHCP discover to the server
    sendp(dhcp_discover1)


# Function to handle DHCP responses
def got_dhcp_offer():

    global client_ip_from_server

    pkt = sniff(filter="udp and port 68", count=1, iface="enp0s3")[0]

    if DHCP in pkt and pkt[DHCP].options[0][1] == 2:
        print("DHCP Offer received")

        client_ip_from_server = pkt[BOOTP].yiaddr

        if client_ip_from_server == "0.0.0.0":
            print("there is no more available ips from the server")
            return

        print("the client_ip that the server offer is:", client_ip_from_server)

        print("ok, i want this ip address:", client_ip_from_server, "can i lease it?")

        # Craft DHCP Request
        dhcp_request = Ether(dst="ff:ff:ff:ff:ff:ff") / \
                       IP(src="0.0.0.0", dst="255.255.255.255") / \
                       UDP(sport=68, dport=67) / \
                       BOOTP(op=1, chaddr="4a:e4:66:e8:7a:00", xid=pkt[BOOTP].xid) / \
                       DHCP(options=[("message-type", "request"),
                                     ("requested_addr", pkt[BOOTP].yiaddr),
                                     ("server_id", pkt[IP].src),
                                     "end"])

        time.sleep(1)
        print("sending dhcp request to the server")
        # Send DHCP Request to the server
        sendp(dhcp_request)


def got_dhcp_ack():

    pkt = sniff(filter="udp and port 68", count=1, iface="enp0s3")[0]  #got the pkt in the spot 0

    if DHCP in pkt and pkt[DHCP].options[0][1] == 5:
        print("DHCP ack received")

        print("so my ip address is:", client_ip_from_server)


def dns_socket():

    dns_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    input_domain = input("DNS please input a domain:")

    dns_sock.sendto(input_domain.encode("utf-8"), ("127.0.0.1", 53))

    ip_address = dns_sock.recvfrom(4096)

    print("the ip of the address is:", ip_address[0].decode("utf-8"))  #because the ip_address we get from the server its a tuple

    dns_sock.close()



def tcp_app_client():

    tcp_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_client_socket.connect(("127.0.0.1", 80))  #the 529 in the port is the last 3 digit of the id

    # We are creating a request to the server to give us a link to the oceans song
    request = "I want a picture".encode("utf-8")

    print("The choices of movies are:")
    print("For Avengers-Endgame write 1")
    print("For Avengers-InfinityWar write 2")
    print("For Avengers-FirstAvenger write 3")

    input_choice = input("APP which poster movie do you want? pick 1 to 3! ")

    # Sending the request to the app_server
    tcp_client_socket.send(input_choice.encode("utf-8"))
    print("sent the request to the app_server")

    url_response_server = tcp_client_socket.recv(4096).decode("utf-8")
    print(url_response_server)
    print("Got the response from the app_server")

    if input_choice == "1":
        # Send an HTTP request to the URL and get the response object
        response = requests.get(url_response_server, allow_redirects=True)

        print(f"The status code is: {response.status_code}")

        # check if the image have been moved temporality to a diffrent URL
        if response.status_code == 302:
            new_url = response.headers['Location']
            response = requests.get(new_url)

        # Check if the request was successful (HTTP status code 200)
        elif response.status_code == 200:
            # Open a local file with wb (write binary) permission.
            with open("EndGame.jpg", "wb") as file:
                # Write the contents of the response to the file.
                file.write(response.content)
                print("Image downloaded successfully.")
                img = Image.open('EndGame.jpg')
                img.show()
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")

    elif input_choice == "2":

        # Send an HTTP request to the URL and get the response object
        response = requests.get(url_response_server, allow_redirects=True)

        print(f"The status code is: {response.status_code}")

        # check if the image have been moved temporality to a diffrent URL
        if response.status_code == 302:
            new_url = response.headers['Location']
            response = requests.get(new_url)

        # Check if the request was successful (HTTP status code 200)
        elif response.status_code == 200:
            # Open a local file with wb (write binary) permission.
            with open("InfinityWar.jpg", "wb") as file:
                # Write the contents of the response to the file.
                file.write(response.content)
                print("Image downloaded successfully.")
                img = Image.open('InfinityWar.jpg')
                img.show()
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")

    elif input_choice == "3":

        # Send an HTTP request to the URL and get the response object
        response = requests.get(url_response_server, allow_redirects=True)

        print(f"The status code is: {response.status_code}")

        # check if the image have been moved temporality to a diffrent URL
        if response.status_code == 302:
            new_url = response.headers['Location']
            response = requests.get(new_url)

        # Check if the request was successful (HTTP status code 200)
        elif response.status_code == 200:
            # Open a local file with wb (write binary) permission.
            with open("Ultron.jpg", "wb") as file:
                # Write the contents of the response to the file.
                file.write(response.content)
                print("Image downloaded successfully.")
                img = Image.open('Ultron.jpg')
                img.show()
        else:
            print(f"Failed to download image. HTTP status code: {response.status_code}")

    tcp_client_socket.close()


def udp_client():

    # Configure the server address and port number
    app_address = '127.0.0.1'
    app_port = 20529

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    client_socket.bind(("127.0.0.1", 20530))
    client_socket.setblocking(True)
    client_socket.settimeout(5)

    print("hello! which phone do you want to get:")
    input_choice = input("Iphone or Android? ")

    if input_choice == "Iphone":
        mod_choice = input("which model do you like? Iphone 14 or Iphone 13?")

    if input_choice == "Android":
        mod_choice = input("which model do you like? Galaxy S23 or Galaxy S22? ")

    # Send
    while True:
        try:
            client_socket.sendto(mod_choice.encode("utf-8"), (app_address, app_port))
            print("Sent to the Application the request")
            break
        except socket.timeout:
            continue


    # getting the response from the app if he got the request
    while True:
        try:
            check_ack, app_addr = client_socket.recvfrom(4096)
            check_ack = check_ack.decode("utf-8")
        except socket.timeout:
            continue
        break

    # checking what ack we received
    while True:
        if check_ack != "ACK":
            print("Application didnt recv the request")
            try:
                client_socket.sendto(mod_choice.encode("utf-8"), (app_address, app_port))
                print("Sent the request again!")
            except socket.timeout:
                continue
        else:
            print("Application got the request!")
            send_ack_to_app = "ACK"
            try:
                client_socket.sendto(send_ack_to_app.encode("utf-8"), (app_address, app_port))
                print("Sent Ack to Application that we recv that ACK from him")
            except socket.timeout:
                continue
            break


    # segemnts is a dictionery because we don't know the order that the segments received in the application
    segments = {}

    # -1 is like infinty we do it because we don't know how much segments will receive
    last_segment = -1

    # getting segments from app when we don't know how much segments we need to get (last_segment didn't change)
    while last_segment == -1:
        try:
            segment_packet = client_socket.recvfrom(4096)[0]
            segment_packet = segment_packet.decode()
        except socket.error:
            continue

        letter, seq_num_from_app, segment_data = segment_packet.split(',', 3)
        seq_num = int(seq_num_from_app)

        ack_packet_seq_num = str(seq_num)

        client_socket.sendto(ack_packet_seq_num.encode(), (app_address, app_port))

        if seq_num not in segments:
            segments[seq_num] = segment_data
            print("Get segment number " + str(seq_num))

        if letter == "E":
            last_segment = seq_num

    # while to get all the packet after we got the last packet, and we know how much packet we need to get
    while len(segments) <= last_segment:
        try:
            segment_packet = client_socket.recvfrom(4096)[0]
            segment_packet = segment_packet.decode()
        except socket.error:
            continue

        letter, seq_num_from_app, segment_data = segment_packet.split(',', 3)
        seq_num = int(seq_num_from_app)

        ack_packet_seq_num = str(seq_num)

        client_socket.sendto(ack_packet_seq_num.encode(), (app_address, app_port))

        if seq_num not in segments:
            segments[seq_num] = segment_data
            print("Get segment number " + str(seq_num))

    # assemble the full data that we received from the app
    data = ""
    for i in range(last_segment + 1):
        data += segments[i]

    print(data)

    url_response_server = data

    # Send an HTTP request to the URL and get the response object
    response = requests.get(url_response_server, allow_redirects=True)

    print(f"The status code is: {response.status_code}")

    # check if the image have been moved temporality to a diffrent URL
    if response.status_code == 302:
        new_url = response.headers['Location']
        response = requests.get(new_url)

    # Check if the request was successful (HTTP status code 200)
    if response.status_code == 200:
        # Open a local file with wb (write binary) permission.
        with open("Image.jpg", "wb") as file:
            # Write the contents of the response to the file.
            file.write(response.content)
            print("Image downloaded successfully.")
            img = Image.open('Image.jpg')
            img.show()
    else:
        print(f"Failed to download image. HTTP status code: {response.status_code}")


# main
if __name__ == "__main__":
    #dhcp_discover()
    #got_dhcp_offer()
    #got_dhcp_ack()

    #dns_socket()

    #tcp_app_client()

    udp_client()

