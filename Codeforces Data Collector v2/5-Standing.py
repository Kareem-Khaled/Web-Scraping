import sqlite3            
import xlsxwriter
import Sheet_Update

# from Telegram_Bot import *

# Database connection
conn = sqlite3.connect('app.db')
cursor = conn.cursor()

# Get all Sheets to iterate over its problem
get = "select * from sheets"
sheets = cursor.execute(get).fetchall()

# Get all contestants to get their aceepted soultions
get = "select * from contestants"
contestants = cursor.execute(get).fetchall()

workbook = xlsxwriter.Workbook('K_K - Training.xlsx')
worksheet = workbook.add_worksheet('Standing')
bold = workbook.add_format({'bold': True})


if __name__ == '__main__':
    row = 0
    col = 0
    worksheet.write(row, col, 'Handle/Sheet')
    
    for sheet in sheets:
        col += 1
        worksheet.write_url(row, col, sheet[0], string=sheet[1])
    row = 0
    col = 0

    for contestant in contestants: 
        row += 1
        worksheet.write_url(row, col, 'https://codeforces.com/profile/' + contestant[0], string=contestant[0])

    for sheet in sheets:
        row = 0
        col += 1
        for contestant in contestants: # itreate over contestants
            row += 1
            query = f"select Pname from '{sheet[1]}' where handle = '{contestant[0]}'"
            problems = cursor.execute(query).fetchall()
            Pnum = str(len(problems)) + '/' + str(sheet[2])
            worksheet.write(row, col, Pnum)
            
    workbook.close()
    Sheet_Update.update()