import requests
import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

botKey = '<Your bot Key>'
chatId = '<Your chatId>'

def History():
    get = "select * from history"
    history = cursor.execute(get).fetchall()
    for his in history:
        msg = f'Congratulation :)\n "{his[0]}"\n for solving: \n{his[1]} problem ^^'
        url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={chatId}&text={msg}"
        requests.get(url)

    delete = "delete from history"
    cursor.execute(delete)
    conn.commit()

def Standing():
    data = []
    get = "select * from contestants"
    contestants = cursor.execute(get).fetchall()
    for contestant in contestants: # itreate over contestants
        get = "select Pname from solved where handle = ?"
        problems = cursor.execute(get, (contestant[0], )).fetchall()
        data.append((len(problems), contestant[0]))
    msg = "-------- Current Standing 🥳 --------\n---------------------------------------\n"
    data.sort(reverse = True)
    for idx in range(len(data)):
        msg += f'{idx + 1} - {data[idx][1]}\nsolved : {data[idx][0]}\n---------------------\n'
      
    url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={chatId}&text={msg}"
    requests.get(url)

def notification():
    get = "select * from history"
    history = cursor.execute(get).fetchall()
    for idx in range(len(history)):
        msg = support[idx % len(support)] 
        msg = msg.replace('<handle>', history[idx][0]).replace('<problem>', history[idx][1])
        url = f"https://api.telegram.org/bot{botKey}/sendMessage?chat_id={chatId}&text={msg}"
        requests.get(url)
        
    delete = "delete from history"
    cursor.execute(delete)
    conn.commit()

#Standing()
#groups = f"https://api.telegram.org/bot{botKey}/getUpdates"
#req = requests.get(groups)
#print(req.text)
#notification()
