import sqlite3            

conn = sqlite3.connect('app.db')
cursor = conn.cursor()

contestants = """CREATE TABLE "contestants" (
	"handle"	TEXT,
	"last_submit"	TEXT,
	PRIMARY KEY("handle")
);"""

sheets = """CREATE TABLE "sheets" (
	"link"	TEXT,
	PRIMARY KEY("link")
);"""

problems = """CREATE TABLE "problems" (
	"name"	TEXT,
	"link"	TEXT,
	PRIMARY KEY("name")
);"""

solved = """CREATE TABLE "solved" (
	"handle"	TEXT,
	"Pname"	TEXT,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle")
);"""

history = """CREATE TABLE "history" (
	"handle"	TEXT,
	"Pname"	TEXT,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle")
);"""


wrongs = """CREATE TABLE "wrongs" (
	"handle"	TEXT,
	"Pname"	TEXT,
	"cnt"	INTEGER,
	PRIMARY KEY("handle","Pname"),
	FOREIGN KEY("handle") REFERENCES "contestants"("handle"),
	FOREIGN KEY("Pname") REFERENCES "problems"("name")
);"""

cursor.execute(contestants)
cursor.execute(sheets)
cursor.execute(solved)
cursor.execute(history)