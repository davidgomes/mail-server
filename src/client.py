import socket
import user
import utils
import email_utils
from ast import literal_eval

HOST = 'localhost'
PORT = 50003

def send_server(what):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))
    s.sendall(what.encode())
    return s

def client_refresh(user):
    s = send_server("GET {0}".format(user))
    server_response = s.recv(1024).decode()
    user = literal_eval(server_response)
    s.close()

    return True
    
def client_send_mail(user):
    user["email"] = email_utils.email_send_interface()
    send_server("SEND {0}".format(str(user)))

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
    menu = [ ["Refresh", client_refresh],
             ["Send Email", client_send_mail],
             ["Read Inbox", client_read_received_mail],
             ["Read Sent Mail", client_read_sent_mail],
             ["Exit", client_exit] ]

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
        s = send_server("GET {0}".format(client_user_str))

        # Receive the full user
        server_response = s.recv(1024).decode()
        s.close()

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
