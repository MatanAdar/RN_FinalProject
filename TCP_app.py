import socket

PORT = 80
SERVER_ADDRESS = "127.0.0.1"


def tcp_server():

    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    tcp_server_socket.bind((SERVER_ADDRESS, PORT))

    tcp_server_socket.listen(5)

    # open a connection to the second server that have the object
    second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    second_server_socket.connect(("127.0.0.1", 30553))

    while True:
        connection_socket, addr = tcp_server_socket.accept()
        print(f"connected to server {addr}")

        request = connection_socket.recv(4096).decode("utf-8")

        print("Received the request from the client")

        print("Got number:", request)

        print("I dont have what you want but i know the server that have this")
        print("i will connect to this server")

        # Sending the request to the second server
        second_server_socket.send(request.encode("utf-8"))
        print("Sent the request to the second server")

        response = second_server_socket.recv(4096)
        print("Got the response from the second Server")

        connection_socket.send(response)
        print("Sent the response to the Client")

        break

    # Closing sockets
    second_server_socket.close()
    connection_socket.close()
    tcp_server_socket.close()


if __name__ == "__main__":
    tcp_server()
