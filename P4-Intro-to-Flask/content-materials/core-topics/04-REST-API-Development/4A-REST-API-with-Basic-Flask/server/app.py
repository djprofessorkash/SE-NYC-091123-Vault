"""
FILENAME:       app.py
TITLE:          Basic Flask REST API.
AUTHOR:         Aakash 'Kash' Sudhakar
DESCRIPTION:    A tutorial mini-project on setting up basic backend servers
                that handle RESTful API calls via HTTP requests. 
USAGE:          Run in CLI with command `python(3) app.py`, `flask run`, or
                `flask --app app.py --debug run`. 
"""

################################################################################
############## IMPORT STATEMENTS FOR BACKEND DEVELOPMENT IN FLASK ##############
################################################################################


from json import loads, dump
from flask import Flask, jsonify, request, abort, make_response


################################################################################
######### LOADING DATA AND SETTING UP FLASK SERVER FOR API DEVELOPMENT #########
################################################################################


# NOTE: Relative path to data may influence how Python can handle this script.
#       Ensure that Flask/Python is executed from an appropriate location.
PATH_TO_DATASET = "data/tasks.json"

with open(PATH_TO_DATASET, "r") as fr:
    tasks = loads(fr.read())["tasks"]

app = Flask(__name__)


################################################################################
####################### FLASK API DEVELOPMENT AND TESTING ######################
################################################################################

# NOTE: For all API routes, you can use either `http://localhost` or 
#       `http://AAA.B.C.D`, where the latter option's letters are replaced by 
#       the actual IP address from which your application loads.

"""
Test with the following command(s):
    curl -i http://localhost:{PORT}/
"""
@app.route("/", methods=["GET"])
def home():
    return {"message": "Welcome to the TODO List API!"}

"""
Test with the following command:
    curl -i http://localhost:{PORT}/todo/api/tasks
"""
@app.route("/todo/api/tasks", methods=["GET"])
def get_tasks():
    return tasks, 201

"""
Test with the following command:
    curl -i http://localhost:{PORT}/todo/api/tasks/1
"""
@app.route("/todo/api/tasks/<int:task_id>", methods=["GET"])
def get_task_by_task_id(task_id):
    task = [task for task in tasks if task["id"] == int(task_id)]
    if len(task) == 0:
        abort(404)
    return jsonify({"task": task[0]}), 201

"""
Test with the following command:
    curl -i -H "Content-Type: application/json" -X POST -d 
    '{"title":"Read a book","description":"Get a book from the library and read it over a week"}' 
    http://localhost:{PORT}/todo/api/tasks
```
"""
@app.route("/todo/api/tasks", methods=["POST"])
def create_task():
    if not request.json or not "title" in request.json:
        abort(400)
    with open(PATH_TO_DATASET, "w") as stream:
        task = {
            "id": tasks[-1]["id"] + 1,
            "title": request.json["title"],
            "description": request.json.get("description", ""),
            "done": False
        }
        tasks.append(task)
        dump({"tasks": tasks}, stream, indent=4)
    return jsonify({"task": task}), 201
    
"""
Test with the following command:
    curl -i -H "Content-Type: application/json" -X PATCH -d 
    '{"done":true}' http://localhost:{PORT}/todo/api/tasks/2
"""
@app.route("/todo/api/tasks/<int:task_id>", methods=["PATCH"])
def update_task_by_task_id(task_id):
    task = [task for task in tasks if task["id"] == int(task_id)]
    if len(task) == 0:
        abort(404)
    if not request.json:
        abort(400)
    if "title" in request.json and type(request.json["title"]) is not str:
        abort(400)
    if "description" in request.json and type(request.json["description"]) is not str:
        abort(400)
    if "done" in request.json and type(request.json["done"]) is not bool:
        abort(400)
    with open(PATH_TO_DATASET, "w") as stream:
        task[0]["title"] = request.json.get("title", task[0]["title"])
        task[0]["description"] = request.json.get("description", task[0]["description"])
        task[0]["done"] = request.json.get("done", task[0]["done"])
        dump({"tasks": tasks}, stream, indent=4)
    return jsonify({"task": task[0]}), 201

"""
Test with the following command:
    curl -H "Content-Type: application/json" -X DELETE
    http://localhost:{PORT}/todo/api/tasks/3
"""
@app.route("/todo/api/tasks/<int:task_id>", methods=["DELETE"])
def delete_task_by_task_id(task_id):
    task = [task for task in tasks if task["id"] == int(task_id)]
    if len(task) == 0:
        abort(404)
    with open(PATH_TO_DATASET, "w") as stream:
        tasks.remove(task[0])
        dump({"tasks": tasks}, stream, indent=4)
    return jsonify(task[0]), 201

"""
Test with the following command:
    curl -i http://localhost:{PORT}/whoooooooooo
"""
@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({"error": "Not Found!"}), 404)


################################################################################
####################### LAUNCHING SERVER-SIDE APPLICATION ######################
################################################################################


if __name__ == "__main__":
    app.run(port=5000, debug=True)