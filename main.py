# coding : utf-8

import sqlite3
import eel


web_app_option = {
    'mode': 'chrome-app',
    'port': 8000,
    'chromeFlags':[
        '--window-size=800,900',
    ]
}



# SQLite
conn = sqlite3.connect('MDlist.db')
cur = conn.cursor()

# 作成済みの場合の回避
try:
    # タイトル、カテゴリー、備考、更新日時
    table_create_q = '''CREATE TABLE MDLIST (title TEXT,title_ruby TEXT, category TEXT, note TEXT, updatetime TEXT)'''
    cur.execute(table_create_q)
except sqlite3.Error as e:
    pass


@eel.expose
def add_record(data):
    cur.execute('INSERT INTO MDLIST (title, title_ruby, category, note, updatetime) VALUES(?,?,?,?,CURRENT_TIMESTAMP)', data)
    conn.commit()

@eel.expose
def show_all():
    result = []
    for i in ('日本映画', '海外映画', '日本ドラマ', '海外映画', 'その他'):
        cur.execute('SELECT * FROM MDLIST WHERE category=?', (i,))
        result = result + cur.fetchall()
    return result

@eel.expose
def search(data):
    cur.execute('SELECT * FROM MDLIST WHERE title=? AND category=?', (data,))
    return cur.fetchall()

@eel.expose
def history():
    cur.execute('SELECT * FROM MDLIST ORDER BY updatetime DESC LIMIT 10')
    return cur.fetchall()



eel.init('web')
eel.start('main.html', options=web_app_option)

conn.close()
