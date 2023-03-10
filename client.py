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


# Define a function to handle DHCP responses
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

    while True:
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
            if response.status_code == 200:
                # Open a local file with wb (write binary) permission.
                with open("EndGame.jpg", "wb") as file:
                    # Write the contents of the response to the file.
                    file.write(response.content)
                    print("Image downloaded successfully.")
                    img = Image.open('/home/matan/PycharmProjects/RN_FinalProject/EndGame.jpg')
                    img.show()
            else:
                print(f"Failed to download image. HTTP status code: {response.status_code}")



            # with open("EndGame.jpg", "wb") as file:
            #     # Write the contents of the response to the file.
            #     file.write(response)
            #     print("Image downloaded successfully.")
            #     img = Image.open('/home/matan/PycharmProjects/RN_Final_Project/EndGame.jpg')
            #     img.show()

        if input_choice == "2":

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
                with open("InfinityWar.jpg", "wb") as file:
                    # Write the contents of the response to the file.
                    file.write(response.content)
                    print("Image downloaded successfully.")
                    img = Image.open('/home/matan/PycharmProjects/RN_FinalProject/InfinityWar.jpg')
                    img.show()
            else:
                print(f"Failed to download image. HTTP status code: {response.status_code}")

        if input_choice == "3":

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
                with open("Ultron.jpg", "wb") as file:
                    # Write the contents of the response to the file.
                    file.write(response.content)
                    print("Image downloaded successfully.")
                    img = Image.open('/home/matan/PycharmProjects/RN_FinalProject/Ultron.jpg')
                    img.show()
            else:
                print(f"Failed to download image. HTTP status code: {response.status_code}")


        decide_input = input("do you want to keep going or to exit? for exit write e , for keep going write k: ")

        while decide_input != "e" and decide_input != "k":
            decide_input = input("do you want to keep going or to exit? for exit write e , for keep going write k: ")
            if decide_input == "e" or decide_input == "k":
                break

        if decide_input == "e":
            print("Client decide to exit")
            break
        if decide_input == "k":
            print("APP what else do you want to get? remember to pick between 1-3: ")
            continue

    tcp_client_socket.close()


def authentication_check(sock):

    # checking if the request that we sent got fully to the server
    Authentication_Check = 1111010

    check_from_server = sock.recvfrom(4096)

    if check_from_server == Authentication_Check:
        print("the request Got to the server Successfully")
        return 1
    else:
        print("The request didn't Got fully to the server")
        return 0




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

    client_socket.sendto(mod_choice.encode("utf-8"), (app_address, app_port))
    print("Sent to the Application the request")

    # segemnts is a dictionery because we don't know the order that the segments received in the application
    segments = {}

    # -1 is like infinty we do it because we don't know how much segments will receive
    last_segment = -1

    while last_segment == -1 or len(segments) <= last_segment:
        try:
            segment_packet = client_socket.recvfrom(4096)[0]
            segment_packet = segment_packet.decode()
        except socket.error:
            continue

        tag, seq_num_as_str, segment = segment_packet.split(',', 3)
        seq_num = int(seq_num_as_str)

        ack_packet = str(seq_num)

        client_socket.sendto(ack_packet.encode(), (app_address, app_port))

        if seq_num not in segments:
            segments[seq_num] = segment
            print("Get segment number " + str(seq_num))

        if tag == "E":
            last_segment = seq_num

    data = ""
    for i in range(last_segment + 1):
        data += segments[i]

    print(data)


    # segment_size = 5
    # byte_send = 0
    # segment_count = len(mod_choice)
    #
    # if segment_count%segment_size == 0:
    #     segment_count = int(segment_count / segment_size)
    # else:
    #     segment_count = int(segment_count/segment_size)+1
    #
    # while seq_number < segment_count:
    #
    #     # request contain the model that the client selected and the seq number of the packet
    #     request = str(window_size) + ',' + str(seq_number) + ',' + mod_choice[segment_size*seq_number:segment_size*(seq_number+1)]
    #
    #     client_socket.sendto(request.encode("utf-8"), (server_address, server_port))
    #     print("Sent to the Application the request")
    #
    #     checking_ack = client_socket.recvfrom(4096)
    #
    #     client_socket.settimeout(10)
    #     try:
    #         if checking_ack == "ACK":
    #             print("Got ACK!")
    #             seq_number += 1
    #         else:
    #             print("Got NACK")
    #             client_socket.sendto(request, (server_address, server_port))
    #             print("Sent the request again")
    #     except socket.timeout:
    #         print("timeout")



    # # AuthenticationCheck
    # authentication= authentication_check(client_socket)
    # if authentication == 0:

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




def udp_app_client():

     # Configure the server address and port number
    server_address = '127.0.0.1'
    server_port = 20529

    # Create a UDP socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Send a request to the server
    request = 'Please redirect me to the remote server'.encode()
    client_socket.sendto(request, (server_address, server_port))

    # Receive the redirect response from the server
    redirect_response, server_address = client_socket.recvfrom(1024)

    print('Received redirect response from server at {}:{}'.format(server_address[0], server_address[1]))

    # Parse the IP address and port number of the remote server from the redirect response
    remote_server_address, remote_server_port = redirect_response.decode().split(':')

    print('Connecting to remote server at {}:{}'.format(remote_server_address, remote_server_port))

    # Connect to the remote server and download the file
    remote_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    remote_server_socket.connect((remote_server_address, int(remote_server_port)))
    remote_server_socket.sendall('Please send me the file'.encode())

    with open('file.txt', 'wb') as f:
        while True:
            data = remote_server_socket.recv(1024)
            if not data:
                break
            f.write(data)

    print('File downloaded from remote server')


# main
if __name__ == "__main__":
    #dhcp_discover()
    #got_dhcp_offer()
    #got_dhcp_ack()

    #dns_socket()

    #tcp_app_client()

    udp_client()

    #udp_app_client()
