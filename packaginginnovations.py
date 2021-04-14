import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import time
from datetime import date
from googlesearch import search

mydb = mysql.connector.connect(
    host="xxx",
    user="xxx",
    password="xxx",
    database="xxx"

)
mycursor = mydb.cursor()

t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
today = str(date.today())
today = today.replace("-", "_")
table_name = today + "_" + current_time + "_" + 'packaginginnovations_data'
sql_table_creation = "CREATE TABLE " + table_name + " (company_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, company_name VARCHAR(255), stand_number VARCHAR(255), result1 VARCHAR(255), result2 VARCHAR(255), result3 VARCHAR(255), result4 VARCHAR(255), result5 VARCHAR(255))"
mycursor.execute(sql_table_creation)

sqlFormula = "INSERT INTO " + table_name + " (company_id, company_name, stand_number, result1, result2, result3, result4, result5) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

page_url = 'https://www.packaginginnovations.pl/pl/dla-odwiedzajacych/lista-wystawcow.html'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
scrapings = page_soup.find("tbody")
company_id = 1
for row in scrapings:
    sql_data = []
    sql_data.append(company_id)
    company_name = row.td.text
    sql_data.append(company_name)
    stand_number = row.td.next_sibling.text
    sql_data.append(stand_number)
    for j in search(company_name, tld="pl", lang='pl', num=5, stop=5, pause=2):
        sql_data.append(j)
    mycursor.execute(sqlFormula, sql_data)
    company_id = company_id + 1
mydb.commit()