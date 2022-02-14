from operator import imod
import os
import sqlite3            
import datetime
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.keys import Keys
from Telegram_Bot import *

# Chrome settings & options to hide the browser
options = ChromeOptions()
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
driver = Chrome(executable_path = os.getcwd() + '\chromedriver', options = options)

# Database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get all Sheets to iterate over its problem
get = "select * from sheets"
sheets = cursor.execute(get).fetchall()

# Get all contestants to get their aceepted soultions
get = "select * from contestants"
contestants = cursor.execute(get).fetchall()

# To insert accepted solutions
ac = "insert or ignore into solved (handle, Pname) values(?,?)"
his = "insert or ignore into history (handle, Pname) values(?,?)"

# To change date format
months = ['Jan-01', 'Feb-02', 'Mar-03', 'Apr-04', 'May-05', 'Jun-06', 'Jul-07', 'Aug-08', 'Sep-09', 'Oct-10', 'Nov-11', 'Dec-12']
def dateFormat(curTime):
    for month in months:
        curTime = curTime.replace(month[:3], month[4:6])
    return curTime

# To get Accepted solutions and save it in Database
def getSolutions(table, lastSubmit):
    idx = 0 #2000-08-13 13:08:00
    lastSubmit = datetime.datetime(int(lastSubmit[0:4]), int(lastSubmit[5:7]), int(lastSubmit[8:10]), int(lastSubmit[11:13]), int(lastSubmit[14:16]))
    ret = lastSubmit
    for td in table:
        if len(td.text):
            txt = td.text.replace('\n','').strip()
            if idx == 1:
                txt = txt[:-5]
                date = dateFormat(txt)
            elif idx == 2:
                handel = txt
            elif idx == 3:
                problem = txt
            elif idx == 5: #08/13/2000 13:08 
                verdict = txt
                date = datetime.datetime(int(date[6:10]), int(date[0:2]), int(date[3:5]), int(date[11:13]), int(date[14:16]))
                if lastSubmit >= date:
                    break
                if ret == lastSubmit:
                    ret = date

                if verdict == 'Happy New Year!' or verdict == 'Accepted':
                    cursor.execute(ac, (handel, problem,))
                    cursor.execute(his, (handel, problem,))
            elif idx == 8:
                idx = 0
        idx += 1
    conn.commit()
    return ret

sheetNum = 0
lastSubmits = []
firstItr = 1
for sheet in sheets:
    link = f"{sheet[0]}/status?order=BY_ARRIVED_DESC"
    driver.get(link)
    if firstItr: # To select accepted solutions
        verdict = driver.find_element_by_id("verdictName")
        verdict.send_keys(Keys.ARROW_DOWN)
    sheetNum += 1
    idx = 0
    for contestant in contestants: # itreate over contestants
        curHandle = driver.find_element_by_id("participantSubstring")
        curHandle.clear()
        curHandle.send_keys(contestant[0]) # handel
        curHandle.send_keys(Keys.ENTER)
        
        src = driver.page_source
        soup = BeautifulSoup(src, 'lxml')
        table = soup.find('table', class_ = "status-frame-datatable").find_all('td')
        lastSubmit = getSolutions(table, contestant[1])
       
         # to save the time of the last submit
        if firstItr:
            lastSubmits.append(lastSubmit)
        else:
            lastSubmits[idx] = max(lastSubmits[idx], lastSubmit)
            idx += 1
    firstItr = 0

# update last time solved
update = "update contestants set last_submit = ? where handle = ?"
for idx in range(len(contestants)):
    cursor.execute(update, (lastSubmits[idx], contestants[idx][0]))
conn.commit()
driver.quit()
Standing()