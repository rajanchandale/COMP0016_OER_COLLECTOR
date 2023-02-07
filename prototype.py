import psycopg2
import sys
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

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
    document = ["pptx","odp","docx","doc","html","txt"]
    vid = ["avi","divx","m4v","mov","mp3","rm","mpeg"]
    data = [["other document",0],["video",0],["pdf"]]
    for i in typedata:
        if i[0] in document:
            data[0][1] = data[0][1] + i[1]
        if i[0] in vid:
            data[1][1] = data[1][1] + i[1]
        if i[0] == "pdf":    
            data[2].append(i[1])
    return data

def vidprocess(typedata):
    vid = [["avi"],["m4v"],["mov"],["mp3"],["rm"]]
    for i in typedata:
        for j in vid:
            if i[0] == j[0]:
                j.append(i[1])
    return vid

def piechart(title,legtitle,categories,data):
    
    fig, ax = plt.subplots(figsize=(12, 6), subplot_kw=dict(aspect="equal"))

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return "{:.1f}%".format(pct)
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),textprops=dict(color="w"))

    ax.legend(wedges, categories,
            title= legtitle,
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=12, weight="bold")

    ax.set_title(title)

    plt.show()
    
def display(title,leg,completedata):
    languages = []
    data = []
    for i in completedata:
        data.append(i[1])
        languages.append(i[0])
    piechart(title,leg,languages,data)

conn = connect(param_dic)
langdata =language_data(conn)
rawtype= material_type_data(conn)
typedata = typeprocess(rawtype)
viddata = vidprocess(rawtype)
browserdata = browserlang(conn)
#display("languages of x5gon materials","languages",langdata)
#display("type of materials","types",typedata)
#display("video materials","file format",viddata)
#display("User languages","languages",browserdata)

