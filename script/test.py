from time import sleep
import requests, csv, json, os
import pandas as pd
import mysql.connector


repolinks = ["julianbruegger/Hochwasser", "schufeli/reddit-random-service", "answerdev/answer"]
URL= "https://api.codetabs.com/v1/loc?github="
fileignore = "LICENSE,.gitignore,.dockerignore"

totallines = 0

mydb = mysql.connector.connect(
    host="192.168.111.61", 
    user="root",
    password="123ict",
    database="hackathon")
mycursor = mydb.cursor()

def filterjson(file, arraynr):

    with open(file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=' ')
        data = list(csv_reader)[-1][-1]
        print(data)

        dataarray = data.split(",");
        dataarray = dataarray[-1]
        return dataarray

def sql(table, total):

    sql = "INSERT INTO " + table + " (datetime, total, tmp) VALUES (now(), %s, %s)"
    print(sql)
    val = (total, total)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("iz working")

def sql2(table, total):

    sql = "INSERT INTO " + "test" + " (datetime, total, tmp) VALUES (now(), %s, %s)"
    print(sql)
    val = (total, table)
    mycursor.execute(sql, val)
    mydb.commit()
    #print("iz working")


for x in repolinks:
    print (x)
    request_url = URL + x + "&ignored=" + fileignore
    filename = x.replace("/","")
    filename = filename.replace("-","")
    file_csv = filename +".csv"
    file_json = filename + ".json"  
    print(request_url)
    r = requests.get(request_url)
    data = r.json()

    print(data)

    json_object = json.dumps(data, indent=4)
 
    # Writing to sample.json
    with open(file_json, "w") as outfile:
        outfile.write(json_object)

    with open(file_json, encoding='utf-8') as inputfile:
        df = pd.read_json(inputfile)

    df.to_csv("tmpfile.csv", encoding='utf-8', index=False)

    
    linesofcode = (filterjson("tmpfile.csv", 1))
    linesofcode = int(linesofcode)
    sql2(filename, linesofcode)

    totallines = totallines + linesofcode

    sleep(10)

sql("total", totallines)


