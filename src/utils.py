def clear_screen():
    """
        Dirty hack to clear the terminal screen.
    """

    print(chr(27) + "[2J")