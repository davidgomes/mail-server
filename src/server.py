import socket
import user
from ast import literal_eval


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

users = []

def main():
    # TODO Read users from file
    users.append({ "name": "david", "password": "lol" })

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        data = conn.recv(1024)

        # keep looking
        if not data: continue

        # 'data' is now a dictionary in a string
        # parse it into client_user
        client_user = literal_eval(data.decode())

        if client_user not in users:
            users.append(client_user)

        conn.sendall(data)

    conn.close()


if __name__ == "__main__":
    main()
