import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

file = open('delete.txt','r')
for line in file:
    if line[0] == '*':
        continue
    delete = f"delete from {line}"
    cursor.execute(delete)
    conn.commit()
    print(f"- {cursor.rowcount} {line} has been deleted successfully.")

file.close()