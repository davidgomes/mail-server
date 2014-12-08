import socket
import user
import utils
import email_utils
from ast import literal_eval

HOST = 'localhost'
PORT = 50003

def client_send_mail(user):
    return True

def client_read_received_mail(user):
    email_utils.list_wait(user["emails"]["received"])
    return True

def client_read_sent_mail(user):
    email_utils.list_wait(user["emails"]["sent"])
    return True

def client_exit(user):
    return False

def client_menu_wait(user):
    menu = [ ["Enviar email", client_send_mail],
             ["Ler emails recebidos", client_read_received_mail],
             ["Ler emails enviados", client_read_sent_mail],
             ["Sair", client_exit] ]

    client_menu(menu)
    menu_option = int(input("Escolhe: ")) - 1 # options start in 1
    return menu[menu_option][-1](user)

def client_menu(menu):
    utils.clear_screen()

    for i in range(len(menu)):
        menu_option = menu[i]
        print("{0}: {1}".format(i + 1, menu_option[0]))

def main():
    successful_login = False
    login_error = ""
 
    while not successful_login:
        user_dict = user.login(login_error)
        client_user_str = str(user_dict)

        # Send our login attempt
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.sendall("GET {0}".format(client_user_str).encode())

        # Receive the full user
        server_response = s.recv(1024).decode()
        print("response: " + server_response)

        if server_response.startswith("ERROR"):
            login_error = " ".join(server_response.split()[1:])
        else:
            successful_login = True
            user_dict = literal_eval(server_response)

    # Call menu with to the full user we get back from the server
    while True:
        if not client_menu_wait(user_dict):
            break

    # client_exit leads you where
    s.close()

if __name__ == "__main__":
    main()
