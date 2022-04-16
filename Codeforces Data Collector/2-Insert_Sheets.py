import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

insert = "insert or ignore into sheets (link) values(?)"

fi = open('sheets.txt', 'r')
for line in fi:
    if line[0] == '*':
        continue
    cursor.execute(insert, (line.rstrip(),))

fi.close()
conn.commit()
print("sheets added successfully :)")