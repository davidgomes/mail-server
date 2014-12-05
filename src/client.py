import socket
import user
import utils
import email_utils
from ast import literal_eval

HOST = 'localhost'
PORT = 50007

def client_send_mail():
    pass


def client_read_received_mail(user):
    return email_utils.read_list(user["emails"]["received"])


def client_read_sent_mail(user):
    return email_utils.read_list(user["emails"]["sent"])


def client_exit():
    pass


def client_menu_wait(user):
    menu = [ ["Enviar email", client_send_mail],
             ["Ler emails recebidos", client_read_received_mail],
             ["Ler emails enviados", client_read_sent_mail],
             ["Sair", client_exit] ]

    client_menu(menu)
    menu_option = int(input("Escolhe: ")) - 1 # options start in 1
    menu[menu_option][-1](user)


def client_menu(menu):
    utils.clear_screen()

    for i in range(len(menu)):
        menu_option = menu[i]
        print("{0}: {1}".format(i + 1, menu_option[0]))


def main():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    user_dict = user.login()
    client_user_str = str(user_dict).encode()

    # Send our login attempt
    s.sendall(client_user_str)

    # Receive the full user
    server_response = s.recv(1024).decode()
    user_dict = literal_eval(server_response)

    # Call menu with to the full user we get back from the server
    print(user_dict)
    #print(user_dict["emails"]["received"])
    client_menu_wait(user_dict)

    s.close()


if __name__ == "__main__":
    main()
