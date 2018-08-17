# coding : utf-8

import sqlite3
import eel
import copy
from pykakasi import kakasi, wakati


web_app_option = {
    'mode': 'chrome-app',
    'port': 8000,
    'chromeFlags':[
        '--window-size=1000,900',
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

# レコードに追加
@eel.expose
def add_record(data):
    cur.execute('INSERT INTO MDLIST (title, title_ruby, category, note, updatetime) VALUES(?,?,?,?,CURRENT_TIMESTAMP)', data)
    conn.commit()

# 全件取得
@eel.expose
def show_all():
    result = []
    for i in ('日本映画', '海外映画', '日本ドラマ', '海外ドラマ', 'その他'):
        cur.execute('SELECT *, ROWID FROM MDLIST WHERE category=?', (i,))
        i_res = cur.fetchall()
        if i_res is not None:
            i_res.sort(key=lambda x:x[1])
        result = result + i_res
    return result


# 検索画面が更新すると消えちゃうので検索キーをこっちで保持することにした
search_data = []
@eel.expose
def search_update(data):
    global search_data
    search_data = copy.deepcopy(data)


# 検索
@eel.expose
def search():
    global search_data
    if len(search_data) == 2 and search_data[1] == 'すべて':
        search_data[0] = '%' + search_data[0] + '%'
        cur.execute('SELECT *, ROWID FROM MDLIST WHERE title LIKE ?', (search_data[0],))
    elif len(search_data) == 2:
        search_data[0] = '%' + search_data[0] + '%'
        cur.execute('SELECT *, ROWID FROM MDLIST WHERE title LIKE ? AND category=?', (search_data,))
    else:
        return 0
    return cur.fetchall()

# 履歴表示
@eel.expose
def history():
    cur.execute('SELECT *, ROWID FROM MDLIST ORDER BY updatetime DESC LIMIT 10')
    return cur.fetchall()

# タブフラグ管理がJavaでうまくできないのでこっちでやる
checked_num = 2 # 全件表示:1 追加:2 検索:3

@eel.expose
def check_checked():
    global checked_num
    return checked_num

@eel.expose
def check_update(num):
    global checked_num
    checked_num = num



eel.init('web')
eel.start('main.html', options=web_app_option)

conn.close()
