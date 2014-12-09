import os
import sys
import socket
import json
import threading
import socketserver
import utils

from ast import literal_eval

HOST = ''
PORT = 50003

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        data = self.request.recv(1024)
        cur_thread = threading.current_thread()

        data = data.decode()
        split_data = data.split()
        command_name = split_data[0]
        information = " ".join(split_data[1:])

        if command_name == "GET":
            response = self.server.get(information)
        elif command_name == "SEND":
            response = self.server.send(information)
        elif command_name == "DELETE":
            pass

        self.request.sendall(response.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    users = []

    def find_user(self, client_user):
        found_anything = False

        for user in self.users:
            if user["name"] == client_user["name"]:
                found_anything = True

                if user["password"] == client_user["password"]:
                    return user
                else:
                    raise Exception("Wrong password.")

        if not found_anything:
            raise Exception("User not found.")

    def send(self, info):
        print("Got a SEND request.")

        info = literal_eval(info)

        try:
            full_user = self.find_user(info)
        except Exception as error:
            return "ERROR {0}".format(error)

        # Add the email to each receiver's inbox
        for receiver in info["email"]["receivers"]:
            for user in self.users:
                if receiver == user["name"]:
                    print("Adding received email to " + user["name"])
                    user["emails"]["received"].append(info["email"])

                if full_user["name"] == user["name"]:
                    user["emails"]["sent"].append(info["email"])

        print(self.users)
        return ""

    def get(self, info):
        print("Got a GET request.")
        print(info)

        client_user = literal_eval(info)

        try:
            full_user = self.find_user(client_user)
            return str(full_user)
        except Exception as error:
            return "ERROR {0}".format(error)

    def __init__(self, server_address, handler_class):
        user_file = open("users.json", "r")
        self.users = json.loads(user_file.read())
        user_file.close()

        self.allow_reuse_address = True

        socketserver.TCPServer.__init__(self, server_address, handler_class)

    def shutdown(self):
        user_file = open("users.txt", "w")
        user_file.write(json.dumps(users))
        user_file.close()

        super().shutdown()

def server_get(info, conn):
    # 'data' is a dictionary in a string, containing ["user"] and ["password"]
    # parse it into client_user

    print("Got a GET request.")
    print(users)

    client_user = literal_eval(info)

    try:
        full_user = server_find_user(client_user)
        conn.sendall(str(full_user).encode())
    except Exception as error:
        conn.sendall("ERROR {0}".format(error).encode())

def server_send(info, conn):
    """
    Find the full user in `users`, from ["user"] and ["password"].

    Then proceed to sending the email in ["email"].
    """

    print("Got a SEND request.")

    info = literal_eval(info)

    try:
        full_user = server_find_user(info)
    except Exception as error:
        conn.sendall("ERROR {0}".format(error).encode())
        return

    # Add the email to each receiver's inbox
    for receiver in info["email"]["receivers"]:
        for user in users:
            if receiver == user["name"]:
                print("Adding received email to " + user["name"])
                user["emails"]["received"].append(info["email"])

    # Add the email to the sender's send box
    full_user["emails"]["sent"].append(info["email"])

    print(users)

def main():
    utils.clear_screen()

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()

if __name__ == "__main__":
    main()
