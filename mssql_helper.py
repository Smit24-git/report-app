import pyodbc


def mssql_get_data(con,cmd):
    connection = pyodbc.connect(con)
    cursor = connection.cursor()

    cursor.execute(cmd)
    
    headers = (col[0] for col in cursor.description)
    records = cursor.fetchall()

    return {
        'column_headers': headers,
        'records': records
    }

