import socket


def img_server_udp():

    # ***********************************************************************************************

    # 1
    # creating a socket and receiving the request from the app

    img_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # making that the addr will not say "the addr is already in use"
    img_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    img_server_socket.bind(("127.0.0.1", 30553))
    img_server_socket.listen(5)
    img_server_socket.setblocking(True)
    img_server_socket.settimeout(5)

    connection_socket, app_addr = img_server_socket.accept()
    print(f"connected to server {app_addr}")

    # *******************************************************************************

    # 2
    # receiving the request from the app and sending the url_response to the app

    while True:
        try:
            request = connection_socket.recv(4096)
        except socket.error:
            continue

        handle_request(connection_socket, request, app_addr)

    # **************************************************************************************

    # 3
    # closing sockets (the only why the server will close if we manually close them in terminal with ctrl+c)
    connection_socket.close()
    img_server_socket.close()

# helper function to handle the request and send exactly the url to the app
def handle_request(connection_socket, request, app_addr):

    request = request.decode("utf-8")
    print("Got the Request")
    print(request)

    if request == "Iphone 14":
        # get the img from the func get_image_EndGame
        url_iphone14 = Get_Image_Iphone14()
        connection_socket.sendto(url_iphone14.encode("utf-8"), app_addr)
        print("Sent the file to the app server")

    elif request == "Iphone 13":
        # get the img from the func get_image_InfinityWar
        url_iphone13 = Get_Image_Iphone13()
        connection_socket.sendto(url_iphone13.encode("utf-8"), app_addr)
        print("Sent the file to the app server")

    elif request == "Galaxy S23":
        # get the img from the func get_image_ultron
        url_GalaxyS23 = Get_Image_GalaxyS23()
        connection_socket.sendto(url_GalaxyS23.encode("utf-8"), app_addr)
        print("Sent the file to the app server")

    elif request == "Galaxy S22":
        # get the img from the func get_image_ultron
        url_GalaxyS22 = Get_Image_GalaxyS22()
        connection_socket.sendto(url_GalaxyS22.encode("utf-8"), app_addr)
        print("Sent the file to the app server")

    else:
        print("the object that you ask for, isn't here")



# helper function to get the url of the Iphone 14
def Get_Image_Iphone14():

    # URL of the image to download
    url = 'https://9to5mac.com/wp-content/uploads/sites/6/2022/01/iphone-14-news-design.jpg?quality=82&strip=all'
    return url

# helper function to get the url of the Iphone 13
def Get_Image_Iphone13():

    # URL of the image to download
    url = 'https://i.ytimg.com/vi/l0EvriCfmrE/maxresdefault.jpg'
    return url

# helper function to get the url of the Galaxy S23
def Get_Image_GalaxyS23():

    # URL of the image to download
    url = 'http://johnlewis.scene7.com/is/image/JohnLewis/109920785'
    return url

# helper function to get the url of the Galaxy S22
def Get_Image_GalaxyS22():

    # URL of the image to download
    url = 'https://tecnocell.co.il/wp-content/uploads/2022/11/%D7%A1%D7%9E%D7%A1%D7%95%D7%A0%D7%92-SAMSUNG-S22-ULTRA-256GB-12GB-RAM-%D7%A9%D7%97%D7%95%D7%A8.jpg'
    return url


if __name__ == "__main__":
    img_server_udp()
