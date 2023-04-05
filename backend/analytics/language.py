import psycopg2
import sys
import pandas as pd

# connection parameters
param_dic = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "Incorrect-10"
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


# helper function for user_language_data
def user_lang_sql(cursor, langcode, language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.cookies
        Where language Like '{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = {"name": language, "value": num[0][0]}
    return data


def piechart_colours(data):
    colours = [
        "#63C1BD",#turquoise
        "#304C89",  # dark blue
        "#ABDAFC",  # Light blue
        "#F7C548", #yellow
        "#D36135",  # orange
        "#3A5A40", #green
        "#A24936" #Brown
   ]
    i = 0
    for lang in data:
        lang["colour"] = colours[i]
        i += 1


# returns an array of dictionaries in the format {x:"language", y: int(number of users with that browser lang)}
def user_language_data():
    datalist = []
    cursor = conn.cursor()
    languages = [("en", "English"), ("es", "Spanish"), ("sl", "Slovenian"), ("it", "Italian"), ("fr", "French"),
                 ("de", "German")]
    for i in languages:
        data = user_lang_sql(cursor, i[0], i[1])
        datalist.append(data)
    total = user_lang_sql(cursor, "%", "total")
    sum = 0
    for i in datalist:
        sum = sum + i["value"]
    other = total["value"] - sum
    datalist.append({"name": "Other", "value": other})
    cursor.close()
    piechart_colours(sorted(datalist, key = lambda x: x["value"], reverse=True))
    return datalist


# helper function for material_language_data
def material_lang_sql(cursor, langcode, language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.oer_materials
        Where language Like '%{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = {"name": language, "value": num[0][0]}
    return data


# returns an array of dictionaries in the format {x:"language", y: int(number of materials with that language )}
def material_language_data():
    datalist = []
    languages = [("en", "English"), ("es", "Spanish"), ("sl", "Slovenian"), ("it", "Italian"), ("fr", "French"),
                 ("de", "German")]
    cursor = conn.cursor()
    for i in languages:
        data = material_lang_sql(cursor, i[0], i[1])
        datalist.append(data)
    total = material_lang_sql(cursor, "%", "total")
    sum = 0
    for i in datalist:
        sum = sum + i["value"]
    other = total["value"] - sum
    datalist.append({"name": "Other", "value": other})
    cursor.close()
    piechart_colours(datalist)
    return datalist


def percentager(datalist):
    sum = 0
    for i in datalist:
        sum += i[1]
    pcts = map(lambda num: round(num[1] / sum * 100, 1), datalist)
    temp = list(pcts)
    for i in range(0, len(datalist)):
        datalist[i] = (datalist[i][0], temp[i])
    return datalist


def compare_language_data():
    finallist = []
    datalist1 = []
    datalist2 = []
    languages = [("en", "English"), ("es", "Spanish"), ("sl", "Slovenian"), ("it", "Italian"), ("fr", "French"),
                 ("de", "German")]
    cursor = conn.cursor()
    for i in languages:
        user = user_lang_sql(cursor, i[0], i[1])
        material = material_lang_sql(cursor, i[0], i[1])
        datalist1.append((user["name"], user["value"]))
        datalist2.append((material["name"], material["value"]))
    cursor.close()
    dl1 = percentager(datalist1)
    dl2 = percentager(datalist2)
    j = 0
    cursor = conn.cursor()
    for i in languages:
        user = user_lang_sql(cursor, i[0], i[1])
        material = material_lang_sql(cursor, i[0], i[1])
        finallist.append({"name": user["name"], "value1": dl1[j][1], "value2": dl2[j][1]})
        j += 1
    return finallist


conn = connect(param_dic)
