import sqlite3
# sqlite store data into a single file
connection = sqlite3.connect('data.db')

cursor = connection.cursor()

create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, (1, 'qingyun', 'wqycfc1992'))

users = [
    (2, 'kane', 'kane559'),
    (3, 'roger', '420398')
]
# execute multiple lines
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM  users"
for row in cursor.execute(select_query):
    print (row)

connection.commit()
connection.close()
