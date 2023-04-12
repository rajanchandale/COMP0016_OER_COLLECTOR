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

def material_type_sql(cursor,type):
    try:
        cursor.execute((f"""Select Count (type)
        From public.oer_materials
        Where type = '{type}'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = num[0][0]
    return data

def material_type_process(typedata):
    worddoc = ["pptx","doc","docx"]
    textfile = ["html","txt"]
    vid = ["avi","divx","m4v","mov","mp3","rm","mpeg"]
    data = [
        {
            "name": "Microsoft",
            "value": 0,
            "colour": "#F7C548"
        },
        {
            "name": "Textfile",
            "value": 0,
            "colour": "#304C89"
        },
        {
            "name": "Video",
            "value": 0,
            "colour": "#ABDAFC"},
        {
            "name": "PDF",
            "value": 0,
            "colour": "#63C1BD"
        }
    ]

    for i in typedata:
        if i[0] in worddoc:
            data[0]["value"] = data[0]["value"] + i[1]
        if i[0] in textfile:
            data[1]["value"] = data[1]["value"] +  i[1]
        if i[0] in vid:
            data[2]["value"] = data[2]["value"] + i[1]
        if i[0] == "pdf":
            data[3]["value"] = i[1]
    return data

def material_type_raw(conn):
    cursor = conn.cursor()
    #find all the distinct file types
    try:
        cursor.execute("""Select distinct type
        From Public.oer_materials""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    alltypes = cursor.fetchall()
    cursor.close()
    #return a list of (file type, count)
    cursor = conn.cursor()
    counts = []
    for i in alltypes:
        data = material_type_sql(cursor,i[0])
        counts.append((i[0],data))
    return counts

#returns data about material types in a list of dictionaries
#pie chart
def material_type_data():
   data =  material_type_raw(conn)
   processed_data = material_type_process(data)
   return sorted(processed_data, key=lambda x: x["value"], reverse=True)

def vid_process(typedata):
    vid = {"avi":0, "m4v":0, "mov":0,"mp3":0,"rm":0}
    for i in typedata:
        if i[0] in vid:
            vid[i[0]] = i[1]
    dictlist = [{"name":key,"value":value} for key, value in vid.items()]
    colours = ["#63C1BD","#D36135","#304C89","#F7C548","#3A5A40"]
    j =0
    for i in dictlist:
        i["colour"] = colours[j]
        j += 1
    return dictlist

#returns data about video types in a list of dictionaries
#pie chart
def vid_type_data():
    data =  material_type_raw(conn)
    processed_data = vid_process(data)
    return processed_data

def percentager(datalist):
    sum = 0
    for i in datalist:
        sum += i[1]
    pcts = map(lambda num: round(num[1]/sum *100,1),datalist)
    temp =list(pcts)
    for i in range(0,len(datalist)):
        datalist[i]= (datalist[i][0],temp[i])
    return datalist

conn = connect(param_dic)
