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

@app.route('/tasks', methods=['POST'])
def create_task():
    if not request.is_json:
        return{'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['title', 'description', 'dueDate']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    title = data.get('title')
    description = data.get('description')
    due_date = data.get('dueDate')
    new_task = {
        'id': len(tasks_list) + 1,
        'title': title,
        'description': description,
        'completed': False,
        'dueDate': due_date
    }
    tasks_list.append(new_task)
    return new_task, 201
