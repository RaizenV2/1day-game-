import socket


def Main():

    host = '127.0.0.1'

    port = 12345

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # connect to server on local computer
    s.connect((host, port))
    username = input("Please enter your username")
    s.send(username.encode('ascii'))
    print(f"We send the username{username} to the server")
    data = s.recv(1024)
    print("Explanation is : ", str(data.decode('ascii')))
    counter = 0
    while True:
        # counter = counter + 1
        message = input("Please input word or letter ")
        s.send(message.encode('ascii'))

        data = s.recv(1024)
        received = ""
        received = data.decode('ascii')
        received = received.strip(" ")
        if received == "win":
            print("U won the game , u are free now \n")
            break
        if received == "lose":
            print("U lost the game,but i'll let you go now \n")
            break
        print("Received: --->", received)
        received = ""
        # print("Iteration no ", counter)

    s.close()


if __name__ == '__main__':
    Main()
