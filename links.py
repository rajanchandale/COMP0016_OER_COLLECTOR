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

def sqlstatement(cursor):
    try:      
        cursor.execute("""Select cookie_id
            From(Select Count(cookie_id),cookie_id
            From user_activities
            Group By Cookie_id) as t1
            where t1.count > 99 and t1.count < 150
        """)
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    nums = cursor.fetchall()
    return nums

def sqlstatement1(cursor,cookie):
    try:      
        cursor.execute(f"""Select t2.cookie_id, user_activities.url_id
                    From(Select cookie_id
                    From(Select Count(cookie_id),cookie_id
                    From user_activities
                    Group By Cookie_id) as t1
                    where t1.cookie_id = {cookie}) as t2
                    Inner Join user_activities on t2.cookie_id = user_activities.cookie_id""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    nums = cursor.fetchall()
    return nums

def id_url_sql(cursor,id):
    try:      
        cursor.execute(f"""Select urls.url
        From urls 
        where urls.id = {id}""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    nums = cursor.fetchall()
    return nums

def process(conn):
    pairs = {}
    cursor = conn.cursor()
    cookies = sqlstatement(cursor)
    cursor.close()
    cursor = conn.cursor()
    for i in cookies:
        cookie = i[0]
        data = sqlstatement1(cursor,cookie)
        for i in range(0,len(data)-1):
            if data[i][0] == data[i+1][0]: #if they are the same cookie
                if data[i][1] != data[i+1][1]: #if it is not a link from a website to itself
                    key = (data[i][1],data[i+1][1])
                    if key in pairs:
                        pairs[key] = pairs[key]+1
                    else:
                        pairs[key] = 1
    cursor.close()
    sorted_pairs = sorted(pairs.items(), key=lambda x:x[1])
    final = []
    for i in range(15):
        link = sorted_pairs.pop()
        source = link[0][0]
        target = link[0][1]
        a=id_url_sql(source)
        b=id_url_sql(target)
        final.append({"source":a,"target":b,"value":link[1]})
        break
    print(final)
    return(final)
    
        
conn = connect(param_dic)
process(conn)

