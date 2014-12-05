import socket
import user
import utils

HOST = 'localhost'
PORT = 50007


def client_send_mail():
    pass


def client_read_mail():
    pass


def client_exit():
    pass


def client_menu_wait():
    menu = [ ["Enviar email", client_send_mail],
             ["Ler emails", client_read_mail],
             ["Sair", client_exit] ]

    client_menu(menu)
    menu_option = int(input("Escolhe: ")) - 1 # options start in 1
    menu[menu_option][-1]()


def client_menu(menu):
    utils.clear_screen()

    for i in range(len(menu)):
        menu_option = menu[i]
        print("{0}: {1}".format(i + 1, menu_option[0]))


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    client_user_str = str(user.login()).encode()
    s.sendall(client_user_str)
    client_menu_wait()

    data = s.recv(1024)

    s.close()


if __name__ == "__main__":
    main()
