import socket

msg_len = 1024
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(("127.0.0.1", 4444))
init_message = sock.recv(msg_len).decode("UTF-8")

user_contine = True

while user_contine:
    possible_prime = input("Enter an integer to check if it's prime: ")
    byte_packet = bytes("%s\n" % possible_prime, "UTF-8")
    sock.send(byte_packet)
    response = str(sock.recv(msg_len).decode("UTF-8")).replace("0", "")

    if "True" in response:
        print(possible_prime, "is a prime.")
    else:
        print(possible_prime, "is not a prime.")

    while True:
        cont_response = input("Continue? (y/n)")
        if cont_response == "y":
            break
        else:
            exit()
