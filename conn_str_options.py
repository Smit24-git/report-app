from shared import multi_line_input 
from shared import clear_screen
from shared import print_options_and_get_selection
from shared import is_id_exist
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

connection_string_options = [
    "1. view connection strings",
    "2. add new connection string",
    "3. update connection string",
    "4. remove connection string",
    "0. go to previous option"
]

connection_string_exit_option = 0


def view_connection_strings():
    """ display list of connection strings """
    res = db.list_db_connections()
    for conn in res:
        print(conn)
    input("\npress enter to continue...")

def add_new_connection_string():
    """ runs series of steps to add new connection string """
    clear_screen()
    alias = input("alias:")
    conn_type = input("connection type (mSsql) :")
    print("connection string:")
    conn_str = multi_line_input()
    data = ({
        "alias": alias,
        "db_type": conn_type,
        "connection_string": conn_str,
    },)
    
    try:
        db.add_db_connections(data)
    except Exception as e:
        print(e)
        input("\npress enter to continue...")
        clear_screen()
        return

    clear_screen()
    print("\nconnection property added.")
    input("\npress enter to continue...")
    clear_screen()

def print_all_connections():
    conns = db.list_db_connections()
    for conn in conns:
        print(conn)
    return conns

def update_connection_string():
    conns = print_all_connections()
    
    con_id = int(input("select id: "))
    if is_id_exist(con_id, conns):
        print("new connection string:")
        connection = multi_line_input()
        db.update_db_connection({
            "con_id": con_id, 
            "con_str": connection
        })
        input("connection String is updated..."
            " press enter to continue...")
        clear_screen()
    else:
        input("invalid input. press enter to try again.")
        clear_screen()
        update_connection_string()

def remove_connection_string():
    """ provides an option to remove existing connection string """
    conns = print_all_connections()
    
    con_id = int(input("select id: "))
    if is_id_exist(con_id, conns):
        db.remove_db_connection(con_id)
        input("connection string is removed..."
            " press enter to continue...")
        clear_screen()
    else:
        input("invalid input. press enter to try again.")
        clear_screen()
        remove_connection_string()

def continue_with_connection_string_option():
    """ runs with connection string options """
    selection = print_options_and_get_selection(
        connection_string_options
    )
    while(selection!=connection_string_exit_option):
        clear_screen()
        match selection:
            case 1:
                view_connection_strings()
            case 2:
                add_new_connection_string()
            case 3:
                update_connection_string()
            case 4:
                remove_connection_string()
            case _:
                input("\ninvalid option. \n")

        clear_screen()
        selection = print_options_and_get_selection(
            connection_string_options
        )

