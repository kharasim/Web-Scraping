from selenium import webdriver
import time
from datetime import date
from bs4 import BeautifulSoup
import urllib.request
import mysql.connector

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
table_name = today + "_" + current_time + "_" + 'grupa_mtp_data'
mycursor.execute("CREATE TABLE " + table_name + " (exhibitor_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, exhibitor_name VARCHAR(255), street_address VARCHAR(255), postal_code_and_city VARCHAR(255), country VARCHAR(255), telephone VARCHAR(255), pavilion int, booth int)")

sqlFormula = "INSERT INTO " + table_name + " (exhibitor_id, exhibitor_name, street_address, postal_code_and_city, country, telephone, pavilion, booth) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

url = "https://katalog.grupamtp.pl/pl/?ec=T411901&ec=T931901#!%3Fec=T171901"
driver = webdriver.Chrome()
driver.get(url)
html = driver.page_source.encode('utf-8')
page_num = 0
item_id = 1

while driver.find_elements_by_css_selector('.btn-align-center'):
    driver.find_element_by_css_selector('.btn-align-center').click()
    page_num += 1
    print("getting page number "+str(page_num))
    time.sleep(1)
    # ten patent z 'break' jest średni ale działa xD
    if page_num == 30:
        break

page_html = driver.page_source.encode('utf-8')
page_soup = BeautifulSoup(page_html, "html.parser")
scrapings = page_soup.find("div", {"class": "container ng-binding"})
exhibitor_id = 1
for link in scrapings.findAll('a'):
    if link != page_soup.findAll('a')[-1]:
        page_url = 'https://katalog.grupamtp.pl/' + link.get('href')
        print(page_url)
        page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
        page = urllib.request.urlopen(page_req)
        page_html2 = page.read()
        page.close()
        page_soup2 = BeautifulSoup(page_html2, "html.parser")
        exhibitor_name = page_soup2.find("div", {"class": "col-md-8 col-sm-8 col-xs-8"})
        exhibitor_name = exhibitor_name.p.text
        print(exhibitor_name)
        scrapings2 = page_soup2.find("div", {"class": "col-md-6 col-sm-12"})
        #print(scrapings2)
        tel = scrapings2.find("div", {"class": "col-md-4 col-sm-4 col-xs-6"})
        if tel is not None:
            tel = tel.find("p")
            tel = tel.text.replace("Telefon:", "")
            print(tel)
        else:
            tel = None
            print(tel)
        other_info = scrapings2.findAll("div", {"class": "col-md-4 col-sm-6 col-xs-12"})
        #print(len(other_info))
        lines = other_info[0].find("p")
        #print(lines)
        lines = lines.text.split('\n')
        try:
            street_address = lines[1].lstrip()
        except IndexError:
            street_address = None
        print(street_address)
        try:
            postal = lines[2].lstrip()
        except IndexError:
            postal = None
        print(postal)
        try:
            country = lines[3].lstrip()
        except IndexError:
            country = None
        print(country)
        try:
            pavilion = other_info[1].text
            pavilion = pavilion.replace('Pawilon: ', '')
            pavilion = pavilion.strip()
        except IndexError:
            pavilion = None
        print(pavilion)
        try:
            booth = other_info[2].text
            booth = booth.replace('Stoisko:', '')
            booth = booth.strip()
        except IndexError:
            booth = None
        print(booth)
        sql_data = (exhibitor_id, exhibitor_name, street_address, postal, country, tel, pavilion, booth)
        mycursor.execute(sqlFormula, sql_data)
        exhibitor_id = exhibitor_id + 1
mydb.commit()