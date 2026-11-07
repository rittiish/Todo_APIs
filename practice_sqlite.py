import sqlite3


conn = sqlite3.connect("todos.db")
conn.row_factory=sqlite3.Row

cursor= conn.execute("SELECT * FROM todos")
todos=[dict(row)for row in cursor.fetchall()]
print(todos)

conn.close()



