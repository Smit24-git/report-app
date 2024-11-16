import time
import math
import importlib
import re
from mssql_helper import mssql_get_data 
from file_manager import FileManager
from shared import find_by_id

ReportDB = importlib.import_module("report-db").ReportDB
db = ReportDB()

def list_and_get_group_name():
    group_list = db.list_groups()
    
    for grp in group_list:
        print(grp)

    return input("choose group:")

def replace_command_parameters(cmd, params):
    for p in params:
        cmd = re.sub(f'\${p[1]}',p[2],cmd)
    return cmd

def run_continous_loop(grp_n, timer, cycles):
    timestamp = math.floor(time.time())
    loop_file_name = f"./reports/{timestamp}_{grp_n}_t{timer}_c{cycles}.txt"
    f = FileManager(loop_file_name)
    reports = db.list_reports_by_group(grp_n)
    conns = db.list_db_connections()

    c_cycle = 0
    input("press enter to begin...")
    while( c_cycle < cycles):
        for report in reports:
            cmd = report[2]
            parameters = db.list_default_parameters_by_report(report[0])
            cmd = replace_command_parameters(cmd, parameters)
            con = find_by_id(report[3], conns)
            data = mssql_get_data(con[3],cmd)
            param_list = f",\n\t ".join(
                [f'{p[1]}: {p[2]}' for p in parameters]
            )
            
            print(""
            f"\nreport: '{report[1]}'"
            f"\nparameters:"
            f"\n\t{param_list}"
            f"\nrow count: {len(data['records'])}.\n")

            f.append_string(str(report[1]))
            f.append_data_arr((data['column_headers'],))
            f.append_data_arr(data['records'])
            f.append_string(f"row count: {len(data['records'])}.")
            f.append_new_line()
        c_cycle += 1
        print(f"{c_cycle} cycle(s) completed.")
        if c_cycle != cycles:
            time.sleep(timer * 60)

    print(f"\nsaved in '{loop_file_name}' file.")

def continue_with_periodic_execution():
    """ periodic execution  """
    loop_time = int(input("execution timer (min): "))
    cycles = int(input("cycles: "))
    group_name = list_and_get_group_name()
    
    run_continous_loop(group_name, loop_time, cycles)

    print("\ncycles completed...")
    input("\nplease enter to continue...")
