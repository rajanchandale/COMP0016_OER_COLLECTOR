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
        From public.Cookies
        Where language Like '%{langcode}%'; """))
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        cursor.close()
        return "error"
    num = cursor.fetchall()
    data = (language,num[0][0])
    return data

def postgresql_to_data(conn):
    """
    Tranform a SELECT query into a pandas dataframe
    """
    datalist = []
    cursor = conn.cursor()
    data = sqlstatement(cursor,"en","english")
    datalist.append(data)
    datalist.append(("other",901228))
    data = sqlstatement(cursor,"sl","slovenian")
    datalist.append(data)
    data = sqlstatement(cursor,"es","spanish")
    datalist.append(data)
    data = sqlstatement(cursor,"de","german")
    datalist.append(data)
    cursor.close()
    return datalist

def piechart(completedata):
    
    fig, ax = plt.subplots(figsize=(12, 6), subplot_kw=dict(aspect="equal"))

    data = []
    languages =[]
    for i in range(0,len(completedata)):
        data.append(completedata[i][1])
        languages.append(completedata[i][0])
    

    def func(pct, allvals):
        absolute = int(np.round(pct/100.*np.sum(allvals)))
        return "{:.1f}%".format(pct)
    colours = ["#B1D4E0","#2E8BC0","#145DA0","#0074B7","#316389"]
    wedges, texts, autotexts = ax.pie(data, autopct=lambda pct: func(pct, data),textprops=dict(color="w"),colors=colours)

    ax.legend(wedges, languages,
            title="Languages",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=12, weight="bold")

    ax.set_title("x5gon Languages")

    plt.show()
    

conn = connect(param_dic)
data =postgresql_to_data(conn)
piechart(data)

