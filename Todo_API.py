from flask import Flask
from flask import jsonify
from flask import request
from flask import abort
import sqlite3
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__)) # gives the path of the file save in full directory
DB_PATH = os.path.join(BASE_DIR, "todos.db")#build the database path

app=Flask(__name__)


def get_db():#only func every route will call code reuseability
    conn=sqlite3.connect(DB_PATH) #connects to the database where data is stored
    conn.row_factory=sqlite3.Row # converts the data in tuple to row row lacks dict properties hence dict(row) is done further
    return conn



def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS todos (
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            done INTEGER DEFAULT 0
        )
    """)
    conn.commit()
    conn.close()




@app.route("/todos",methods=["POST"])
def create_todo():
    data=request.get_json()
    if not data or "title" not in data:
        return jsonify({"error":"title missing"}),400
    conn=get_db()
    cursor=conn.execute("insert into todos (title) values (?)",(data["title"],))
    conn.commit()
    new_id=cursor.lastrowid
    conn.close()
    return jsonify({"recieved": {"id": new_id, "title": data["title"], "done": 0}}), 201


@app.route("/todos/<int:todo_id>",methods=["GET"])
def get_todo(todo_id):
    conn=get_db()
    rows=conn.execute("select*from todos where id = ?" ,(todo_id,)).fetchone()
    if rows is None:
        conn.close()
        abort(404)
    return jsonify(dict(rows))



@app.route("/todos",methods=["GET"])
def get_todos():
    conn=get_db()
    rows=conn.execute("select*from todos").fetchall()
    conn.close()
    return jsonify([dict(row) for row in rows])



@app.route("/todos/<int:todo_id>",methods=["PUT"])
def put_todo(todo_id):
    Data=request.get_json()
    if not Data:
        return jsonify({"error": "no data sent"}), 400
    conn=get_db()
    rows=conn.execute("select *from todos where id=?",(todo_id,)).fetchone()
    if rows is None:
        conn.close()
        abort(404)
    new_title=Data.get("title",rows["title"])
    new_done=Data.get("done",rows["done"])
    conn.execute("update todos set  title=?,done=? where id=?",(new_title,new_done,todo_id))
    conn.commit
    updated=conn.execute("select* from todos where id =?",(todo_id,)).fetchone()
    conn.close
    return jsonify(dict(updated))




@app.route("/todos/<int:delete_id>",methods=["DELETE"])
def delete_todo(delete_id):
    conn=get_db()
    rows=conn.execute("select*from todos where id = ?",(delete_id,)).fetchone()
    if rows is None:
        conn.close()
        abort(404)
    conn.execute("delete from todos where id =?",(delete_id,))
    conn.commit()
    conn.close()
    return jsonify({"removed":dict(rows)})

    
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "not found"}), 404


if __name__=="__main__":
    init_db()
    app.run(debug=True)
