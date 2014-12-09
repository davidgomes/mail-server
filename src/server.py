import os
import sys
import socket
import json
from ast import literal_eval
import socketserver

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50003              # Arbitrary non-privileged port

users = []

def server_find_user(client_user):
    """
    Given a dictionary with fields ["user"] and ["password"], try to "log in"
    and find the full user in `users`.
    """

    found_anything = False

    for user in users:
        if user["name"] == client_user["name"]:
            found_anything = True

            if user["password"] == client_user["password"]:
                return user
            else:
                raise Exception("Wrong password.")

    if not found_anything:
        raise Exception("User not found.")

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
        
def server_process(data, conn):
    data = data.decode()
    split_data = data.split()
    command_name = split_data[0]
    information = " ".join(split_data[1:])

    if command_name == "GET":
        server_get(information, conn)
    elif command_name == "SEND":
        server_send(information, conn)
    elif command_name == "DELETE":
        pass

def main():
    user_file = open("users.txt", "r")
    user_list = json.loads(user_file.read())
    user_file.close()
    
    for user in user_list:
        users.append(user)

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)

    any_connection = False

    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024)

            # keep looking
            if not data: continue

            any_connection = True

            pid = os.fork()

            if pid == 0:
                server_process(data, conn)
                conn.close()
                sys.exit(0)
        except KeyboardInterrupt:
            break

    if any_connection:
        conn.close()

    # TODO Re-write users
    user_file = open("users.txt", "w")
    user_file.write(json.dumps(users))
    user_file.close()

if __name__ == "__main__":
    main()
