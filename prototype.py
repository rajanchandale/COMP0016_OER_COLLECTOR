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

def sqlstatement(cursor,langcode,language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.oer_materials
        Where language Like '%{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = (language,num[0][0])
    return data

def sqlstatement1(cursor,type):
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

def sqlstatement2(cursor,langcode,language):
    try:
        cursor.execute((f"""Select Count (language)
        From public.cookies
        Where language Like '{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = (language,num[0][0])
    return data

def language_data(conn):
    datalist = []
    cursor = conn.cursor()
    data = sqlstatement(cursor,"en","english")
    datalist.append(data)
    data = sqlstatement(cursor,"es","spanish")
    datalist.append(data)
    data = sqlstatement(cursor,"sl","slovenian")
    datalist.append(data)
    data = sqlstatement(cursor,"it","italian")
    datalist.append(data)
    total = sqlstatement(cursor,"%","total")
    sum = 0
    for i in range(0,len(datalist)):
        sum = sum + datalist[i][1]
    other = total[1] - sum
    datalist.append(("other",other))
    cursor.close()
    return datalist

def browserlang(conn):
    datalist = []
    cursor = conn.cursor()
    data = sqlstatement2(cursor,"en","english")
    datalist.append(data)
    data = sqlstatement2(cursor,"es","spanish")
    datalist.append(data)
    data = sqlstatement2(cursor,"sl","slovenian")
    datalist.append(data)
    data = sqlstatement2(cursor,"it","italian")
    datalist.append(data)
    data = sqlstatement2(cursor,"zh","chinese")
    datalist.append(data)
    data = sqlstatement2(cursor,"ru","russian")
    datalist.append(data)
    total = sqlstatement2(cursor,"%","total")
    sum = 0
    for i in range(0,len(datalist)):
        sum = sum + datalist[i][1]
    other = total[1] - sum
    datalist.append(("other",other))
    cursor.close()
    return datalist

def material_type_data(conn):
    cursor = conn.cursor()
    try:
        cursor.execute("""Select distinct type
        From Public.oer_materials""")
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    tupples = cursor.fetchall()
    cursor.close()

    cursor = conn.cursor()
    column_names = ["types","counts"]
    counts = []
    for i in tupples:
        data = sqlstatement1(cursor,i[0])
        counts.append((i[0],data))
    #df = pd.DataFrame(counts, columns=column_names)
    return counts

def typeprocess(typedata):
    worddoc = ["pptx","doc","docx"]
    other = ["odp","ods","html","txt"]
    vid = ["avi","divx","m4v","mov","mp3","rm","mpeg"]
    data = [["presentation",0],["other",0],["video",0],["pdf",0]]
    for i in typedata:
        if i[0] in worddoc:
            data[0][1] = data[0][1] + i[1]
        if i[0] in other:
            data[1][1] = data[1][1] +  i[1]
        if i[0] in vid:
            data[2][1] = data[2][1] + i[1]
        if i[0] == "pdf":
            data[3][1] = i[1]
        
    return data

def vidprocess(typedata):
    vid = [["avi"],["m4v"],["mov"],["mp3"],["rm"]]
    for i in typedata:
        for j in vid:
            if i[0] == j[0]:
                j.append(i[1])
    return vid

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
langdata =percentager(language_data(conn))
rawtype= material_type_data(conn)
typedata = percentager(typeprocess(rawtype))
viddata = percentager(vidprocess(rawtype))
browserdata = percentager(browserlang(conn))



