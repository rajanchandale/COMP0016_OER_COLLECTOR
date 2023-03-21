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

    
#helper function for user_language_data
def user_lang_sql(cursor,langcode,language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.cookies
        Where language Like '{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = {"x":language,"y":num[0][0]}
    return data

#returns an array of dictionaries in the format {x:"language", y: int(number of users with that browser lang)}
def user_language_data(conn):
    datalist = []
    cursor = conn.cursor()
    data = user_lang_sql(cursor,"en","english")
    datalist.append(data)
    data = user_lang_sql(cursor,"es","spanish")
    datalist.append(data)
    data = user_lang_sql(cursor,"sl","slovenian")
    datalist.append(data)
    data = user_lang_sql(cursor,"it","italian")
    datalist.append(data)
    total = user_lang_sql(cursor,"%","total")
    sum = 0
    for i in datalist:
        sum = sum + i["y"]
    other = total["y"] - sum
    datalist.append({"x":"other","y":other})
    cursor.close()
    return datalist


#helper function for material_language_data
def material_lang_sql(cursor,langcode,language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.oer_materials
        Where language Like '%{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = {"x":language,"y":num[0][0]}
    return data

#returns an array of dictionaries in the format {x:"language", y: int(number of materials with that language )}
def material_language_data(conn):
    datalist = []
    languages = [("en","english"),("es","spanish"),("sl","slovinian"),("it","italian"),("zh","chinese"),("ru","russian")]
    cursor = conn.cursor()
    for i in languages:
        data = material_lang_sql(cursor,i[0],i[1])
        datalist.append(data)
    total = material_lang_sql(cursor,"%","total")
    sum = 0
    for i in datalist:
        sum = sum + i["y"]
    other = total["y"] - sum
    datalist.append({"x":"other","y":other})
    cursor.close()
    return datalist