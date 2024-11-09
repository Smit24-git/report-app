from shared import clear_screen, print_options_and_get_selection
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

options = [
    "1. view groups",
    "2. add new group",
    "3. update group",
    "4. remove group",
    "0. go back to previous option"
]
exit_option = 0

def list_all():
    res = db.list_groups()
    for conn in res:
        print(conn)
    input("\npress enter to continue...")

def add_group():
    clear_screen()
    name = input("group name: ")
    data = ({
        "name": name,
    },)
    
    try:
        db.add_groups(data)
    except Exception as e:
        print(e)
        input("\npress enter to continue...")
        clear_screen()
        return

    clear_screen()
    print("\nnew group registered...")
    input("\npress enter to continue...")
    clear_screen()


def print_groups():
    groups = db.list_groups()
    for group in groups:
        print(group)
    return groups

def is_group_exist(grp_id,grps):
    for grp in grps:
        if grp[0] == int(grp_id):
            return True
    return False

def update_group():
    grps = print_groups();
    grp_id = input("select group:") 
    if is_group_exist(grp_id, grps):
        name = input("new name:")
        db.update_group({
            'id': grp_id,
            'name': name
        })
        input("\ngroup updated sucessfully."
              "\n\npress enter to continue...")
        clear_screen()
    else:
        input("invalid input. press enter to try again...")
        clear_screen()
        update_group()


def remove_group():
    """remove group"""
    grps = print_groups();
    grp_id = input("select group:") 
    if is_group_exist(grp_id, grps):
        db.remove_group(grp_id)
        input("\ngroup removed sucessfully."
              "\n\npress enter to continue...")
        clear_screen()
    else:
        input("invalid input. press enter to try again...")
        clear_screen()
        remove_group()


def continue_with_report_group_option():
    """ runs with report group options """
    print("")
    selection = print_options_and_get_selection(
        options
    )
    while(selection != exit_option):
        match selection:
            case 1:
                list_all()
            case 2:
                add_group()
            case 3:
                update_group()
            case 4:
                remove_group()
            case _:
                input("\ninvalid option. \n")


        selection = print_options_and_get_selection(
            options
        )
