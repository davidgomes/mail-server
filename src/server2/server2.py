import sys
import json
import threading
import socketserver
# import utils
import signal

from ast import literal_eval

HOST = ''

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
                self.user = response
                self.request.sendall(str(response).encode())
            elif command_name == "SEND":
                response = self.server.send(self.user, information)
                self.request.sendall(str(response).encode())
            elif command_name == "DELETE":
                self.server.delete_email(self.user, information)

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    daemon_threads = True
    allow_reuse_address = True

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

    def delete_email(self, user, info):
        split_info = info.split()
        email = literal_eval(" ".join(split_info[:-1]))
        received_or_sent = split_info[-1].strip()

        try:
            user["emails"][received_or_sent].remove(email)
        except ValueError:
            return "ERROR Email not found."

    def send(self, sender_user, email):
        email = literal_eval(email)

        # Add the email to each receiver's inbox
        any_receiver_found = False
        for receiver in email["receivers"]:
            for user in self.users:
                if receiver == user["name"]:
                    any_receiver_found = True
                    user["emails"]["received"].append(email)

                if sender_user["name"] == user["name"]:
                    sender_user["emails"]["sent"].append(email)

        return any_receiver_found

    def get(self, info):
        client_user = literal_eval(info)

        try:
            full_user = self.find_user(client_user)
            return full_user
        except Exception as error:
            return "ERROR {0}".format(error)

    def __init__(self, server_address, handler_class):
        # utils.clear_screen()

        user_file = open("users.json", "r")
        self.users = json.loads(user_file.read())
        user_file.close()

        socketserver.TCPServer.__init__(self, server_address, handler_class)

    def shutdown(self):
        user_file = open("users.json", "w")
        user_file.write(json.dumps(self.users))
        user_file.close()

        super().shutdown()

def main():
    server = ThreadedTCPServer((HOST, int(sys.argv[1])), ThreadedTCPRequestHandler)

    # server_thread = threading.Thread(target=server.serve_forever)
    # server_thread.daemon = True
    # server_thread.start()
    # server_thread.join()

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        server.shutdown()

if __name__ == "__main__":
    main()
