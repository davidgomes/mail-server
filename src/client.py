import socket
import utils
import user_utils
import email_utils
import time
import sys
from ast import literal_eval

class Client():
    HOST = 'localhost'
    PORT = 50003
    user = dict()

    def send_server(self, what):
        print("what: %s" % what)
        self.s.sendall(what.encode())

    def send_mail(self):
        client_user = self.user
        client_user["email"] = email_utils.email_send_interface()
        self.send_server("SEND {0}".format(str(client_user)))
        time.sleep(5)
        self.user = literal_eval(self.s.recv(1024).decode())

    def read_received_mail(self):
        email_utils.list_wait(self.user["emails"]["received"])

    def read_sent_mail(self):
        email_utils.list_wait(self.user["emails"]["sent"])

    def exit(self):
        sys.exit(0)

    def menu(self, menu):
        utils.clear_screen()

        for i in range(len(menu)):
            menu_option = menu[i]
            print("{0}: {1}".format(i + 1, menu_option[0]))

    def menu_wait(self):
        menu = [ ["Send Email", self.send_mail],
                 ["Read Inbox", self.read_received_mail],
                 ["Read Sent Mail", self.read_sent_mail],
                 ["Exit", self.exit] ]

        self.menu(menu)
        menu_option = int(input("Choose: ")) - 1 # options start in 1
        return menu[menu_option][-1]()

    def login(self):
        successful_login = False
        login_error = ""

        while not successful_login:
            user_dict = user_utils.login_interface(login_error)
            client_user_str = str(user_dict)

            # Send our login attempt
            self.send_server("GET {0}".format(client_user_str))

            # Receive the full user
            server_response = self.s.recv(1024).decode()

            print("response: " + server_response)

            if server_response.startswith("ERROR"):
                login_error = " ".join(server_response.split()[1:])
                self.load_socket()
            else:
                successful_login = True
                self.user = literal_eval(server_response)

        while True:
            self.menu_wait()

    def load_socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.connect((self.HOST, self.PORT))

    def __init__(self):
        self.load_socket()

def main():
    client = Client()
    client.login()

if __name__ == "__main__":
    main()
