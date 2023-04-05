import psycopg2
import sys

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

def sqlstatement(cursor, num):
    try:
        cursor.execute(f"""Select sum(count)
            From(Select t1.count as event, count(t1.count)
            From(Select Count(cookie_id),cookie_id
            From user_activities
            Group By Cookie_id) as t1
            Group By t1.count
            order By event) as t2
            Where event = {num}""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()[0]
    bandtotal = int(num[0])
    return bandtotal

#data about how many cookies have a number of events
#returns a list of dictionaries in the format {"x":"range of events",y:int(number of cookies with that many events)}
#Bar Chart
def eventcount():
    final = []
    cursor = conn.cursor()
    for i in range(1,16):
        num = i
        data  = sqlstatement(cursor,num)
        final.append({"x":num,"y":data})
    cursor.close()
    return final


conn = connect(param_dic)
