import socket

PORT = 20529
APP_ADDRESS = "127.0.0.1"


def udp_server():

    udp_app_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_app_socket.bind((APP_ADDRESS, PORT))

    udp_app_socket.setblocking(True)
    udp_app_socket.settimeout(5)

    # open a connection to the second server that have the object
    img_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    while True:
        try:
            request_from_client, client_addr = udp_app_socket.recvfrom(4096)
            print(f"connected to server {client_addr}")
            break
        except socket.error:
            print("error")
            pass

    print("The model phone that the client choice is:", request_from_client)

    print("I dont have what you want but i know the server that have this")
    print("I will connect to this server")

    # Sending the request to the second server
    img_server_socket.sendto(request_from_client, ("127.0.0.1", 30553))
    print("Sent the request to the second server")

    response_from_server = img_server_socket.recvfrom(4096)
    url_response = response_from_server[0]
    print("Got the response from the second Server")

    # CC algo reno
    data = url_response.decode()

    # the code start now

    segment_size = 5

    dataLen = len(data)

    segments_count = int(dataLen / segment_size)
    if segments_count * segment_size < dataLen:
        segments_count += 1

    segments = {}  # dict that keep all segements

    # loop that fill the array with seq_num and data
    i = 0
    while i < segments_count - 1:
        segments[i] = "M," + str(i) + "," + data[i*segment_size:(i+1) * segment_size]
        i += 1

    segments[i] = "E," + str(i) + "," + data[i*segment_size:]

    window_size = 1
    # index array that keep the segments that going to send but didn't sent yet
    segments_to_send = list(range(segments_count))
    # index array that keep the segments that sending in this current window
    segments_sending = []

    # the while

    while len(segments_to_send) > 0:
        i = 0
        while i < window_size and len(segments_to_send) > 0:
            seq_num = segments_to_send.pop(0)
            segments_sending.append(seq_num)

            packet = segments[seq_num]

            print("Send Segment " + str(seq_num))

            udp_app_socket.sendto(packet.encode(), ("127.0.0.1", 20530))

            i += 1

        timeout = False
        while len(segments_sending) > 0 and not timeout:
            try:
                ack_packet = udp_app_socket.recvfrom(4096)
                seq_num = int(ack_packet[0].decode("utf-8"))
                print("Get ACK for segment " + str(seq_num))
                if seq_num in segments_sending:
                    segments_sending.remove(seq_num)
            except socket.error:
                timeout = True

        if timeout:
            print("Decrease Window")
            window_size = int(max(window_size / 2, 1))
        else:
            print("Increase Window")
            window_size += 1

        # put all the segments that we didn't got ack on them, we put the back in the segment_to_send array
        # and empty the array of segments sending and do the while all again to send the segments that didnt get ack again
        segments_to_send = segments_sending + segments_to_send
        segments_sending = []

    # end while

    # Closing sockets
    img_server_socket.close()
    udp_app_socket.close()


if __name__ == "__main__":
    udp_server()
