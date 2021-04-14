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

basic_table_name_organizers = today + "_" + current_time + "_" + 'portal_targowy_organizers'
sql_table_creation = "CREATE TABLE " + basic_table_name_organizers + " (organizer_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, organizer_full_name VARCHAR(255), organizer_address VARCHAR(255), organizer_www VARCHAR(255), organizer_telephone int, organizer_email VARCHAR(255), organizer_page_url VARCHAR(255)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_organizers = "INSERT INTO " + basic_table_name_organizers + " (organizer_id, organizer_full_name, organizer_address, organizer_www, organizer_telephone, organizer_email, organizer_page_url) VALUES (%s, %s, %s, %s, %s, %s, %s)"

basic_table_name_categories = today + "_" + current_time + "_" + 'portal_targowy_categories'
sql_table_creation = "CREATE TABLE " + basic_table_name_categories + " (category_id int NOT NULL PRIMARY KEY, category_name VARCHAR(255)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_categories = "INSERT INTO " + basic_table_name_categories + " (category_id, category_name) VALUES (%s, %s)"

basic_table_name_offers_data = today + "_" + current_time + "_" + 'portal_targowy_offers_data'
sql_table_creation = "CREATE TABLE " + basic_table_name_offers_data + " (offer_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255), trade_portaltargowy_site VARCHAR(255), trade_fair VARCHAR(255), announce_date_valid VARCHAR(255), announce_type VARCHAR(255), description MEDIUMTEXT, exhibitor_name VARCHAR(255), exhibitor_address VARCHAR(255), exhibitor_www VARCHAR(255), exhibitor_telephone int, exhibitor_email VARCHAR(255), category_id int, FOREIGN KEY (category_id) REFERENCES " + basic_table_name_categories + "(category_id)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_offers_data = "INSERT INTO " + basic_table_name_offers_data + " (offer_id, name, trade_portaltargowy_site, trade_fair, announce_date_valid, announce_type, description, exhibitor_name, exhibitor_address, exhibitor_www, exhibitor_telephone, exhibitor_email, category_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

basic_table_name_exhibitors = today + "_" + current_time + "_" + 'portal_targowy_exhibitors'
sql_table_creation = "CREATE TABLE " + basic_table_name_exhibitors + " (exhibitor_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, exhibitor_full_name VARCHAR(255), exhibitor_address VARCHAR(255), exhibitor_www VARCHAR(255), exhibitor_telephone int, exhibitor_email VARCHAR(255), exhibitor_logo VARCHAR(255)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_exhibitors = "INSERT INTO " + basic_table_name_exhibitors + " (exhibitor_id, exhibitor_full_name, exhibitor_address, exhibitor_www, exhibitor_telephone, exhibitor_email, exhibitor_logo) VALUES (%s, %s, %s, %s, %s, %s, %s)"

basic_table_name_cat_j_exh = today + "_" + current_time + "_" + 'portal_targowy_cat_j_exh'
sql_table_creation = "CREATE TABLE " + basic_table_name_cat_j_exh + " (category_id int NOT NULL, FOREIGN KEY (category_id) REFERENCES " + basic_table_name_categories + "(category_id), exhibitor_id int NOT NULL, FOREIGN KEY (exhibitor_id) REFERENCES " + basic_table_name_exhibitors + "(exhibitor_id)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_cat_j_exh = "INSERT INTO " + basic_table_name_cat_j_exh + " (category_id, exhibitor_id) VALUES (%s, %s)"

basic_table_name_events = today + "_" + current_time + "_" + 'portal_targowy_events'
sql_table_creation = "CREATE TABLE " + basic_table_name_events + " (event_id int NOT NULL AUTO_INCREMENT PRIMARY KEY, event_full_name VARCHAR(255), event_logo VARCHAR(255), event_date VARCHAR(255), event_localization VARCHAR(255), event_www VARCHAR(255), event_description MEDIUMTEXT, organizer_id int, FOREIGN KEY (organizer_id) REFERENCES " + basic_table_name_organizers + "(organizer_id)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_events = "INSERT INTO " + basic_table_name_events + " (event_id, event_full_name, event_logo, event_date, event_localization, event_www, event_description, organizer_id) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"

basic_table_name_cat_j_ev = today + "_" + current_time + "_" + 'portal_targowy_cat_j_ev'
sql_table_creation = "CREATE TABLE " + basic_table_name_cat_j_ev + " (category_id int NOT NULL, FOREIGN KEY (category_id) REFERENCES " + basic_table_name_categories + "(category_id), event_id int NOT NULL, FOREIGN KEY (event_id) REFERENCES " + basic_table_name_events + "(event_id)) COLLATE=utf8_general_ci"
mycursor.execute(sql_table_creation)
sqlFormula_cat_j_ev = "INSERT INTO " + basic_table_name_cat_j_ev + " (category_id, event_id) VALUES (%s, %s)"

page_number = 1
organizer_full_name = None
organizer_address = None
organizer_www = None
organizer_telephone = None
organizer_email = None
organizer_id = 1
while True:
    organizer_page_url = 'https://portaltargowy.pl/organizatorzy?page=' + str(page_number)
    print("organizer page number: " + str(page_number))
    organizer_page_req = urllib.request.Request(organizer_page_url, headers={'User-Agent': "Mozilla/5.0"})
    organizer_page = urllib.request.urlopen(organizer_page_req)
    organizer_page_html = organizer_page.read()
    organizer_page.close()
    organizer_page_soup = BeautifulSoup(organizer_page_html, "html.parser")
    organizer_list = organizer_page_soup.findAll("div", {"class": "ccol-lg-8 col-md-6 mt-2"})
    if not organizer_list:
        break
    for row in organizer_list:
        organizer_page_url = row.a["href"]
        organizer_page_req = urllib.request.Request(organizer_page_url, headers={'User-Agent': "Mozilla/5.0"})
        organizer_page = urllib.request.urlopen(organizer_page_req)
        organizer_page_html = organizer_page.read()
        organizer_page.close()
        organizer_page_soup = BeautifulSoup(organizer_page_html, "html.parser")
        organizer_list = organizer_page_soup.select('#organizer .col-md-8')
        organizer_list = organizer_list[0].text.split('\n')
        for y in range(5):
            # print(x)
            try:
                if organizer_list[y + 1].strip().startswith('Pełna nazwa'):
                    organizer_full_name = organizer_list[y + 1].strip()
                    organizer_full_name = organizer_full_name.replace('Pełna nazwa: ', '')
            except IndexError:
                continue
            try:
                if organizer_list[y + 1].strip().startswith('Adres'):
                    organizer_address = organizer_list[y + 1].strip()
                    organizer_address = organizer_address.replace('Adres: ', '')
            except IndexError:
                continue
            try:
                if organizer_list[y + 1].strip().startswith('WWW'):
                    organizer_www = organizer_list[y + 1].strip()
                    organizer_www = organizer_www.replace('WWW: ', '')
            except IndexError:
                continue
            try:
                if organizer_list[y + 1].strip().startswith('Telefon'):
                    organizer_telephone = organizer_list[y + 1].strip()
                    organizer_telephone = organizer_telephone.replace('Telefon: ', '')
            except IndexError:
                continue
            try:
                if organizer_list[y + 1].strip().startswith('E-mail'):
                    organizer_email = organizer_list[y + 1].strip()
                    organizer_email = organizer_email.replace('E-mail: ', '')
            except IndexError:
                continue
        print(organizer_full_name)
        print(organizer_address)
        print(organizer_www)
        print(organizer_telephone)
        print(organizer_email)
        sql_data_organizers = (organizer_id, organizer_full_name, organizer_address, organizer_www, organizer_telephone, organizer_email, organizer_page_url)
        # print(sql_data_organizer)
        mycursor.execute(sqlFormula_organizers, sql_data_organizers)
        organizer_full_name = None
        organizer_address = None
        organizer_www = None
        organizer_telephone = None
        organizer_email = None
        print("organizer nr: " + str(organizer_id))
        organizer_id = organizer_id + 1
    page_number = page_number + 1
event_id = 1
offer_id = 1
exhibitor_id = 1
exhibitor_full_name = None
exhibitor_address = None
exhibitor_www = None
exhibitor_telephone = None
exhibitor_email = None
exhibitor_full_name_mysql = None
exhibitor_address_mysql = None
# x to liczba kategorii, należy wprowadzić ręcznie w kodzie
for x in range(17):
    category_id = x + 1
    offers_page_url = 'https://portaltargowy.pl/wyniki-wyszukiwania?q=&category=' + str(category_id)
    offers_page_req = urllib.request.Request(offers_page_url, headers={'User-Agent': "Mozilla/5.0"})
    offers_page = urllib.request.urlopen(offers_page_req)
    offers_page_html = offers_page.read()
    offers_page.close()
    offers_page_soup = BeautifulSoup(offers_page_html, "html.parser")
    category_name = offers_page_soup.select('small')
    category_name = category_name[0].text.strip()
    category_name = category_name.replace('Wyniki wyszukiwania dla frazy: \"\"\n                    w kategorii: \"', '')
    category_name = category_name[:-1]
    sql_data_categories = (category_id, category_name)
    mycursor.execute(sqlFormula_categories, sql_data_categories)
    promo_list1 = offers_page_soup.find("div", {"id": "offers"})
    try:
        promo_list2 = promo_list1.findAll("div", {"class": "col-md-6 mt-2"})
    except AttributeError:
        continue
    for row in promo_list2:
        offers_page_url2 = row.a["href"]
        offers_page_req2 = urllib.request.Request(offers_page_url2, headers={'User-Agent': "Mozilla/5.0"})
        offers_page2 = urllib.request.urlopen(offers_page_req2)
        offers_page_html2 = offers_page2.read()
        offers_page2.close()
        offers_page_soup2 = BeautifulSoup(offers_page_html2, "html.parser")
        name = offers_page_soup2.find("h1", {"class": "line-after"}).text
        text_right = offers_page_soup2.select('.col-md-12 .text-right')
        trade_portaltargowy_site = text_right[0].a["href"]
        text_right = text_right[0].text
        # print(text_right[0].text.strip())
        text_right = text_right.split("|")
        trade_fair = text_right[0].strip()
        trade_fair = trade_fair.replace('Targi: ', '')
        announce_date_valid = text_right[1]
        announce_date_valid = announce_date_valid.replace('Ogłoszenie ważne\n        ', '').strip()
        announce_type = text_right[2].strip()
        description = offers_page_soup2.select('.col-md-12 .col-md-12')
        description = description[0].text.strip()
        description = description.replace('Opis ogłoszenia:\n', '')
        exhibitor_data1 = offers_page_soup2.select('br+ .row .col-md-12')
        exhibitor_data1 = exhibitor_data1[0].text.strip()
        if exhibitor_data1 == "Galeria ogłoszenia:":
            exhibitor_data2 = offers_page_soup2.select('.col-md-12 .col-md-8')
            try:
                exhibitor_data2 = exhibitor_data2[0].text.strip()
            except IndexError:
                exhibitor_data3 = offers_page_soup2.select('.row:nth-child(9) .col-md-12')
                exhibitor_data3 = exhibitor_data3[0].text.strip()
                exhibitor_data3 = exhibitor_data3.split("\n")
                exhibitor_name = exhibitor_data3[1].strip()
                # print(exhibitor_name)
                exhibitor_address = exhibitor_data3[3].strip() + exhibitor_data3[4].strip()
                exhibitor_address = exhibitor_address.replace('Adres: ', '')
                # print(exhibitor_address)
                exhibitor_www = exhibitor_data3[5].strip()
                exhibitor_www = exhibitor_www.replace('WWW: ', '')
                # print(exhibitor_www)
                exhibitor_telephone = exhibitor_data3[-1].strip()
                if exhibitor_telephone.startswith("WWW"):
                    exhibitor_telephone = None
                # print(exhibitor_telephone)
                exhibitor_email = None
            else:
                exhibitor_data2 = exhibitor_data2.split("\n")
                exhibitor_name = exhibitor_data2[2].strip()
                # print(exhibitor_name)
                exhibitor_address = exhibitor_data2[5].strip()
                exhibitor_address = exhibitor_address.replace('Adres: ', '')
                # print(exhibitor_address)
                exhibitor_www = exhibitor_data2[7].strip()
                exhibitor_www = exhibitor_www.replace('WWW: ', '')
                # print(exhibitor_www)
                exhibitor_telephone = exhibitor_data2[8].strip()
                # print(exhibitor_telephone)
                exhibitor_email = exhibitor_data2[10].strip()
                exhibitor_email = exhibitor_email.replace('E-mail: ', '')
                # print(exhibitor_email)
        else:
            exhibitor_data1 = exhibitor_data1.split("\n")
            exhibitor_name = exhibitor_data1[1].strip()
            # print(exhibitor_name)
            exhibitor_address = exhibitor_data1[3].strip() + exhibitor_data1[4].strip()
            exhibitor_address = exhibitor_address.replace('Adres: ', '')
            # print(exhibitor_address)
            exhibitor_www = exhibitor_data1[5].strip()
            exhibitor_www = exhibitor_www.replace('WWW: ', '')
            # print(exhibitor_www)
            exhibitor_telephone = exhibitor_data1[-1].strip()
            exhibitor_telephone = exhibitor_telephone.replace('Telefon: ', '')
            if exhibitor_telephone.startswith("WWW"):
                exhibitor_telephone = None
            # print(exhibitor_telephone)
            exhibitor_email = None
        sql_data_offers_data = (offer_id, name, trade_portaltargowy_site, trade_fair, announce_date_valid, announce_type, description, exhibitor_name, exhibitor_address, exhibitor_www, exhibitor_telephone, exhibitor_email, category_id)
        mycursor.execute(sqlFormula_offers_data, sql_data_offers_data)
        offer_id = offer_id + 1
    page_number = 1
    while True:
        print("category number " + str(x + 1))
        print("page number " + str(page_number))
        exhibitor_page_url = 'https://portaltargowy.pl/wystawcy?category=' + str(x + 1) + '&page=' + str(page_number)
        exhibitor_page_req = urllib.request.Request(exhibitor_page_url, headers={'User-Agent': "Mozilla/5.0"})
        exhibitor_page = urllib.request.urlopen(exhibitor_page_req)
        exhibitor_page_html = exhibitor_page.read()
        exhibitor_page.close()
        exhibitor_page_soup = BeautifulSoup(exhibitor_page_html, "html.parser")
        exhibitor_list = exhibitor_page_soup.findAll("div", {"class": "col-lg-8 mt-2"})
        if not exhibitor_list:
            break
        for row in exhibitor_list:
            exhibitor_page_url = row.a["href"]
            exhibitor_page_req = urllib.request.Request(exhibitor_page_url, headers={'User-Agent': "Mozilla/5.0"})
            exhibitor_page = urllib.request.urlopen(exhibitor_page_req)
            exhibitor_page_html = exhibitor_page.read()
            exhibitor_page.close()
            exhibitor_page_soup = BeautifulSoup(exhibitor_page_html, "html.parser")
            exhibitor_data = exhibitor_page_soup.select('.col-md-8 .col-md-8')
            exhibitor_data = exhibitor_data[0].text.strip()
            exhibitor_data = exhibitor_data.split("\n")
            for y in range(4):
                try:
                    if exhibitor_data[y].strip().startswith('Pełna nazwa'):
                        exhibitor_full_name = exhibitor_data[y].strip()
                        exhibitor_full_name = exhibitor_full_name.replace('Pełna nazwa: ', '')
                        exhibitor_full_name_mysql = (exhibitor_full_name,)
                        print(exhibitor_full_name)
                except IndexError:
                    continue
                try:
                    if exhibitor_data[y].strip().startswith('Adres'):
                        exhibitor_address = exhibitor_data[y].strip()
                        exhibitor_address = exhibitor_address.replace('Adres: ', '')
                        exhibitor_address_mysql = (exhibitor_address,)
                        print(exhibitor_address)
                except IndexError:
                    continue
                try:
                    if exhibitor_data[y].strip().startswith('WWW'):
                        exhibitor_www = exhibitor_data[y].strip()
                        exhibitor_www = exhibitor_www.replace('WWW: ', '')
                        print(exhibitor_www)
                except IndexError:
                    continue
                try:
                    if exhibitor_data[y].strip().startswith('Telefon'):
                        exhibitor_telephone = exhibitor_data[y].strip()
                        exhibitor_telephone = exhibitor_telephone.replace('Telefon: ', '')
                        print(exhibitor_telephone)
                except IndexError:
                    continue
                try:
                    if exhibitor_data[y].strip().startswith('E-mail'):
                        exhibitor_email = exhibitor_data[y].strip()
                        exhibitor_email = exhibitor_email.replace('E-mail: ', '')
                        print(exhibitor_email)
                except IndexError:
                    continue
            exhibitor_logo = exhibitor_page_soup.select('.logo-exhibitor img')
            exhibitor_logo = exhibitor_logo[0]["src"]
            print(exhibitor_logo)
            select_exists_exhibitor_full_name_formula = "SELECT EXISTS(SELECT * from " + basic_table_name_exhibitors + " WHERE exhibitor_full_name = " + "%s" + ")"
            mycursor.execute(select_exists_exhibitor_full_name_formula, exhibitor_full_name_mysql)
            exists_exhibitor_full_name_condition = mycursor.fetchone()
            exists_exhibitor_full_name_condition = exists_exhibitor_full_name_condition[0]
            print("existence condition name: " + str(exists_exhibitor_full_name_condition))
            select_exists_exhibitor_address_formula = "SELECT EXISTS(SELECT * from " + basic_table_name_exhibitors + " WHERE exhibitor_address = " + "%s" + ")"
            mycursor.execute(select_exists_exhibitor_address_formula, exhibitor_address_mysql)
            exists_exhibitor_address_condition = mycursor.fetchone()
            exists_exhibitor_address_condition = exists_exhibitor_address_condition[0]
            print("existence condition address: " + str(exists_exhibitor_address_condition))
            if exists_exhibitor_full_name_condition and exists_exhibitor_address_condition:
                print("EXIST")
                select_existing_exhibitor_id_formula = "SELECT exhibitor_id FROM " + basic_table_name_exhibitors + " WHERE exhibitor_full_name = %s"
                mycursor.execute(select_existing_exhibitor_id_formula, exhibitor_full_name_mysql)
                existing_exhibitor_id = mycursor.fetchone()
                existing_exhibitor_id = existing_exhibitor_id[0]
                sql_data_cat_j_exh = (category_id, existing_exhibitor_id)
            else:
                print("NOT EXIST")
                sql_data_exhibitors = (exhibitor_id, exhibitor_full_name, exhibitor_address, exhibitor_www, exhibitor_telephone, exhibitor_email, exhibitor_logo)
                mycursor.execute(sqlFormula_exhibitors, sql_data_exhibitors)
                sql_data_cat_j_exh = (category_id, exhibitor_id)
            mycursor.execute(sqlFormula_cat_j_exh, sql_data_cat_j_exh)
            if not (exists_exhibitor_full_name_condition and exists_exhibitor_address_condition):
                exhibitor_id = exhibitor_id + 1
            exhibitor_full_name = None
            exhibitor_address = None
            exhibitor_www = None
            exhibitor_telephone = None
            exhibitor_email = None
            exhibitor_full_name_mysql = None
            exhibitor_address_mysql = None
        page_number = page_number + 1
    page_number = 1
    while True:
        print("category number " + str(x + 1))
        print("page number " + str(page_number))
        event_page_url = 'https://portaltargowy.pl/targi?category=' + str(category_id) + '&page=' + str(page_number)
        event_page_req = urllib.request.Request(event_page_url, headers={'User-Agent': "Mozilla/5.0"})
        event_page = urllib.request.urlopen(event_page_req)
        event_page_html = event_page.read()
        event_page.close()
        event_page_soup = BeautifulSoup(event_page_html, "html.parser")
        event_list = event_page_soup.findAll("div", {"class": "col-lg-8 col-md-6"})
        if not event_list:
            break
        for row in event_list:
            event_page_url = row.a["href"]
            event_page_req = urllib.request.Request(event_page_url, headers={'User-Agent': "Mozilla/5.0"})
            event_page = urllib.request.urlopen(event_page_req)
            event_page_html = event_page.read()
            event_page.close()
            event_page_soup = BeautifulSoup(event_page_html, "html.parser")
            event_full_name = event_page_soup.select('small')
            event_full_name = event_full_name[0].text
            event_full_name = event_full_name.replace('Pełna nazwa targów: ', '')
            event_full_name_mysql = (event_full_name,)
            print(event_full_name)
            event_logo = event_page_soup.select('.event-box-single img')
            event_logo = event_logo[0]["src"]
            print(event_logo)
            event_date = event_page_soup.select('.col-sm-6:nth-child(1)')
            event_date = event_date[0].text.strip()
            event_date = event_date.split("\n")
            event_date = event_date[1].strip() + " " + event_date[2].strip()
            print(event_date)
            event_localization = event_page_soup.select('.col-sm-6:nth-child(2)')
            event_localization = event_localization[0].text.strip()
            event_localization = event_localization.split("\n")
            event_localization = event_localization[1].strip()
            event_localization_mysql = (event_localization,)
            print(event_localization)
            event_www = event_page_soup.select('.col-sm-6 a')
            if not event_www:
                event_www = None
            else:
                event_www = event_www[0]["href"]
            print(event_www)
            event_description = event_page_soup.select('.row:nth-child(5) .col-lg-12')
            event_description = event_description[0].text
            event_description = event_description.split('\n', 2)[-1].strip()
            print(event_description)
            event_page_url = event_page_soup.find("div", {"class": "col-lg-8 col-sm-8 col-xs-12"})
            event_page_url = event_page_url.a["href"]
            event_page_url_mysql = (event_page_url,)
            select_formula = "SELECT organizer_id FROM " + basic_table_name_organizers + " WHERE organizer_page_url = %s"
            mycursor.execute(select_formula, event_page_url_mysql)
            organizer_id_event = mycursor.fetchone()
            organizer_id_event = organizer_id_event[0]
            print(organizer_id_event)
            select_exists_event_full_name_formula = "SELECT EXISTS(SELECT * from " + basic_table_name_events + " WHERE event_full_name = " + "%s" + ")"
            mycursor.execute(select_exists_event_full_name_formula, event_full_name_mysql)
            exists_event_full_name_condition = mycursor.fetchone()
            exists_event_full_name_condition = exists_event_full_name_condition[0]
            print("existence condition name: " + str(exists_event_full_name_condition))
            select_exists_event_localization_formula = "SELECT EXISTS(SELECT * from " + basic_table_name_events + " WHERE event_localization = " + "%s" + ")"
            mycursor.execute(select_exists_event_localization_formula, event_localization_mysql)
            exists_event_localization_condition = mycursor.fetchone()
            exists_event_localization_condition = exists_event_localization_condition[0]
            print("existence condition localization: " + str(exists_event_localization_condition))
            if exists_event_full_name_condition and exists_event_localization_condition:
                print("EXIST")
                select_existing_event_id_formula = "SELECT event_id FROM " + basic_table_name_events + " WHERE event_full_name = %s"
                mycursor.execute(select_existing_event_id_formula, event_full_name_mysql)
                existing_event_id = mycursor.fetchone()
                existing_event_id = existing_event_id[0]
                sql_data_cat_j_ev = (category_id, existing_event_id)
            else:
                print("NOT EXIST")
                sql_data_events = (event_id, event_full_name, event_logo, event_date, event_localization, event_www, event_description, organizer_id_event)
                mycursor.execute(sqlFormula_events, sql_data_events)
                sql_data_cat_j_ev = (category_id, event_id)
            mycursor.execute(sqlFormula_cat_j_ev, sql_data_cat_j_ev)
            if not (exists_event_full_name_condition and exists_event_localization_condition):
                event_id = event_id + 1
        page_number = page_number + 1
mydb.commit()
