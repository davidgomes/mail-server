import json
import threading
import socketserver
import utils

from ast import literal_eval

HOST = ''
PORT = 50003

class ThreadedTCPRequestHandler(socketserver.BaseRequestHandler):
    def handle(self):
        while True:
            data = self.request.recv(1024)
            cur_thread = threading.current_thread()

            data = data.decode()
            if not data: continue

            print("data: %s" % data)
            split_data = data.split()
            command_name = split_data[0]
            information = " ".join(split_data[1:])

            if command_name == "GET":
                response = self.server.get(information)
            elif command_name == "SEND":
                response = self.server.send(information)
            elif command_name == "DELETE":
                response = self.server.delete_email(information)

            self.request.sendall(response.encode())

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True

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

    def delete_email(self, info):
        split_info = " ".join(info.split()[:-1]).split("} {")
        info_user = literal_eval(split_info[0] + "}")
        info_email = literal_eval("{" + split_info[1])
        received_or_sent = info.split()[-1].strip()

        try:
            full_user = self.find_user(info_user)
        except Exception as error:
            return "ERROR {0}".format(error)

        try:
            full_user["emails"][received_or_sent].remove(info_email)
        except ValueError:
            return "ERROR Email not found."

        return str(full_user)
        
    def send(self, info):
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

        return str(full_user)

    def get(self, info):
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
        user_file = open("users.json", "w")
        user_file.write(json.dumps(users))
        user_file.close()

        super().shutdown()

def main():
    utils.clear_screen()

    server = ThreadedTCPServer((HOST, PORT), ThreadedTCPRequestHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.daemon = True
    server_thread.start()
    server_thread.join()

if __name__ == "__main__":
    main()
