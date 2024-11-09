from shared import clear_screen, print_options_and_get_selection
from periodic_execution import continue_with_periodic_execution
from single_execution import continue_with_single_execution

options = [
    "1. execute periodically",
    "2. execute once",
    "0. EXIT",
]

exit_option = 0

def main():
    selection = print_options_and_get_selection(options)

    while(selection != exit_option):
        match selection:
            case 1:
                continue_with_periodic_execution()
            case 2:
                continue_with_single_execution()
            case _:
                input("\ninvalid option. \n")

        selection = print_options_and_get_selection(options)
main()
