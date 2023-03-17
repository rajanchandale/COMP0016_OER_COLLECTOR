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

def sqlstatement(cursor):
    try:
        cursor.execute("""
        Select count(id), Browser
        From
        (Select id, user_agent,
        CASE
                WHEN user_agent LIKE '%edge%'THEN ' Edge'
                WHEN user_agent LIKE '%MSIE%' THEN 'Internet Explorer'
                WHEN user_agent LIKE '%Firefox%' THEN 'Mozilla Firefox'
                WHEN user_agent LIKE '%Chrome%' THEN ' Google Chrome'
                WHEN user_agent LIKE '%Safari%' THEN ' Apple Safari'
                WHEN user_agent LIKE '%Opera%' THEN ' Opera' 
                WHEN user_agent LIKE '%Outlook%' THEN 'Outlook' 
                ELSE 'Unknown'
        END AS Browser
        FROM cookies) as t1
        Group by Browser
        """)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    nums = cursor.fetchall()
    return nums

def todictionary():
    data =browser(conn)
    arr = []
    for i in data:
        arr.append({"browser": i[1],"value": i[0]})
    return arr

def browser(conn):
    cursor = conn.cursor()
    data = sqlstatement(cursor)
    cursor.close()
    return data

conn = connect(param_dic)
todictionary()
