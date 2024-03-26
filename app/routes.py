from flask import request
from app import app
from fake_tasks.tasks import tasks_list

@app.route("/")
def index():
    return "This is my home work.  Please go to /tasks or /tasks/task id to see them"

@app.route('/tasks')
def get_tasks():
    tasks = tasks_list
    return tasks

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    tasks = tasks_list
    for task in tasks:
        if task['id'] == task_id:
            return task
    return {'error': f"Task with an ID of {task_id} does not exist"}, 404