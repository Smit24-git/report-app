import pyodbc


def mssql_get_data(con,cmd):
    connection = pyodbc.connect(con)
    cursor = connection.cursor()

    cursor.execute(cmd)

    return cursor.fetchall()

def mssql_get_column_names(con, cmd):
    connection = pyodbc.connect(con)
    cursor = connection.cursor()

    cursor.execute(cmd)

    return (col[0] for col in cursor.description)
