conn = sqlite3.connect('ma_base.db')

cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
     id INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
     name TEXT,
     age INTERGER
)
""")
conn.commit()

cursor.execute("""
INSERT INTO users(name, age) VALUES(?, ?)""", ("olivier", 30))

id = cursor.lastrowid
print('dernier id: %d' % id)

users = []
users.append(("olivier", 30))
users.append(("jean-louis", 90))
cursor.executemany("""
INSERT INTO users(name, age) VALUES(?, ?)""", users)

cursor.execute("""select* from users""""")

user1 = cursor.fetchone()
print(user1)

cursor.execute("""SELECT id, name, age FROM users""")
rows = cursor.fetchall()
for row in rows:
    print('{0} : {1} - {2}'.format(row[0], row[1], row[2]))

id = 2
cursor.execute("""SELECT id, name FROM users WHERE id=?""", (id,))
response = cursor.fetchone()
print(response)

cursor.execute("""select* from users""")
rep = cursor.fetchall()
print(rep)