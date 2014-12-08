import socket
import user
from ast import literal_eval
import os


HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50003              # Arbitrary non-privileged port

users = []

def server_get(data, conn):
    # 'data' is a dictionary in a string, containing ["user"] and ["password"]
    # parse it into client_user

    client_user = literal_eval(data)
    for user in users:
        if user["name"] == client_user["name"] and user["password"] == client_user["password"]:
            client_user = user

            print("sending back full user")
            conn.sendall(str(client_user).encode())

def server_process(data, conn):
    data = data.decode()
    split_data = data.split()
    command_name = split_data[0]

    if command_name == "GET":
        server_get(" ".join(split_data[1:]), conn)
    elif command_name == "SEND":
        pass
    elif command_name == "DELETE":
        pass


def main():
    # TODO Read users from file
    users.append({ "name": "david", "password": "lol",
                   "emails": {
                       "sent": [
                           {
                             "subject": "Novo Contrato",
                             "content": "Quero mais dinheiro.\nAssinado Ronaldo."
                           }
                       ],

                       "received": [ ]
                   },
                  })

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen(1)

    any_connection = False
    
    while True:
        try:
            conn, addr = s.accept()
            data = conn.recv(1024)
            any_connection = True
            
            # keep looking
            if not data: continue
            
            pid = os.fork()
            
            if pid == 0:
                server_process(data, conn)
        except KeyboardInterrupt:
            break

    if any_connection:
        print("Closing connection")
        conn.close()


if __name__ == "__main__":
    main()
