import urllib.request
from bs4 import BeautifulSoup
import mysql.connector
import time
from datetime import date

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
table_name = today + "_" + current_time + "_" + 'innoform_data'
sql_table_creation = "CREATE TABLE " + table_name + " (company_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, company_name VARCHAR(255), country VARCHAR(255), booth_number int)"
mycursor.execute(sql_table_creation)

sqlFormula = "INSERT INTO " + table_name + " (company_id, company_name, country, booth_number) VALUES (%s, %s, %s, %s)"

page_url = 'https://www.innoform.pl/pl/dla-zwiedzajacych/lista-wystawcow.html'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
tbody = page_soup.tbody
trlist = tbody.findAll("tr")
company_id = 1
for row in trlist[1:]:
    tdlist = row.findAll("td")
    company_name = tdlist[0].text
    country = tdlist[1].text
    booth_number = tdlist[2].text
    sql_data = (company_id, company_name, country, booth_number)
    mycursor.execute(sqlFormula, sql_data)
    company_id = company_id + 1
mydb.commit()