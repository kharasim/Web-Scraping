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

mycursor = mydb.cursor(buffered=True)

t = time.localtime()
current_time = time.strftime("%H_%M_%S", t)
today = str(date.today())
today = today.replace("-", "_")
basic_table_name = today + "_" + current_time + "_" + 'braubeviale_basic_data'
sql_table_creation = "CREATE TABLE " + basic_table_name + " (supplier_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), braubeviale_site VARCHAR(255), icon VARCHAR(255), braubeviale_id INT)"
mycursor.execute(sql_table_creation)

sqlFormula = "INSERT INTO " + basic_table_name + " (supplier_id, name, braubeviale_site, icon, braubeviale_id) VALUES (%s, %s, %s, %s, %s)"

page_url = 'https://www.braubeviale.de/de/ausstellerprodukte/exhibitorlist?zip=&catids=&halls=&countries=&edbid=&filterchar=&items=2000&search=&tab=1'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
scrapings = page_soup.findAll("div", {"class": "rcEntry"})
id = 1
for row in scrapings:
    eimage = row.find("div", {"class": "eImage"})
    eposition = row.find("div", {"class": "ePosition"})
    name = eimage.a["title"]
    braubeviale_site = "https://www.braubeviale.de" + eimage.a["href"]
    icon = eimage.a.img["data-original"]
    braubevialeid = eposition.a["data-exhibitor"]
    sql_data = (id, name, braubeviale_site, icon, braubevialeid)
    mycursor.execute(sqlFormula, sql_data)
    id = id + 1
mydb.commit()

site_table_name = today + "_" + current_time + "_" + 'braubeviale_site_data'
sql_table_creation = "CREATE TABLE " + site_table_name + " (supplier_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, FOREIGN KEY (supplier_id) REFERENCES suppliers_basic_data(supplier_id), street_address VARCHAR(255), postal_code VARCHAR(255), address_locality VARCHAR(255), address_country VARCHAR(255), supplier_site VARCHAR(255), telephone VARCHAR(255), fax VARCHAR(255), land VARCHAR(255))"
mycursor.execute(sql_table_creation)
sqlFormula = "INSERT INTO " + site_table_name + " (supplier_id, street_address, postal_code, address_locality, address_country, supplier_site, telephone, fax, land) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"

select_formula = "SELECT braubeviale_site FROM " + basic_table_name
mycursor.execute(select_formula)
braubeviale_site_column = mycursor.fetchall()
supplier_id = 1
for row in braubeviale_site_column:
    page_url = row[0]
    page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
    page = urllib.request.urlopen(page_req)
    page_html = page.read()
    page.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    left = page_soup.findAll("div", {"class": "rText__col--left"})
    street_address = left[0].find("span", itemprop="streetAddress")
    if street_address is not None:
        street_address = street_address.text
    postal_code = left[0].find("span", itemprop="postalCode")
    if postal_code is not None:
        postal_code = postal_code.text
    address_locality = left[0].find("span", itemprop="addressLocality")
    if address_locality is not None:
        address_locality = address_locality.text
    address_country = left[0].find("span", itemprop="addressCountry")
    if address_country is not None:
        address_country = address_country.text
    supplier_site = left[1].find("a", {"class": "bold"})
    if supplier_site is not None:
        supplier_site = supplier_site["href"]
    right = page_soup.find("div", {"class": "rText__col--right"})
    telephone = right.find("span", itemprop="telephone")
    if telephone is not None:
        telephone = telephone.text
    fax = right.find("span", itemprop="faxNumber")
    if fax is not None:
        fax = fax.text
    land = None
    if address_country == "Deutschland":
        spans = left[0].findAll("span")
        land = spans[3].text
        if land != "Deutschland":
            land = land[1:]
    if street_address is None and postal_code is None and address_locality is None and address_country is None:
        adapt = page_soup.find("div", {"class": "rText__col--left"})
        adapt = adapt.findAll("span")
        street_address = adapt[1].text
        postal_code = adapt[0].text
        address_locality = adapt[2].text
    sql_data = (supplier_id, street_address, postal_code, address_locality, address_country, supplier_site, telephone, fax, land)
    mycursor.execute(sqlFormula, sql_data)
    supplier_id = supplier_id + 1
mydb.commit()