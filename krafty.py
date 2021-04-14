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
table_name = today + "_" + current_time + "_" + 'polskikraft_data'
sql_table_creation = "CREATE TABLE " + table_name + " (beer_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, beer_name VARCHAR(255), beer_rating FLOAT(2), brewery_name VARCHAR(255), beer_style VARCHAR(255), beer_blg FLOAT(2), beer_alc FLOAT(2), beer_ibu FLOAT(2), beer_extra_ingredients MEDIUMTEXT, beer_description MEDIUMTEXT)"
mycursor.execute(sql_table_creation)

sqlFormula = "INSERT INTO " + table_name + " (beer_id, beer_name, beer_rating, brewery_name, beer_style, beer_blg, beer_alc, beer_ibu, beer_extra_ingredients, beer_description) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
beer_id = 1

page_url = 'https://www.polskikraft.pl/najlepsze'
page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
page = urllib.request.urlopen(page_req)
page_html = page.read()
page.close()
page_soup = BeautifulSoup(page_html, "html.parser")
scrapings = page_soup.find("div", {"class": "pk-infscroll"})
for link in scrapings.findAll('a'):
    if link != scrapings.findAll('a')[-1]:
        href_req = urllib.request.Request(link.get('href'), headers={'User-Agent': "Mozilla/5.0"})
        item_page = urllib.request.urlopen(href_req)
        item_page_html = item_page.read()
        item_page.close()
        item_page_soup = BeautifulSoup(item_page_html, "html.parser")
        item_rating = item_page_soup.find("span", {"itemprop": "ratingValue"})
        item_rating = item_rating.text
        print(item_rating)
        beer_name = item_page_soup.find("p", {"class": "beer-name"})
        beer_name = beer_name.text
        print(beer_name)
        brewery_name = item_page_soup.find("p", {"class": "brewery-name"})
        brewery_name = brewery_name.text
        print(brewery_name)
        style = item_page_soup.find("p", {"style": "font-size: 20px"})
        style = style.text.strip()
        print(style)
        blg = item_page_soup.find("h1", {"id": "amount-blg-b"})
        blg = blg.text
        if blg == "-":
            blg = None
        print(blg)
        alc = item_page_soup.find("h1", {"id": "amount-alc-s"})
        alc = alc.text
        if alc == "-":
            alc = None
        print(alc)
        ibu = item_page_soup.find("h1", {"id": "amount-ibu-b"})
        ibu = ibu.text
        if ibu == "-":
            ibu = None
        print(ibu)
        extra = item_page_soup.find("p", {"style": "font-size: 16px"})
        if extra is not None:
            extra = extra.text.strip()
        print(extra)
        description = item_page_soup.find("p", {"class": "description"})
        if len(description.text) == 1:
            description = None
        else:
            description = description.text.strip()
        print(description)
        sql_data = (beer_id, beer_name, item_rating, brewery_name, style, blg, alc, ibu, extra, description)
        mycursor.execute(sqlFormula, sql_data)
        print('mycursor execute')
        beer_id = beer_id + 1
site_number = 2
while site_number != 81:
    page_url = 'https://www.polskikraft.pl/najlepsze/' + str(site_number)
    page_req = urllib.request.Request(page_url, headers={'User-Agent': "Mozilla/5.0"})
    page = urllib.request.urlopen(page_req)
    page_html = page.read()
    page.close()
    page_soup = BeautifulSoup(page_html, "html.parser")
    scrapings = page_soup.findAll("div", {"class": "col-lg-2 col-md-3 col-sm-4 col-xs-6 pk-thumbnail"})
    for row in scrapings:
        href_req = urllib.request.Request(row.a["href"], headers={'User-Agent': "Mozilla/5.0"})
        item_page = urllib.request.urlopen(href_req)
        item_page_html = item_page.read()
        item_page.close()
        item_page_soup = BeautifulSoup(item_page_html, "html.parser")
        item_rating = item_page_soup.find("span", {"itemprop": "ratingValue"})
        item_rating = item_rating.text
        print(item_rating)
        beer_name = item_page_soup.find("p", {"class": "beer-name"})
        beer_name = beer_name.text
        print(beer_name)
        brewery_name = item_page_soup.find("p", {"class": "brewery-name"})
        brewery_name = brewery_name.text
        print(brewery_name)
        style = item_page_soup.find("p", {"style": "font-size: 20px"})
        style = style.text.strip()
        print(style)
        blg = item_page_soup.find("h1", {"id": "amount-blg-b"})
        blg = blg.text
        if blg == "-":
            blg = None
        print(blg)
        alc = item_page_soup.find("h1", {"id": "amount-alc-s"})
        alc = alc.text
        if alc == "-":
            alc = None
        print(alc)
        ibu = item_page_soup.find("h1", {"id": "amount-ibu-b"})
        ibu = ibu.text
        if ibu == "-":
            ibu = None
        print(ibu)
        extra = item_page_soup.find("p", {"style": "font-size: 16px"})
        if extra is not None:
            extra = extra.text.strip()
        print(extra)
        description = item_page_soup.find("p", {"class": "description"})
        if len(description.text) == 1:
            description = None
        else:
            description = description.text.strip()
        print(description)
        sql_data = (beer_id, beer_name, item_rating, brewery_name, style, blg, alc, ibu, extra, description)
        mycursor.execute(sqlFormula, sql_data)
        print('mycursor execute')
        beer_id = beer_id + 1
    site_number = site_number + 1
mydb.commit()
print('mydb commit')