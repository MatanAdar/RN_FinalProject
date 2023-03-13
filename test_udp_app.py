import socket

PORT = 20529
APP_ADDRESS = "127.0.0.1"


def udp_server():
    udp_app_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_app_socket.bind((APP_ADDRESS, PORT))

    udp_app_socket.setblocking(True)
    udp_app_socket.settimeout(5)

    # open a connection to the second server that have the object
    img_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    img_server_socket.connect(("127.0.0.1", 30553))

    # checking if we got the request
    while True:
        try:
            request_from_client, client_addr = udp_app_socket.recvfrom(4096)
            request_from_client = request_from_client.decode("utf-8")
        except socket.error:
            continue

        if request_from_client == "Iphone 14":
            print("Got the request")
            got_the_request = "ACK"
            while True:
                try:
                    udp_app_socket.sendto(got_the_request.encode("utf-8"), client_addr)
                    print("Sent ACK to the client")
                    break
                except socket.timeout:
                    continue

            break
        elif request_from_client == "Iphone 13":
            print("Got the request")
            got_the_request = "ACK"
            while True:
                try:
                    udp_app_socket.sendto(got_the_request.encode("utf-8"), client_addr)
                    print("Sent ACK to the client")
                    break
                except socket.timeout:
                    continue

            break
        elif request_from_client == "Galaxy S23":
            print("Got the request")
            got_the_request = "ACK"
            while True:
                try:
                    udp_app_socket.sendto(got_the_request.encode("utf-8"), client_addr)
                    print("Sent ACK to the client")
                    break
                except socket.timeout:
                    continue

            break
        elif request_from_client == "Galaxy S22":
            print("Got the request")
            got_the_request = "ACK"
            while True:
                try:
                    udp_app_socket.sendto(got_the_request.encode("utf-8"), client_addr)
                    print("Sent ACK to the client")
                    break
                except socket.timeout:
                    continue

            break
        else:
            print("Didnt got the request")
            didnt_got_the_reqest = "NACK"
            udp_app_socket.sendto(didnt_got_the_reqest.encode("utf-8"), client_addr)
            print("Sent the client that we didnt get the reuqest")

    # end while

    # waiting that the client tell us that he got ACK
    while True:
        try:
            udp_app_socket.settimeout(10)  # 10 seconds
            response_to_ack = udp_app_socket.recvfrom(4096)
            response_to_ack = response_to_ack[0].decode("utf-8")
            break
        except socket.timeout:
            continue

    while True:
        if response_to_ack == "ACK":
            print("Got ack, great!")
            break
        else:
            continue

    while True:
        if response_to_ack == "ACK":
            print("Got ack, great!")
            break
        else:
            continue

    print("The model phone that the client choice is:", request_from_client)

    print("I dont have what you want but i know the server that have this")
    print("I will connect to this server")

    # Sending the request to the second server
    img_server_socket.send(request_from_client.encode("utf-8"))
    print("Sent the request to the second server")

    response_from_server = img_server_socket.recv(4096)
    url_response = response_from_server
    print("Got the response from the second Server")

   # Set up Reno congestion control parameters

    cwnd = 1
    ssthresh = 16
    # dict that keep all segements
    segments = {}


    # Reno congestion control algorithm
    url_data = url_response.decode()

    segment_size = 5

    url_data_length = len(url_data)

    if url_data_length % segment_size > 0:
        remind = 1
    else:
        remind = 0

    num_segments = int(url_data_length / segment_size) + remind

    ack_received = [False] * num_segments
    dup_ack_index = [0] * num_segments

    # loop that fill the dictionary with seq_num and data ?????
    i = 0
    while i < num_segments:
        index = str(i)
        if i == num_segments - 1:
            segments[i] = "E," + index + "," + url_data[i * segment_size:]
            # index array that keep the segments that going to send but didn't send yet
        else:
            segments[i] = "S," + index + "," + url_data[i * segment_size: (i+1)*segment_size]

        i += 1

    # Check if all segments have been acknowledged
    while True:
        # put all the segments that we didn't got ack on them(segments that not True in the ack_received array), back in the segment_to_send array
        # index array that keep the segments that going to send but didn't send yet
        segments_to_send = []
        for i in range(num_segments):
            if ack_received[i] == False:
                segments_to_send.append(i)

        if len(segments_to_send) == 0:
            print("received ack on every segments")
            break

        # Send new segments up to congestion window size
        count_segment_that_sending = 0
        while count_segment_that_sending < cwnd and len(segments_to_send) > 0:
            seq_num = segments_to_send.pop(0)
            udp_app_socket.sendto(segments[seq_num].encode(), client_addr)
            print("Sent segment", seq_num)
            count_segment_that_sending += 1

        timeout = False
        dup_ack_count = 0
        while count_segment_that_sending > 0:
            # Receive acknowledgments
            try:
                ack_data, addr = udp_app_socket.recvfrom(1024)
                ack_seq_num = int(ack_data.decode())
                print("Received ACK for segment", ack_seq_num)
                if not ack_received[ack_seq_num]:
                    ack_received[ack_seq_num] = True
                    count_segment_that_sending -= 1
                    dup_ack_index[ack_seq_num] = dup_ack_index[ack_seq_num]+1
                    print(dup_ack_index)

                    # Update congestion window size using Reno algorithm
                    if cwnd < ssthresh:
                        cwnd *= 2
                    else:
                        cwnd += 1 / cwnd

                # if we got ack on this seq_num already, so we check if we get 3 dup ack and do Fast retransmit
                else:

                    if dup_ack_count[ack_seq_num] < 3:
                        dup_ack_index[ack_seq_num] = dup_ack_index[ack_seq_num]+1
                    elif dup_ack_count[ack_seq_num] == 3:
                        print("Fast Retransmit")
                        ssthresh = max(int(cwnd/2), 1)
                        cwnd = ssthresh + 3

                        # reseting the seq_num that we got dup ack on him
                        dup_ack_count[ack_seq_num] = 0

                        # adding the 3 seq_num to send again
                        for i in range(seq_num - 2, seq_num):
                            segments_to_send.append(i)
                        break
                    else:
                        dup_ack_count = 0

            except socket.timeout:
                print("Timeout waiting for ACK")
                timeout = True
                break

        if timeout:
            print("Decrease Window")
            ssthresh = cwnd / 2
            cwnd = 1
        else:
            print("Increase Window")
            ssthresh = cwnd


    # end while

    # Closing sockets
    img_server_socket.close()
    udp_app_socket.close()


#def sending_data_to_client():


if __name__ == "__main__":
    udp_server()
