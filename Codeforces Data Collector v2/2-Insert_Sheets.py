# import os
# import time
import sqlite3            
# import datetime
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver import ChromeOptions
# from selenium.webdriver.common.keys import Keys
# from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# from Telegram_Bot import *

# Chrome settings & options to hide the browser
options = ChromeOptions()
warnings.filterwarnings("ignore", category = DeprecationWarning)
# options.add_argument("--no-sandbox")
# options.add_argument("--disable-dev-shm-usage")
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

# Database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

insert = "insert or ignore into sheets (link, name, num) values(?,?,?)"

fi = open('sheets.txt', 'r')
for line in fi:
    if line[0] == '*':
        continue
    driver.get(line)
    soup = BeautifulSoup(driver.page_source, 'lxml')
    sheetName = soup.find_all('table', class_ = "rtable")[-1].find('a').text
    problems = soup.find('table', class_ = "problems").find_all('tr')
    print(f"\n- {sheetName}  -  {len(problems) - 1}")
    sheet = f"""CREATE TABLE IF NOT EXISTS "{sheetName}" (
        "handle" TEXT,
        "Pname"	TEXT,
        PRIMARY KEY("handle","Pname"),
        FOREIGN KEY("handle") REFERENCES "contestants"("handle"),
        FOREIGN KEY("Pname") REFERENCES "problems"("name")
    );"""
    cursor.execute(sheet)
    cursor.execute(insert, (line.rstrip(), sheetName, len(problems) - 1, ))

conn.commit()
print("sheets added successfully :)")
fi.close()
driver.quit()