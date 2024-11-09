import pyodbc


def mssql_get_data(con,cmd):
    connection = pyodbc.connect(con)
    cursor = connection.cursor()

    cursor.execute(cmd)

    return cursor.fetchall()
