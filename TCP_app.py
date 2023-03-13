import socket


def tcp_app():

    # ************************************************************************************************

    # 1
    # creating TCP sockets

    port = 20530
    server_address = "127.0.0.1"

    tcp_app_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # making that the addr will not say "the addr is already in use"
    tcp_app_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    tcp_app_socket.bind((server_address, port))

    tcp_app_socket.listen(5)

    # open a connection to the second server that have the object
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    server_socket.bind(("127.0.0.1", 30555))

    server_socket.connect(("127.0.0.1", 30553))

    while True:
        connection_socket, addr = tcp_app_socket.accept()
        print(f"connected to server {addr}")

        # *****************************************************************************************************

        # 2
        # receiving from client the request and sending this request to the server

        request = connection_socket.recv(4096).decode("utf-8")

        print("Received the request from the client")

        print("Got number:", request)

        print("I dont have what you want but i know the server that have this")
        print("i will connect to this server")

        # Sending the request to the second server
        server_socket.send(request.encode("utf-8"))
        print("Sent the request to the second server")

        # *****************************************************************************************************

        # 3
        # receiving the response from the server and sending this response to the client

        response = server_socket.recv(4096)
        print("Got the response from the second Server")

        connection_socket.send(response)
        print("Sent the response to the Client")

        # *****************************************************************************************************

    # 4
    # closing sockets (the only why the server will close if we manually close them in terminal with ctrl+c)
    server_socket.close()
    connection_socket.close()
    tcp_server_socket.close()


# main
if __name__ == "__main__":
    tcp_app()
