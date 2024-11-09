import time
import math
import importlib
import re
from mssql_helper import mssql_get_data
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

def find_connection(c_id, conns):
    for c in conns:
        if c[0] == c_id:
            return c[3]
    return ''

def run_continous_loop(grp_n, timer, cycles):
    timestamp = math.floor(time.time())
    loop_file_name = f"./reports/{timestamp}_{grp_n}_t{timer}_c{cycles}.txt"
    
    reports = db.list_reports_by_group(grp_n)
    conns = db.list_db_connections()

    c_cycle = 0
    input("press enter to begin...")
    while( c_cycle < cycles):
        for report in reports:
            cmd = report[2]
            parameters = db.list_default_parameters_by_report(report[0])
            cmd = replace_command_parameters(cmd, parameters)
            con = find_connection(report[3], conns)
            data = mssql_get_data(con,cmd)
            param_list = f",\n\t ".join(
                [f'{p[1]}: {p[2]}' for p in parameters]
            )
            
            print(""
            f"\nreport: '{report[1]}'"
            f"\nparameters:"
            f"\n\t{param_list}"
            f"\nrow count: {len(data)}.\n")
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
