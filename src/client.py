import socket
import user
import utils

HOST = 'localhost'
PORT = 50007

def client_menu():
    print("1. Enviar email")
    print("2. Ler emails")

def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    client_user_str = str(user.login()).encode()
    s.sendall(client_user_str)
    utils.clear_screen()

    data = s.recv(1024)

    s.close()


if __name__ == "__main__":
    main()
