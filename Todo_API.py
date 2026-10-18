from flask import Flask,jsonify,request,abort
app=Flask(__name__)

todos=[]
next_id=1


@app.route("/todos",methods=["POST"])
def create_todo():
    global next_id
    data=request.get_json()
    if not data or "title" not in data:
        return jsonify({"error":"title missing"}),400
    todo={"title":data["title"],"id":next_id,"done":False}
    todos.append(todo)
    next_id+=1
    return jsonify({"recieved":todo}),201


@app.route("/todos/<int:todo_id>",methods=["GET"])
def get_todo(todo_id):
    for todo in todos:
        if todo["id"]==todo_id:
            return jsonify(todo)
    abort(404)


@app.route("/todos",methods=["GET"])
def get_todos():
    return jsonify(todos)


@app.route("/todos/<int:todo_id>",methods=["PUT"])
def put_todo(todo_id):
    todoData=request.get_json()
    if not todoData:
        return jsonify({"error": "no data sent"}), 400
    for todo in todos:
        if todo["id"]==todo_id:
            if "title" in todoData:
                todo["title"]=todoData["title"]
            if "done" in todoData:
                    todo["done"]=todoData["done"]
            return jsonify(todo),200
    abort(404)


@app.route("/todos/<int:delete_id>",methods=["DELETE"])
def delete_todo(delete_id):
    for todo in todos:
        if todo["id"]==delete_id:
            removed=todos.remove(todo)
            return jsonify({"removed":todo})

    
@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "not found"}), 404


if __name__=="__main__":
    app.run(debug=True)
