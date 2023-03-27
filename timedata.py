import datetime
from datetime import timedelta
import psycopg2
import sys

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

def users_week_sql(cursor,d1,m1,y1,d2,m2,y2):
    try:
        cursor.execute((f"""Select count(distinct(cookie_id)), mydate
        From (SELECT cookie_id,date(timestamp) AS MYDATE
        FROM user_activities
        where timestamp between '20{y1}-{m1:02d}-{d1}' and '20{y2}-{m2:02d}-{d2}') as t1
        group by mydate"""))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    return num

#line graph
def users_week_data(conn):
    visitors = []
    current = datetime.date(2018,6,1)
    weeklater = current + datetime.timedelta(7)
    cursor = conn.cursor()
    d1 = int(current.strftime("%d"))
    m1 = int(current.strftime("%m"))
    y1 = int(current.strftime("%y"))
    d2 = int(weeklater.strftime("%d"))
    m2 = int(weeklater.strftime("%m"))
    y2 = int(weeklater.strftime("%y"))
    nums = users_week_sql(cursor,d1,m1,y1,d2,m2,y2)
    for record in nums:
        date = record[1]
        d = date.strftime("%d")
        m = date.strftime("%m")
        visitors.append({"x":d+"/"+m,"y":record[0]})
    return visitors

def users_month_sql(cursor,d,m,y):
    try:
        cursor.execute((f"""Select count(distinct(cookie_id))
        From(SELECT cookie_id,date(timestamp) AS MYDATE
        FROM user_activities
        where timestamp between '20{y}-{m:02d}-{d}' and '20{y}-{m:02d}-30') as t1
        group by mydate"""))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    return num

#line graph
def users_month_data(conn):
    visitors = []
    current = datetime.date(2018,6,1)
    cursor = conn.cursor()
    d = int(current.strftime("%d"))
    m = int(current.strftime("%m"))
    y = int(current.strftime("%y"))
    num = users_month_sql(cursor,d,m,y)
    day =1
    for i in num:
        visitors.append({"x":str(day)+"/"+str(m),"y":i[0]})
        day +=1
    cursor.close()
    return visitors

#double bar chart
#in format {x:date, y1: june 2018 users, y2: jan 2019 users}
def compare_months_data():
    visitors = []
    month1 = datetime.date(2018,6,1)
    month2= datetime.date(2019,1,1)
    cursor = conn.cursor()
    d = int(month1.strftime("%d"))
    m = int(month1.strftime("%m"))
    y = int(month1.strftime("%y"))
    num = users_month_sql(cursor,d,m,y)
    d = int(month2.strftime("%d"))
    m = int(month2.strftime("%m"))
    y = int(month2.strftime("%y"))
    num2 = users_month_sql(cursor,d,m,y)
    print(num2)
    day =1
    for i in num:
        visitors.append({"x":str(day),"y1":i[0],"y2":num2[day-1][0]})
        day +=1
    cursor.close()
    return visitors


conn = connect(param_dic)



