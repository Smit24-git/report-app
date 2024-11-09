from os import system, name


def clear_screen():
    if name == 'nt':
        system('cls')
    else:
        system('clear')


def print_options_and_get_selection(options):
    # clear_screen()
    print("\n")
    for option in options:
        print(option)
    print("\n")
    try:
        selection = int(input("enter selection: "))
    except:
        print_options_and_get_selection(options)
    return selection

def multi_line_input():
    line = ''
    res = ''
    while line != ':wq':
        res += line + " "
        line = input()
    return res.lstrip()

