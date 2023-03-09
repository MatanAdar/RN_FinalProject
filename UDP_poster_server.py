import socket
import requests
from PIL import Image


global list_of_uml
list_of_uml = {}


# need to check how to make it that the objects will be already in the file
def second_server_app():

    second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    second_server_socket.bind(("127.0.0.1", 30553))

    while True:

        request, app_addr = second_server_socket.recvfrom(4096)

        request = request.decode("utf-8")
        print("Got the Request")

        print(request)

        if request == "Iphone 14":
            # get the img from the func get_image_EndGame
            url_iphone14 = Get_Image_Iphone14()
            second_server_socket.sendto(url_iphone14.encode("utf-8"), app_addr)
            print("Sent the file to the app server")
            break

        if request == "Iphone 13":
            # get the img from the func get_image_InfinityWar
            url_iphone13 = Get_Image_Iphone13()
            second_server_socket.sendto(url_iphone13.encode("utf-8"), app_addr)
            print("Sent the file to the app server")
            break

        if request == "Galaxy S23":
            # get the img from the func get_image_ultron
            url_GalaxyS23 = Get_Image_GalaxyS23()
            second_server_socket.sendto(url_GalaxyS23.encode("utf-8"), app_addr)
            print("Sent the file to the app server")
            break

        if request == "Galaxy S22":
            # get the img from the func get_image_ultron
            url_GalaxyS22 = Get_Image_GalaxyS22()
            second_server_socket.sendto(url_GalaxyS22.encode("utf-8"), app_addr)
            print("Sent the file to the app server")
            break

        else:
            print("the object that you ask for, isn't here")
            exit(1)

    second_server_socket.close()


def Get_Image_Iphone14():

    # URL of the image to download
    url = 'https://9to5mac.com/wp-content/uploads/sites/6/2022/01/iphone-14-news-design.jpg?quality=82&strip=all'
    return url


def Get_Image_Iphone13():

    # URL of the image to download
    url = 'https://i.ytimg.com/vi/l0EvriCfmrE/maxresdefault.jpg'
    return url


def Get_Image_GalaxyS23():

    # URL of the image to download
    url = 'http://johnlewis.scene7.com/is/image/JohnLewis/109920785'
    return url


def Get_Image_GalaxyS22():

    # URL of the image to download
    url = 'https://tecnocell.co.il/wp-content/uploads/2022/11/%D7%A1%D7%9E%D7%A1%D7%95%D7%A0%D7%92-SAMSUNG-S22-ULTRA-256GB-12GB-RAM-%D7%A9%D7%97%D7%95%D7%A8.jpg'
    return url


if __name__ == "__main__":
    second_server_app()
