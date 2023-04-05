import psycopg2
import sys
import pandas as pd

#connection parameters
param_dic = {
    "host"      : "localhost",
    "database"  : "postgres",
    "user"      : "postgres",
    "password"  : "Incorrect-10"
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

#changes data to an array of dictionaries for the react front end
def todictionary(data,expand):
    arr = []
    if expand:
        for i in data:
            name = i[1].split()
            arr.append({"x":name[1],"expandedx":i[1],"y": i[0]})
    else:
        for i in data:
            name = i[1].split()
            arr.append({"x":i[1],"expandedx":i[1],"y": i[0]})
    return arr

#helper function for browser_name_data
def browser_name_sql(cursor):
    try:
        cursor.execute("""
        Select count(id), Browser
        From
        (Select id, user_agent,
        CASE
                WHEN user_agent LIKE '%MSIE%' THEN 'Internet Explorer'
                WHEN user_agent LIKE '%Firefox%' THEN 'Mozilla Firefox'
                WHEN user_agent LIKE '%Chrome%' THEN ' Google Chrome'
                WHEN user_agent LIKE '%Safari%' THEN ' Apple Safari'
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

#returns an array of dictionaries
#in the format {"name":"browser name", "value":int(number of users using that browser)}
def browser_name_data():
    cursor = conn.cursor()
    num =browser_name_sql(cursor)
    num.pop() #discard data which does not match browser names
    cursor.close()
    data = todictionary(num,True)
    return data


#helper function for device_name_data
def device_name_sql(cursor):
    try:
        cursor.execute("""
        Select count(id), Device
        From
        (Select id, user_agent,
        CASE
            WHEN user_agent LIKE '%(Mac%' Then 'Macbook'
            WHEN user_agent LIKE '%iPad%' THEN 'iPad'
            WHEN user_agent LIKE '%iPhone%' THEN  'iPhone'
            WHEN user_agent LIKE '%Android%' THEN 'Android'
            WHEN user_agent LIKE '%(Win%' THEN 'Windows'
        END AS Device
        FROM cookies) as t1
        Group by Device
        """)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    nums = cursor.fetchall()
    return nums

#returns an array of dictionaries
#in the format {"name":"device/os name", "value":int(number of users with that device)}
def device_name_data():
    cursor = conn.cursor()
    num =device_name_sql(cursor)
    num.pop()
    cursor.close()
    data = todictionary(num,False)
    return data

conn = connect(param_dic)
#run device_name_data or browser_name_data