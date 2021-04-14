import urllib.request
from bs4 import BeautifulSoup
import re
import mysql.connector
import time
from datetime import date
from selenium import webdriver

mydb = mysql.connector.connect(
    host="xxx",
    user="xxx",
    password="xxx",
    database="xxx"

)

mycursor = mydb.cursor(buffered=True)

t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
today = str(date.today())
today = today.replace("-", "_")
categories_table_name = today + "_" + current_time + "_" + 'categories_worldfood_lentreg_2019_data'
sql_table_creation = "CREATE TABLE " + categories_table_name + " (category_id int NOT NULL PRIMARY KEY, category_name VARCHAR(255))"
mycursor.execute(sql_table_creation)
sqlFormula = "INSERT INTO " + categories_table_name + " (category_id, category_name) VALUES (%s, %s)"

page_url = 'https://worldfood.lentreg.pl/katalog-online-2019/'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
categories = page_soup.findAll('label', {'for': re.compile(r'id_kat_')})
categories_list = []
for row in categories:
    site_category_index = row.input["value"]
    site_category_index = site_category_index.replace('.c', '')
    category_name = row.text.strip()
    categories_list.append((site_category_index, category_name))
#print(categories_list)
#mycursor.executemany(sqlFormula, categories_list)
#mydb.commit()

driver = webdriver.Chrome()
driver.get(page_url)
page_html_selenium = driver.page_source.encode('utf-8')
page_soup_selenium = BeautifulSoup(page_html_selenium, "html.parser")

exhibitor_data = page_soup.findAll('div', {'class': re.compile(r'ko-item\sko-closed\s+ko-iswpis')})
for row in exhibitor_data:
    exhibitor_name = row.find("div", {"class": "ko-nazwa-firmy"})
    #print(exhibitor_name.text)
    exhibitor_booth_number = row.find("h3", {"class": "short-info-numer"})
    exhibitor_booth_number = exhibitor_booth_number.text.replace("Numer stoiska: ", "")
    #print(exhibitor_booth_number)
    exhibitor_description = row.findAll("p")
    exhibitor_description_pl = exhibitor_description[0].text.strip()
    #print(exhibitor_description_pl)
    exhibitor_description_eng = exhibitor_description[1].text.strip()
    #print(exhibitor_description_eng)
    exhibitor_description_nwm = exhibitor_description[2].text.strip()
    #print(exhibitor_description_nwm)
    exhibitor_categories = row.find("ul", {"class": "kategorie-produktowe"})
    #print(exhibitor_categories.text)
    li_categories = exhibitor_categories.findAll("li")
    #for row_li in li_categories:
        #print(row_li.text)
        #print(categories_list[4][1])
        #for i in range(len(categories_list)):
            #if categories_list[i][1] == row_li.text:
                #print(categories_list[i][0])
    exhibitor_description = row.findAll("p")
    exhibitor_adress = exhibitor_description[3].text.strip()
    print(exhibitor_adress)

