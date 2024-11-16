from shared import clear_screen, print_options_and_get_selection
from conn_str_options import  continue_with_connection_string_option
from report_group_option import continue_with_report_group_option
from report_option import continue_with_report_option
import importlib
ReportDB = importlib.import_module("report-db").ReportDB

db = ReportDB()

builder_options = [
    "1. Connection Strings",
    "2. Report Groups",
    "3. Reports",
    "0. EXIT"
]

exit_option = 0


def  main():
    """ init function """
    clear_screen()
    selection = print_options_and_get_selection(builder_options)

    while(selection != exit_option):
        clear_screen()
        match selection:
            case 1:
                continue_with_connection_string_option()
            case 2:
                continue_with_report_group_option()
            case 3:
                continue_with_report_option()
            case _:
                input("\ninvalid option. \n")
        clear_screen()
        selection = print_options_and_get_selection(builder_options)


main()

