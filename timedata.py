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

def sqlstatement(cursor,d,m,y):
    try:
        cursor.execute((f"""select count(distinct cookie_id)
        from user_activities
        WHERE timestamp BETWEEN '20{y}-{m:02d}-{d} 00:00:00' AND '20{y}-{m:02d}-{d} 23:59:59';"""))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    return num[0][0]

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

def users_week_data(conn):
    visitors = []
    days = []
    current = datetime.datetime(2018,6,1)
    cursor = conn.cursor()
    for i in range(1,8):
        lastweek = current - timedelta(i)
        days.append(lastweek.strftime("%x"))
        d = int(lastweek.strftime("%d"))
        m = int(lastweek.strftime("%m"))
        y = int(lastweek.strftime("%y"))
        num = sqlstatement(cursor,d,m,y)
        date = str(d)+"/"+str(m)
        visitors.append({"x":date,"y":num})
    cursor.close()
    return visitors

def users_month_data(conn):
    visitors = []
    current = datetime.datetime(2018,6,1)
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



conn = connect(param_dic)
nums = users_month_data(conn)
print(nums)

