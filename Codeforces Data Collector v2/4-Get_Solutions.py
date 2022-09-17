# import os
# import time
import sqlite3            
import datetime
import warnings
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support import expected_conditions as EC
# from Telegram_Bot import *

# Chrome settings & options to hide the browser
options = ChromeOptions()
warnings.filterwarnings("ignore", category = DeprecationWarning)
options.add_experimental_option('excludeSwitches', ['enable-logging'])
options.headless = True
driver = webdriver.Chrome(ChromeDriverManager().install(), options = options)

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
def getSolutions(table, lastSubmit, sheet):
    ac = f"insert or ignore into '{sheet}' (handle, Pname) values(?,?)"
    idx = 0 #2000-08-13 13:08:00
    lastSubmit = datetime.datetime(int(lastSubmit[0:4]), int(lastSubmit[5:7]), int(lastSubmit[8:10]), int(lastSubmit[11:13]), int(lastSubmit[14:16]))
    ret = lastSubmit
    for td in table:
        if len(td.text):
            txt = td.text.replace('\n','').strip()
            if idx == 1:
                try:
                    txt = txt[:-5]
                    date = dateFormat(txt)
                except:pass
            elif idx == 2:
                txt = td.a.text.replace('\n','').strip()
                handel = txt
            elif idx == 3:
                problem = txt
            elif idx == 5: #08/13/2000 13:08 
                try:
                    verdict = txt
                    date = datetime.datetime(int(date[6:10]), int(date[0:2]), int(date[3:5]), int(date[11:13]), int(date[14:16]))
                    if lastSubmit >= date:
                        break
                    if handel[-1] == '#': 
                        handel = handel.rstrip(handel[-1])

                    if ret == lastSubmit:
                        ret = date

                    if verdict == 'Happy New Year!' or verdict == 'Accepted':
                        cursor.execute(ac, (handel, problem,))
                        cursor.execute(his, (handel, problem,))
                except:pass
            elif idx == 8:
                idx = 0
        idx += 1
    conn.commit()
    return ret

sheetNum = 0
lastSubmits = []
# firstItr = 1

if __name__ == '__main__':
    for sheet in sheets:
        try:
            link = f"{sheet[0]}/status?order=BY_ARRIVED_DESC"
            driver.get(link)
        except Exception as e: 
            print("-->> err - 1")
        try:
            # if firstItr: # To select accepted solutions
            _ = WebDriverWait(driver, 50).until(
            EC.presence_of_element_located((By.ID, "verdictName")))
            verdict = driver.find_element(By.ID, "verdictName")
            verdict.send_keys(Keys.ARROW_DOWN)
            sheetNum += 1
            idx = 0
            print(f"\n- {sheet[1]}")
        except Exception as e: 
            print("-->> err - 2")
        for contestant in contestants: # itreate over contestants
            try:
                page = 1
                print(f"-> {contestant[0]}")
                _ = WebDriverWait(driver, 50).until(
                EC.presence_of_element_located((By.ID, "participantSubstring")))
                curHandle = driver.find_element(By.ID, "participantSubstring")
                curHandle.clear()
                curHandle.send_keys(contestant[0]) # handel
                curHandle.send_keys(Keys.ENTER)
            except Exception as e: 
                print("-->> err - 3")

            try:
                soup = BeautifulSoup(driver.page_source, 'lxml')
                pages = int(soup.find_all('span', class_ = 'page-index')[-1].text)
            except: pages = 1

            while page <= pages:
                try:
                    link = f"{sheet[0]}/status/page/{page}?order=BY_ARRIVED_DESC"
                    driver.get(link) 
                    # print(f"-->> {page}")
                    page += 1
                    
                    src = driver.page_source
                    soup = BeautifulSoup(src, 'lxml')
                    table = soup.find('table', class_ = "status-frame-datatable").find_all('td')
                    lastSubmit = getSolutions(table, contestant[1], sheet[1])
            
                    # to save the time of the last submit
                    if idx + 1 > len(lastSubmits):
                        lastSubmits.append(lastSubmit)
                    else:
                        lastSubmits[idx] = max(lastSubmits[idx], lastSubmit) 
                except Exception as e:
                    # page += 1
                    print("-->> err - 4")
                    print(e)
     
            idx += 1
        # firstItr = 0

    try:
        # update last time solved
        update = "update contestants set last_submit = ? where handle = ?"
        for idx in range(len(contestants)):
            cursor.execute(update, (lastSubmits[idx], contestants[idx][0]))

        conn.commit()
        driver.quit()
    except Exception as e:
        print("-->> err - 5")

    # Standing()