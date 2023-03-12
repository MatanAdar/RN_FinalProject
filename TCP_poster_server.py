import socket
import requests
from PIL import Image


def img_server_tcp():

    # ***********************************************************************************************

    # 1
    # creating a TCP socket and receiving the request from the app

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # making that the addr will not say "the addr is already in use"
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    server_socket.bind(("127.0.0.1", 30553))

    server_socket.listen(3)

    # *******************************************************************************

    # 2
    # receiving the request from the app and sending the url_response to the app

    while True:

        connection_socket, server_addr = server_socket.accept()

        request = connection_socket.recv(4096).decode("utf-8")

        print("Got the Request")

        print(request)

        if request == "1":
            # get the img from the func get_image_EndGame
            url_EndGame = Get_Image_EndGame()
            connection_socket.sendall(url_EndGame.encode("utf-8"))
            print("Sent the file to the app server")

        if request == "2":
            # get the img from the func get_image_InfinityWar
            url_InfinityWar = Get_Image_InfinityWar()
            connection_socket.sendall(url_InfinityWar.encode("utf-8"))
            print("Sent the file to the app server")

        if request == "3":
            # get the img from the func get_image_ultron
            url_ultron = Get_Image_Ultron()
            connection_socket.sendall(url_ultron.encode("utf-8"))
            print("Sent the file to the app server")

        else:
            print("the object that you ask for, isn't here")
            exit(1)

    # **************************************************************************************

    # 3
    # closing sockets (the only why the server will close if we manually close them in terminal with ctrl+c)

    connection_socket.close()
    second_server_socket.close()

# helper function to get the url of the EndGame poster
def Get_Image_EndGame():

    # URL of the image to download
    url = 'https://lumiere-a.akamaihd.net/v1/images/p_avengersendgame_19751_e14a0104.jpeg'
    return url

# helper function to get the url of the InfinityWar poster
def Get_Image_InfinityWar():

    # URL of the image to download
    url = 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_.jpg'
    return url

# helper function to get the url of the Ultron poster
def Get_Image_Ultron():

    # URL of the image to download
    url = 'https://www.vintagemovieposters.co.uk/wp-content/uploads/2021/03/IMG_1741-scaled.jpeg'
    return url


if __name__ == "__main__":
    img_server_tcp()
