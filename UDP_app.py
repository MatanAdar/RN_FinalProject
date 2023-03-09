import socket

PORT = 20529
SERVER_ADDRESS = "127.0.0.1"


def udp_server():

    udp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    udp_server_socket.bind((SERVER_ADDRESS, PORT))

    # open a connection to the second server that have the object
    second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        request_from_client, client_addr = udp_server_socket.recvfrom(4096)
        print(f"connected to server {client_addr}")

        print(request_from_client)

        request = request_from_client.decode("utf-8")
        print(request)

        print("Received the request from the client")

        print("The model phone that the client choice is:", request)

        print("I dont have what you want but i know the server that have this")
        print("I will connect to this server")

        # Sending the request to the second server
        second_server_socket.sendto(request.encode("utf-8"), ("127.0.0.1", 30553))
        print("Sent the request to the second server")

        response = second_server_socket.recvfrom(4096)
        response = response[0]
        print("Got the response from the second Server")

        udp_server_socket.sendto(response, client_addr)
        print("Sent the response to the Client")

        break

    # Closing sockets
    second_server_socket.close()
    udp_server_socket.close()


if __name__ == "__main__":
    udp_server()
