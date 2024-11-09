import re
from shared import clear_screen, print_options_and_get_selection
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


def get_report_by_id(rep_id,reports):
    for rep in reports:
        if rep[0] == int(rep_id):
            return rep
    return None

def update_report():
    res = db.list_reports()
    for data in res:
        print(data)
    print("")
    rep_id = input("select report: ")
    rep = get_report_by_id(rep_id, res) 
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
    opts = [
        "1. assign group",
        "2. unassign group",
        "3. configure new parameters",
        "4. remove existing parameters",
        "0. exit"
    ]
    opt_ext = 0

    s_opt = print_options_and_get_selection(opts)

    while s_opt != opt_ext:
        match s_opt:
            case 1:
                assign_new_group_for_report(rep)
            case 2:
                unassign_group_for_report(rep)
            case 3:
                configure_new_parameters_for_group(rep)
            case 4:
                remove_existing_parameters_from_group(rep)
            case _:
                input("\ninvalid option. \n")
        s_opt = print_options_and_get_selection(opts)
    input("\npress enter to continue...")


def assign_new_group_for_report(rep):
    """ assign new group from available groups """
    types = db.list_groups()
    rep_grps = db.list_report_group_by_report(rep[0])
    available_types = []
    for t in types:
        t_exists = False
        for grp in rep_grps:
            if t[0] == grp[2]:
                t_exists = True
                break
        if not t_exists:
            available_types.append(t)
    
    for at in available_types:
        print(at)

    s_type = int(input("select group: "))

    if is_group_exist(s_type, available_types):
        db.add_report_groups(({
            'rep': rep[0],
            'g_type': s_type,
        },))
        input("group is assigned. \n\npress enter to continue")
    else:
        input("invalid selection. press enter to continue...")
        assign_new_group_for_report(rep)


def is_group_exist(g_id, grps):
    for grp in grps:
        if g_id == grp[0]:
            return True
    return False

def unassign_group_for_report(rep):
    """ unassign group from report """
    rep_grps = db.list_report_group_by_report(rep[0])
    for grp in rep_grps:
        print(f"({grp[0]}, {grp[3]})")

    rg_id = int(input("select group:"))
    if is_group_exist(rg_id, rep_grps):
        db.remove_report_group(rg_id)
        input("group unassigned successfully."
              "\n\npress enter to continue")
        clear_screen()
    else:
        input("invalid input...\n\nplease try again")
        clear_screen()
        unassign_group_for_report(rep)

def configure_new_parameters_for_group(rep):
    """ conf new parameters """
    # search for parameter keys
    command = rep[2]
    keys = find_parameter_keys(command)
    if len(keys) > 0:
        is_default = False
        parameters = input_parameters_by_keys(keys)
        d_params = db.list_default_parameters_by_report(rep[0])
        if len(d_params) == 0:
            is_default = input("set as default parameter? (Y/n): ") == 'Y'

        report_parameter = {
            "report": rep[0],
            "is_def": is_default,
            "parameters": parameters,
        }
        db.add_report_parameter(report_parameter)
        input("parameters added.\n\npress enter to continue")
        clear_screen()
    else:
        input("""command does not have any parameters, or parameters are
              not setup properly.\n\npress enter to continue...""")
        clear_screen()

def is_report_parameter_exist(rp_id, rps):
    for rp in rps:
        if rp[0] == int(rp_id):
            return True
    return False

def remove_existing_parameters_from_group(rep):
    """ remove existing parameter """
    # display list
    rparameters = print_parameters_by_report(rep[0])
    # take input
    rp_id = int(input("select parameter: "))
    
    if is_report_parameter_exist(rp_id,rparameters):
        db.remove_report_parameter(rp_id)
        input("parameters removed.\n\npress enter to continue...")
        clear_screen()
    else:
        input("invalid input.\n\npress enter to continue...")
        remove_existing_parameters_from_group(rep)

def is_report_exist(rep_id, reports):
    for rep in reports:
        if rep[0] == int(rep_id):
            return True
    return False

def remove_report():
    """ remove reports """
    # display list
    res = db.list_reports()
    for data in res:
        print(data)
   
    rep_id = input("select report: ")
    if is_report_exist(rep_id, res):
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

        selection = print_options_and_get_selection(options)

