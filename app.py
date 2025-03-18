from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from flask_migrate import Migrate  # Import Migrate
from models.user import User
from models.todo import Todo
from datetime import datetime
from db import db  # Import db from db.py

# Initialize the Flask app
app = Flask(__name__)

# Configure the app with the database URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Change this to your actual database URI
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Disable track modifications for performance reasons
app.config['SECRET_KEY'] = 'your_secret_key'

# Initialize the database and migration system
db.init_app(app)
migrate = Migrate(app, db)  # Initialize Flask-Migrate with the app and db

# Initialize Flask-Login
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# User loader for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = User.query.filter_by(username=username).first()

        if user and user.password == password:
            login_user(user)
            return redirect(url_for('index'))
        else:
            return 'Invalid username or password!'
    return render_template('login.html')

# Logout Route
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))

# Home route (task management page)
@app.route('/', methods=['POST', 'GET'])
@login_required
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content, user_id=current_user.id)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.filter_by(user_id=current_user.id).order_by(Todo.date_created.desc()).all()
        return render_template('index.html', tasks=tasks)

# Route to delete a task
@app.route('/delete/<int:id>')
@login_required
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)

    if task_to_delete.user_id != current_user.id:
        return 'You do not have permission to delete this task.'

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'There was an issue deleting your task'

# Route to update a task
@app.route('/update/<int:id>', methods=['GET', 'POST'])
@login_required
def update(id):
    task_to_update = Todo.query.get_or_404(id)

    if task_to_update.user_id != current_user.id:
        return 'You do not have permission to update this task.'

    if request.method == 'POST':
        task_content = request.form['content']
        task_to_update.content = task_content
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task_to_update)

# Signup Route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists! Please choose another one.'

        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('signup.html')

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
