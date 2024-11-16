import re
from shared import clear_screen, print_options_and_get_selection
from shared import is_id_exist, find_by_id
from shared import find_parameter_keys
from shared import input_parameters_by_keys
from update_report_option import continue_with_update_report_option
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

options = [
    "1. view reports",
    "2. add new report",
    "3. update report",
    "4. remove report",
    "0. go to previous option"
]

exit_option = 0 

def get_connection_by_id(con_id, conns):
    for con in conns:
        if con[0]==con_id:
            return con
    return None

def print_groups_by_report(rep_id):
    rep_grps = db.list_report_group_by_report(rep_id)
    for grp in rep_grps:
        print(grp)
    return rep_grps 

def print_parameters_by_report(rep_id):
    report_parameters = db.list_report_parameters_by_report(rep_id)
    for rp in report_parameters:
        print(f"id: {rp[0]}")
        print(f"Default: {True if rp[1]==1 else False}")
        params = db.list_parameters_by_report_parameter(rp[0])
        for param in params:
            print(f"\t{param}")
        print()
    return report_parameters


def list_all():
    conn = db.list_db_connections()
    res = db.list_reports()
    for data in res:
        print("report:")
        print(data)
        
        print("connection:")
        print(get_connection_by_id(data[3],conn))

        print("groups:")
        print_groups_by_report(data[0])

        print("parameters:")
        print_parameters_by_report(data[0])

        print("\n")
    input("press enter to continue")


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
    report_parameter = {}
    if input("Do you want to add parameters? (Y/N): ") == "Y":
        keys = find_parameter_keys(command)
        parameters = []

        if len(keys) > 0:
            parameters = input_parameters_by_keys(keys)
        
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

def update_report():
    res = db.list_reports()
    for data in res:
        print(data)
    print("")
    rep_id = int(input("select report: "))
    rep = find_by_id(rep_id, res) 
    conn = db.list_db_connections()
    clear_screen()

    print(rep)
    print("\nconnection:")
    print(get_connection_by_id(rep[3],conn))

    print("\ngroups:")
    print_groups_by_report(rep[0])

    print("\nparameters:")
    print_parameters_by_report(rep[0])

    # show options
    continue_with_update_report_option(rep)

def remove_report():
    """ remove reports """
    res = db.list_reports()
    for data in res:
        print(data)
   
    rep_id = int(input("select report: "))
    if is_id_exist(rep_id, res):
        db.remove_report(rep_id)
        input("report is removed.\n\npress enter to continue...")
        clear_screen()
    else:
        input("invalid input.\n\npress enter to continue...")
        clear_screen()
        remove_report()

def continue_with_report_option():
    """ runs with report options """
    
    selection = print_options_and_get_selection(options)
    res = db.list_reports()

    while(selection != exit_option):
        clear_screen()
        match selection:
            case 1:
                list_all()
            case 2:
                add_report()
            case 3:
                update_report()
            case 4:
                remove_report()
            case _:
                input("\ninvalid option. \n")
        clear_screen()
        selection = print_options_and_get_selection(options)

