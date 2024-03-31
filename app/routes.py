from flask import request
from app import app, db
from .models import Task, User
from .auth import basic_auth, token_auth


@app.route("/")
def index():
    return "This is my Task API.  Please enjoy"

# User endpoints

@app.route('/users', methods=['POST'])
def create_user():
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    data = request.json
    required_fields = ['username', 'email', 'password']
    missing_fields = []
    for field in required_fields:
        if field not in data:
            missing_fields.append(field)
    if missing_fields:
        return {'error': f"{', '.join(missing_fields)} must be in the request body"}, 400
    
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')

    check_users = db.session.execute(db.select(User).where( (User.username == username) | (User.email == email) )).scalars().all()
    if check_users:
        return {'error': "A user with that username and/or email already exists"}, 400
    new_user = User(username=username, email=email, password=password)
    return new_user.to_dict(), 201

@app.route('/users/<int:user_id>')
def get_user(user_id):
    user = db.session.get(User, user_id)
    if user:
        return user.to_dict()
    else:
        return {'error': f"User with an ID of #{user_id} does not exist."}, 404
    
@app.route('/users/<int:user_id>', methods=['PUT'])
@token_auth.login_required()
def edit_user(user_id):
    if not request.is_json:
        return {'error': 'Your content-type must be application/json'}, 400
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with ID #{user_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if current_user is not user:
        return {'error': "This is not your account.  You do not have permission to edit"}, 403
    data = request.json
    user.update(**data)
    return user.to_dict

@app.route('/users/<int:user_id>', methods=['DELETE'])
@token_auth.login_required()
def delete_user(user_id):
    user = db.session.get(User, user_id)
    if user is None:
        return {'error': f"User with ID #{user_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if current_user is not user:
        return {'error': "You are not this user.  You do not have permission to delete"}, 403
    user.delete()
    return {'success': f"{user.username} was successfully deleted"}

@app.route('/token')
@basic_auth.login_required
def get_token():
    user = basic_auth.current_user()
    return user.get_token()



# Task Endpoints

@app.route('/tasks')
def get_tasks():
    tasks = db.session.execute(db.select(Task)).scalars().all()
    return [t.to_dict() for t in tasks]

@app.route('/tasks/<int:task_id>')
def get_task(task_id):
    task = db.session.get(Task, task_id)
    if task:
        return task.to_dict()
    else:
        return {'error': f"Task with an ID of {task_id} does not exist"}, 404

@app.route('/tasks', methods=['POST'])
@token_auth.login_required
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
    current_user = token_auth.current_user()
    new_task = Task(title=title, description=description, due_date=due_date, user_id=current_user.id)
    return new_task.to_dict(), 201

@app.route('/tasks/<int:post_id>', methods=['PUT'])
@token_auth.login_required()
def edit_task(task_id):
    if not request.is_json:
        return {'error': 'Your cuontent-type must be application/json'}, 400
    task = db.session.get(Task, task_id)
    if task is None:
        return {'error': f"Task with ID #{task_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if current_user is not task.user:
        return {'error': "This is not your post. You do not have permisson to edit"}, 403
    data = request.json
    task.update(**data)
    return task.to_dict

@app.route('/tasks/<task_id>', methods=['DELETE'])
@token_auth.login_required()
def delete_task(task_id):
    task = db.session.get(Task, task_id)
    if task is None:
        return {'error': f"Task with ID #{task_id} does not exist"}, 404
    current_user = token_auth.current_user()
    if current_user is not task.user:
        return {'error': "This is not your task. You do not have permisson to delete"}, 403
    task.delete()
    return {'success': f"{task.title} was successfully deleted"}
    

