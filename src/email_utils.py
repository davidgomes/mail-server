"""
A set of functions regarding writing and reading emails and email lists.
"""

import utils

def email_send_interface():
    email = { }

    to = input("To (space-separated names): ").split()
    subject = input("Subject: ")
    content = input("Content: ")

    email["receivers"] = to
    email["subject"] = subject
    email["content"] = content

    return email

def list_wait(email_list):
    """
    Displays a list of emails and allows the user to pick one.
    """

    utils.clear_screen()

    if len(email_list) == 0:
        print("No emails to read. Press Return to go back to the menu.")
        input()
        return

    for index, email in enumerate(email_list):
        print("[{0}] {1}".format(index + 1, email["subject"]))

    email_index = int(input("Which email would you like to read? "))

    display_email_wait(email_list[email_index - 1])

def display_email_wait(which_email):
    """
    Displays a given email and waits for action on it (delete/go back).
    """
    utils.clear_screen()

    print("[Subject] {0}".format(which_email["subject"]))
    print("[Content]")
    print(which_email["content"])

    action = input("Would you like to [D]elete this email or go [B]ack? ")

    # let's delete the email
    if action == "D":
        del which_email
