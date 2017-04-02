import sqlite3

conn = sqlite3.connect('data.db')
cursor = conn.cursor()
# INTEGER for auto increment id
create_table = "CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username text, password text)"
cursor.execute(create_table)

create_table = "CREATE TABLE IF NOT EXISTS items (name text, price real)"
cursor.execute(create_table)


cursor.close()
conn.commit()
conn.close()
