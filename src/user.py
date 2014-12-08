"""

The user structure is as follows:

  user = { emails: { sent: [ ... ],
                     received: [ ... ] },
           name: "Cristiano Ronaldo",
           password: "irina" }


  email = { subject: "Novo Contrato",
            sender: user_instance,
            receivers: [ user_instance, ... ],
            content: "Aumentem-me o ordenado." }

"""

import utils

def login(print_error):
    utils.clear_screen()

    if print_error:
        print(print_error)
    
    print("Welcome to mail-server, you are welcome to log in.")
    name = input("Name: ")
    password = input("Password: ")

    return { "name": name, "password": password }


def add_sent_email(user, email):
    """
        Adds a sent email to user `user`
    """

    user.emails.sent.append(email)


def add_received_email(user, email):
    """
        Adds a received email to user `user`
    """

    user.emails.received.append(email)
