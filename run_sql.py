import sqlite3

conn = sqlite3.connect("todos.db")
sql = open("exercises.sql").read()
for statement in sql.split(";"):
    if statement.strip():
        cursor = conn.execute(statement)
        for row in cursor.fetchall():
            print(row)
conn.commit()
conn.close()