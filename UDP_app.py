import socket

PORT = 20529
APP_ADDRESS = "127.0.0.1"


def udp_server():

    # ************************************************************************************************

    # 1
    # creating UDP socket between app and client and TCP socket between app and server
    # and receiving from client the request and doing the 3 handshake with him(sending acks)

    udp_app_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # making that the addr will not say "the addr is already in use"
    udp_app_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    udp_app_socket.bind((APP_ADDRESS, PORT))

    udp_app_socket.setblocking(True)
    udp_app_socket.settimeout(5)

    # open a connection to the second server that have the object
    img_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    img_server_socket.connect(("127.0.0.1", 30553))

    # to keep the server on
    while True:

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

        # *****************************************************************************************************

        # 2
        # sending the request to the server with TCP socket( like professor amit told us to do) and receiving the url from the server

        print("The model phone that the client choice is:", request_from_client)

        print("I dont have what you want but i know the server that have this")
        print("I will connect to this server")

        # Sending the request to the second server
        img_server_socket.send(request_from_client.encode("utf-8"))
        print("Sent the request to the img server")

        response_from_server = img_server_socket.recv(4096)
        url_response = response_from_server
        print("Got the response from the img Server")

        # ****************************************************************************************************

        # 3
        # sending the url in segments to the client
        # making the UDP socket to work as RUDP socket (using CC reno and ACKS on each segment)

        # *************************
        # 3.1
        # setting parameters and calc how much segments we need to send to the client and making them

        # Set up Reno congestion control parameters

        cwnd = 1
        ssthresh = 16


        # Reno congestion control algorithm
        url_data = url_response.decode()

        # calc the amount of segments app need to send to client to transfer all the data(url) to him
        segment_size = 5

        url_data_length = len(url_data)

        if url_data_length % segment_size > 0:
            remind = 1
        else:
            remind = 0

        num_segments = int(url_data_length / segment_size) + remind

        # boolean array that tell us what seq num of segments got ot the client
        ack_received = [False] * num_segments
        # array that keep track of the amout of ack each seq num get (for 3 dup ack)
        dup_ack_index = [0] * num_segments

        # dict that keep all segments
        segments = {}

        # loop that create the segments with letter , seq num and data
        i = 0
        while i < num_segments:
            index = str(i)
            if i == num_segments - 1:
                segments[i] = "E," + index + "," + url_data[i * segment_size:]
                # index array that keep the segments that going to send but didn't send yet
            else:
                segments[i] = "S," + index + "," + url_data[i * segment_size: (i+1)*segment_size]

            i += 1

        # **********************

        # 3.2
        # checking if all segments have been acknowledged
        # 3.2.1 - adding the segments that didn't get ACK yet to the segments_unacked array
        # 3.2.2 - if the size of segments_unacked is 0 its mean that all the ack received array is True, and we got ACKs on all the segments we sent
        # 3.2.3 - if there still space in chwd(window size) we send to the client the segments until the chwd get full by poping from segments_unacked array and counting the amount segments we're sending
        # 3.2.4 - receiving from the client the seq num segment that he got and checking if we got ACK on him already.
        # if no we're changing ack_received[seq_num] = true and lower the amount of segments we sent and didn't get ack on them yet
        # if yes we're adding the seq_num ack to the array of dup ack, to check if we get 3 dup ack to know if we need to make Fast retransmitted
        # if we got timeout (timeout waiting for ack) we're decreasing ssthresh to be chwd/2 and chwd to be 1
        # else we make the ssthresh to be like chwd

        # Check if all segments have been acknowledged
        while True:
            #  3.2.1
            # put all the segments that we didn't got ack on them(segments that not True in the ack_received array), back in the segment_unacked array
            # index array that keep the segments that didn't get ack yet
            segments_unacked = []
            for i in range(num_segments):
                if ack_received[i] == False:
                    segments_unacked.append(i)

            # 3.2.2
            if len(segments_unacked) == 0:
                print("received ack on every segments")
                break

            # 3.2.3
            # Send new segments up to congestion window size
            count_segment_that_sending = 0
            while count_segment_that_sending < cwnd and len(segments_unacked) > 0:
                seq_num = segments_unacked.pop(0)
                udp_app_socket.sendto(segments[seq_num].encode(), client_addr)
                print("Sent segment", seq_num)
                count_segment_that_sending += 1

            # 3.2.4
            timeout = False
            global ack_seq_num
            ack_seq_num = 0
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

                        # Update congestion window size using Reno algorithm
                        if cwnd < ssthresh:
                            cwnd *= 2
                        else:
                            cwnd += 1 / cwnd

                        if ack_seq_num == seq_num and dup_ack_index[ack_seq_num] < 3:
                            dup_ack_index[ack_seq_num] = dup_ack_index[ack_seq_num]+1
                        elif ack_seq_num == seq_num and dup_ack_index[ack_seq_num] == 3:
                            print("Fast Retransmit")
                            ssthresh = max(int(cwnd/2), 1)
                            cwnd = ssthresh + 3

                            # reseting the seq_num that we got dup ack on him
                            dup_ack_index[ack_seq_num] = 0

                            # adding the 3 seq_num to send again
                            for i in range(seq_num - 2, seq_num):
                                segments_unacked.append(i)
                            break

                    # if we got ack on this seq_num already, so we check if we get 3 dup ack and do Fast retransmit
                    else:

                        if dup_ack_index[ack_seq_num] < 3:
                            dup_ack_index[ack_seq_num] = dup_ack_index[ack_seq_num]+1
                        elif dup_ack_index[ack_seq_num] == 3:
                            print("Fast Retransmit")
                            ssthresh = max(int(cwnd/2), 1)
                            cwnd = ssthresh + 3

                            # reseting the seq_num that we got dup ack on him
                            dup_ack_index[ack_seq_num] = 0

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
            # 3.2.5
            if timeout:
                print("Decrease Window")
                ssthresh = cwnd / 2
                cwnd = 1
            else:
                print("Increase Window")
                ssthresh = cwnd

    # end while

    # ************************************************************************************************************************

    # 4
    # closing sockets (the only why the server will close if we manually close them in terminal with ctrl+c)
    img_server_socket.close()
    udp_app_socket.close()

    # **********************************************************************************************


if __name__ == "__main__":
    udp_server()
