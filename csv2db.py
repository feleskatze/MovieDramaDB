import csv
import sqlite3
from pykakasi import kakasi, wakati


conn = sqlite3.connect('MDlist.db')
cur = conn.cursor()

table_create_q = '''CREATE TABLE MDLIST (title TEXT,title_ruby TEXT, category TEXT, note TEXT, updatetime TEXT)'''
cur.execute(table_create_q)

kakasi = kakasi()
kakasi.setMode('J', 'H')
conv = kakasi.getConverter()

with open('./list.csv', 'r' ,encoding="utf-8") as f:
    b = csv.reader(f)
    for t in b:
        t[1] = conv.do(t[0])
        t[2] = t[2].strip()
        cur.execute('INSERT INTO MDLIST (title, title_ruby, category, updatetime) VALUES(?,?,?,CURRENT_TIMESTAMP)', t)

cur.execute('SELECT * FROM MDLIST')
print(cur.fetchall())

conn.commit()
conn.close()
