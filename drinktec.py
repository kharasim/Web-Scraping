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
table_name = today + "_" + current_time + "_" + 'drinktec_data'
mycursor.execute("CREATE TABLE " + table_name + " (id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), street VARCHAR(255), postal_code_and_city VARCHAR(255), country VARCHAR(255), telephone VARCHAR(255), fax VARCHAR(255), website VARCHAR(255)) COLLATE=utf8_general_ci")

sqlFormula = "INSERT INTO " + table_name + " (id, name, street, postal_code_and_city, country, telephone, fax, website) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"


page_url = 'https://exhibitors.drinktec.com/en/exhibitor-details/exhibitors-brand-names/letter/all/'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
href_list = page_soup.findAll("div", {"class": "treffer-titel w-100"})
e_id = 1
for row in href_list:
    page_req_href = urllib.request.Request(row.a["href"], headers={'User-Agent': "Mozilla/5.0"})
    page_href = urllib.request.urlopen(page_req_href)
    page_html_href = page_href.read()
    page_href.close()
    page_soup_href = BeautifulSoup(page_html_href, "html.parser")
    address = page_soup_href.select('#details p')
    address = address[0].text.split('\n')
    name = page_soup_href.select('h1')[1].text
    name_mysql = (name,)
    select_exists_name_formula = "SELECT EXISTS(SELECT * from " + table_name + " WHERE name = " + "%s" + ")"
    mycursor.execute(select_exists_name_formula, name_mysql)
    exists_name_condition = mycursor.fetchone()
    exists_name_condition = exists_name_condition[0]
    if exists_name_condition:
        continue
    print(name)
    street = address[1].strip()
    postal_code = address[2].strip()
    country = address[3].strip()
    contact = page_soup_href.select('.exhibitordetails-contactinfo-list div')
    phone = None
    fax = None
    website = None
    for x in range(3):
        try:
            if contact[x*2].text.strip().startswith('Phone'):
                phone = contact[(x*2) + 1].text.strip()
            if contact[x*2].text.strip().startswith('Fax'):
                fax = contact[(x*2) + 1].text.strip()
            if contact[x*2].text.strip().startswith('Website'):
                website = contact[(x*2) + 1].text.strip()
        except IndexError:
            continue
    sql_data = (e_id, name, street, postal_code, country, phone, fax, website)
    mycursor.execute(sqlFormula, sql_data)
    e_id = e_id + 1
x = 4
break_while = False
while True:
    if break_while:
        break
    page_url2 = 'https://exhibitors.drinktec.com/index.php?L=1&fair_id=1459&eID=pt&request%5Baction%5D=defaultList&request%5Barguments%5D%5Bparams%5D%5BinitializeWithEmptyQuery%5D=1&request%5Barguments%5D%5Bparams%5D%5Bstatsrch%5D%5Baussteller_buchstfilter%5D=all&request%5Barguments%5D%5Bparams%5D%5Bstatsrch%5D%5Baussteller_offset%5D=0&request%5Barguments%5D%5Bparams%5D%5Bstatsrch%5D%5Baussteller_orderby%5D=ASC&request%5Barguments%5D%5Bparams%5D%5Bstatsrch%5D%5Baussteller_sortby%5D=_title&request%5Barguments%5D%5Bparams%5D%5Bxoffset%5D=' + str(x) + '0&request%5Barguments%5D%5Bparams%5D%5Bappend%5D=1&request%5BpluginName%5D=Exhibitors&request%5Bcontroller%5D=Exhibitors'
    page_req2 = urllib.request.Request(page_url2, headers={'User-Agent': "Mozilla/5.0"})
    page2 = urllib.request.urlopen(page_req2)
    page_html2 = page2.read()
    page2.close()
    page_soup2 = BeautifulSoup(page_html2, "html.parser")
    href_list2 = page_soup2.findAll("div", {"class": "treffer-titel w-100"})
    for row in href_list2:
        page_req_href = urllib.request.Request(row.a["href"], headers={'User-Agent': "Mozilla/5.0"})
        page_href = urllib.request.urlopen(page_req_href)
        page_html_href = page_href.read()
        page_href.close()
        page_soup_href = BeautifulSoup(page_html_href, "html.parser")
        address = page_soup_href.select('#details p')
        address = address[0].text.split('\n')
        name = page_soup_href.select('h1')[1].text
        name_mysql = (name,)
        select_exists_name_formula = "SELECT EXISTS(SELECT * from " + table_name + " WHERE name = " + "%s" + ")"
        mycursor.execute(select_exists_name_formula, name_mysql)
        exists_name_condition = mycursor.fetchone()
        exists_name_condition = exists_name_condition[0]
        if exists_name_condition:
            continue
        print(name)
        street = address[1].strip()
        postal_code = address[2].strip()
        country = address[3].strip()
        contact = page_soup_href.select('.exhibitordetails-contactinfo-list div')
        phone = None
        fax = None
        website = None
        for y in range(3):
            try:
                if contact[y * 2].text.strip().startswith('Phone'):
                    phone = contact[(y * 2) + 1].text.strip()
                if contact[y * 2].text.strip().startswith('Fax'):
                    fax = contact[(y * 2) + 1].text.strip()
                if contact[y * 2].text.strip().startswith('Website'):
                    website = contact[(y * 2) + 1].text.strip()
            except IndexError:
                continue
        sql_data = (e_id, name, street, postal_code, country, phone, fax, website)
        mycursor.execute(sqlFormula, sql_data)
        e_id = e_id + 1
        #trzeba sprawdzać ostatni href
        if row.a["href"] == "https://exhibitors.drinktec.com/?id=29&L=1&tx_nfmedb_exhibitors%5Bparams%5D%5BobjId%5D=1060963&tx_nfmedb_exhibitors%5Baction%5D=detail&tx_nfmedb_exhibitors%5Bcontroller%5D=Exhibitors&cHash=a7c04ff2c03abbc2e05b543f8f0d5025":
            break_while = True
    x = x + 2
mydb.commit()
