import socket
from _thread import *
import threading
import random
word_list = {
    "ceva": "explicatia lui ceva ",
    "mancare": "ceva fara de care nu poti trai si nu e lichid",
    "vin": "lichid rosu din din struguri ",
    "masina": "are 4 roti ",
    "machinelearning": "visezi foarte urat",
    "ferrari": "faci algoritmul ala blanao la ml si il obtii",
    "covid": "cel mai auzit cuvant in 2020"

}


def get_word():
    entry_list = list(word_list)
    random_key = random.choice(entry_list)
    return [random_key, word_list[random_key]]


def threaded(c):
    list = get_word()
    word = list[0]
    print("THe lenght of the word is ", len(word))

    word_completion = "_" * len(word)
    guessed = False
    guessed_letters = []
    guessed_words = []
    tries = 6
    counter = 0
    print("The word for the explanation is ", list[0])
    print("The explaniaton is :", list[1])
    c.send(list[1].encode("ascii"))
    print("We sent the data through the network ")
    while not guessed and tries > 0:
        counter = counter + 1
        # data received from client
        data = c.recv(1024)
        print("We received data from the clinet")
        guess = str(data.decode('ascii'))
        print("The letter we got from the client is ", guess)
        if len(guess) == 1 and guess.isalpha():
            if guess in guessed_letters:
                print("U already typed it bro", guess)
            elif guess not in word:
                tries -= 1
                guessed_letters.append(guess)
            else:
                print("Good job,", guess, "is in the word!")
                guessed_letters.append(guess)
                word_as_list = [letter for letter in word_completion]
                indices = [i for i, letter in enumerate(
                    word) if letter == guess]
                for index in indices:
                    word_as_list[index] = guess
                word_completion = "".join(word_as_list)
                if "_" not in word_completion:
                    guessed = True
                    # return winner
        elif len(guess) == len(word) and guess.isalpha():
            if guess in guessed_words:
                print("You already guessed the word", guess)
            elif guess != word:
                print(guess, "is not the word.")
                tries -= 1
                guessed_words.append(guess)
            else:
                guessed = True
                word_completion = word
                break
        else:
            print("Wrong the wors is still : !", word_completion)
        print("We send to th client the word : ", word_completion)
        print("The number of the tries left", tries)
        print("Iteration no", counter)
        if not guessed and tries > 0:
            c.send(word_completion.encode('ascii'))

    if guessed:
        word_completion = "win"
        print("We send to the client ", word_completion)
        c.send(word_completion.encode('ascii'))
    else:
        word_completion = "lose"
        print("We send to the client ", word_completion)
        c.send(word_completion.encode('ascii'))

    # connection closed
    print("We closed the connection between them!\n")
    c.close()


def Main():
    host = "127.0.0.1"

    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)
    print("The host is ", host)

    s.listen(5)
    print("socket is listening")

    while True:

        c, addr = s.accept()

        print('Connected to :', addr[0], ':', addr[1])

        start_new_thread(threaded, (c,))
    s.close()


if __name__ == '__main__':
    Main()
