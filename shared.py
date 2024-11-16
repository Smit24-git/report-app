from os import system, name
import re

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

def find_by_id(_id, data):
    for d in data:
        if _id == d[0]:
            return d
    return None

def is_id_exist(_id, data):
    res = find_by_id(_id, data)
    return res is not None


def find_parameter_keys(command):
    keys = []
    words = re.split("=| ", command)
    for word in words:
        key = ""
        if word.find("$") == -1:
            continue
        
        if word.startswith("$"):
            word = word[1:]
            if word.endswith("'"):
                word = word[:-1]
            key = word

        elif word.startswith("'"):
            word = word[1:]
            if  word.startswith("$"):
                word = word[1:]
                if word.endswith("'"):
                    word = word[:-1]
                key = word
            else:
                raise Exception("failed parsing")
        else:
            raise Exception("failed parsing")
        
        keys.append(key)
    return keys




def input_parameters_by_keys(keys):
    parameters = []
    for key in keys:
        value = input(f"{key}: ")
        parameters.append({
            "key": key,
            "value": value,
        })
    return parameters


