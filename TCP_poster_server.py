import socket
import requests
from PIL import Image


global list_of_uml
list_of_uml = {}


## need to check how to make it that tobjects will be already in the file
def second_server_app():

    second_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    second_server_socket.bind(("127.0.0.1", 30553))

    second_server_socket.listen(3)

    while True:

        connection_socket, server_addr = second_server_socket.accept()

        request = connection_socket.recv(4096).decode("utf-8")

        print("Got the Request")

        print(request)

        if request == "1":
            # get the img from the func get_image_EndGame
            url_EndGame = Get_Image_EndGame()
            # Open the image file
            # with open('/home/matan/PycharmProjects/RN_Final_Project/EndGame.jpg', 'rb') as file:
            #     image_bytes = file.read()

            connection_socket.sendall(url_EndGame.encode("utf-8"))
            print("Sent the file to the app server")
            break

        if request == "2":
            # get the img from the func get_image_InfinityWar
            url_InfinityWar = Get_Image_InfinityWar()
            # Open the image file
            # with open('/home/matan/PycharmProjects/RN_Final_Project/InfinityWar.jpg', 'rb') as file:
            #     image_bytes = file.read()

            connection_socket.sendall(url_InfinityWar.encode("utf-8"))
            print("Sent the file to the app server")
            break

        if request == "3":
            # get the img from the func get_image_ultron
            url_ultron = Get_Image_Ultron()
            # Open the image file
            # with open('/home/matan/PycharmProjects/RN_Final_Project/Ultron.jpg', 'rb') as file:
            #     image_bytes = file.read()
            #
            #
            connection_socket.sendall(url_ultron.encode("utf-8"))
            print("Sent the file to the app server")
            break

        else:
            print("the object that you ask for, isn't here")
            exit(1)


    connection_socket.close()
    second_server_socket.close()


def Get_Image_EndGame():

    # URL of the image to download
    url = 'https://lumiere-a.akamaihd.net/v1/images/p_avengersendgame_19751_e14a0104.jpeg'
    return url

    # # Send an HTTP request to the URL and get the response object
    # response = requests.get(url, allow_redirects=True)
    #
    # print(f"The status code is: {response.status_code}")
    #
    # # check if the image have been moved temporality to a diffrent URL
    # if response.status_code == 302:
    #     new_url = response.headers['Location']
    #     response = requests.get(new_url)
    #
    # # Check if the request was successful (HTTP status code 200)
    # if response.status_code == 200:
    #     # Open a local file with wb (write binary) permission.
    #     with open("EndGame.jpg", "wb") as file:
    #         # Write the contents of the response to the file.
    #         file.write(response.content)
    #         print("Image downloaded successfully.")
    # else:
    #     print(f"Failed to download image. HTTP status code: {response.status_code}")


def Get_Image_InfinityWar():

    # URL of the image to download
    url = 'https://m.media-amazon.com/images/M/MV5BMjMxNjY2MDU1OV5BMl5BanBnXkFtZTgwNzY1MTUwNTM@._V1_.jpg'
    return url

    # # Send an HTTP request to the URL and get the response object
    # response = requests.get(url, allow_redirects=True)
    #
    # print(f"The status code is: {response.status_code}")
    #
    # # check if the image have been moved temporality to a diffrent URL
    # if response.status_code == 302:
    #     new_url = response.headers['Location']
    #     response = requests.get(new_url)
    #
    # # Check if the request was successful (HTTP status code 200)
    # if response.status_code == 200:
    #     # Open a local file with wb (write binary) permission.
    #     with open("InfinityWar.jpg", "wb") as file:
    #         # Write the contents of the response to the file.
    #         file.write(response.content)
    #         print("Image downloaded successfully.")
    # else:
    #     print(f"Failed to download image. HTTP status code: {response.status_code}")


def Get_Image_Ultron():

    # URL of the image to download
    url = 'https://www.vintagemovieposters.co.uk/wp-content/uploads/2021/03/IMG_1741-scaled.jpeg'
    return url

    # # Send an HTTP request to the URL and get the response object
    # response = requests.get(url, allow_redirects=True)
    #
    # print(f"The status code is: {response.status_code}")
    #
    # # check if the image have been moved temporality to a diffrent URL
    # if response.status_code == 302:
    #     new_url = response.headers['Location']
    #     response = requests.get(new_url)
    #
    # # Check if the request was successful (HTTP status code 200)
    # if response.status_code == 200:
    #     # Open a local file with wb (write binary) permission.
    #     with open("Ultron.jpg", "wb") as file:
    #         # Write the contents of the response to the file.
    #         file.write(response.content)
    #         print("Image downloaded successfully.")
    # else:
    #     print(f"Failed to download image. HTTP status code: {response.status_code}")


if __name__ == "__main__":
    second_server_app()
