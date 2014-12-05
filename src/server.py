import socket
import user
from ast import literal_eval


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

users = []

def main():
    # TODO Read users from file
    users.append({ "name": "david", "password": "lol",
                   "emails": {
                       "sent": [
                           { "subject": "Novo Contrato" }
                       ],

                       "received": [ ]
                   },
                  })

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
        for user in users:
            print(user)
            if user["name"] == client_user["name"] and user["password"] == client_user["password"]:
                client_user = user

        conn.sendall(str(client_user).encode())

    conn.close()


if __name__ == "__main__":
    main()
