import re
from shared import clear_screen, print_options_and_get_selection
from shared import is_id_exist, find_by_id
from shared import find_parameter_keys
from shared import input_parameters_by_keys
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

opts = [
    "1. assign group",
    "2. unassign group",
    "3. configure new parameters",
    "4. remove existing parameters",
    "0. exit"
]

opt_ext = 0

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

    if is_id_exist(s_type, available_types):
        db.add_report_groups(({
            'rep': rep[0],
            'g_type': s_type,
        },))
        input("group is assigned. \n\npress enter to continue")
    else:
        input("invalid selection. press enter to continue...")
        assign_new_group_for_report(rep)

def unassign_group_for_report(rep):
    """ unassign group from report """
    rep_grps = db.list_report_group_by_report(rep[0])
    for grp in rep_grps:
        print(f"({grp[0]}, {grp[3]})")

    rg_id = int(input("select group:"))
    if is_id_exist(rg_id, rep_grps):
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

def remove_existing_parameters_from_group(rep):
    """ remove existing parameter """
    rparameters = print_parameters_by_report(rep[0])
    rp_id = int(input("select parameter: "))
    
    if is_id_exist(rp_id,rparameters):
        db.remove_report_parameter(rp_id)
        input("parameters removed.\n\npress enter to continue...")
        clear_screen()
    else:
        input("invalid input.\n\npress enter to continue...")
        remove_existing_parameters_from_group(rep)

def continue_with_update_report_option(rep):
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
        clear_screen()
        s_opt = print_options_and_get_selection(opts)
    clear_screen()
    input("\npress enter to continue...")

