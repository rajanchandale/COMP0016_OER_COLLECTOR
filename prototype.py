import psycopg2
import sys
import pandas as pd
#connection parameters
param_dic = {
    "host"      : "localhost",
    "database"  : "x5gon",
    "user"      : "postgres",
    "password"  : "pass123"
}
def connect(params_dic):
    """ Connect to the PostgreSQL database server """
    conn = None
    try:
        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(**params_dic)
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        sys.exit(1) 
    print("Connection successful")
    return conn

def postgresql_to_dataframe(conn):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    alist = []
    cursor = conn.cursor()
    try:
        cursor.execute("""Select Count (language)
        From public.Cookies
        Where language Like '%\en%'; """)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # Naturally we get a list of tupples
    num = cursor.fetchall()
    alist.append(("english",num))
    try:
        cursor.execute("""Select Count (language)
        From public.Cookies
        Where language Like '%\zh%'; """)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return 1
    # Naturally we get a list of tupples
    num = cursor.fetchall()
    alist.append(("chinese",num))
    cursor.close()
    print(alist)
    return alist

conn = connect(param_dic)
postgresql_to_dataframe(conn)
