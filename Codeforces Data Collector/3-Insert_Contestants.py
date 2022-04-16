import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

insert = "insert or ignore into contestants (handle, last_submit) values(?,?)"

fi = open('contestants.txt', 'r')
firstItr = 1
for line in fi:
    if firstItr:
        time = line.rstrip()
        firstItr = 0
    else:
        cursor.execute(insert, (line.rstrip(), time, ))

fi.close()
conn.commit()