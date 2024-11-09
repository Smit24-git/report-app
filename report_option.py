import re
from shared import clear_screen, print_options_and_get_selection
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

options = [
    "1. view reports",
    "2. add new report",
    "3. remove report",
    "0. go to previous option"
]

exit_option = 0 

def list_all():
    res = db.list_reports()

def add_report():
    name = input("command name: ")
    print("command/query: ")
    command = ''
    line = ''
    while line != ':wq':
        command += line + ' '
        line = input()
    command = command.lstrip()
    print("")
    res = db.list_db_connections();
    for conn in res:
        print(conn)
    
    print("")
    db_conn = int(input("select database: "))
    
    print("")
    grps = db.list_groups()

    for grp in grps:
        print(grp)
    
    print("")
    selected_groups = input("select group(s): ")
    group_list = selected_groups.split(" ")


    print("")
    keys = []
    parameters = []
    report_parameter = {}
    if input("Do you want to add parameters? (Y/N): ") == "Y":
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
        if len(keys) > 0:
            for key in keys:
                value = input(f"{key}: ")
                parameters.append({
                    "key": key,
                    "value": value,
                })
        if len(parameters) > 0:
            default = input("set as default parameters? (Y/N): ")
            is_default = True if default == "Y" else  False
            report_parameter = {
                "is_def": is_default,
                "parameters": parameters,
            }

    data = {
        "name": name,
        "command": command,
        "db_conn": db_conn,
        "groups": group_list,
        "report_parameter": report_parameter,
    }
   

    db.add_report(data)
    input("\npress enter to continue...")


def remove_report():
    """ remove reports """


def continue_with_report_option():
    """ runs with report options """
    
    selection = print_options_and_get_selection(options)

    while(selection != exit_option):
        match selection:
            case 1:
                list_all()
            case 2:
                add_report()
            case 3:
                remove_report()
            case _:
                input("\ninvalid option. \n")

        selection = print_options_and_get_selection(options)

