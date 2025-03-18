from flask import Flask, render_template, redirect, url_for, request, session, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from datetime import datetime

# Initialize Flask app and database
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'  # Use SQLite for testing, change for production
app.config['SECRET_KEY'] = 'your_secret_key'  # Change this to a more secure key

# Ensure the session expires when the browser is closed
app.config['SESSION_PERMANENT'] = False  # Disable persistent session
app.config['REMEMBER_COOKIE_DURATION'] = 0  # Set to zero for automatic logout

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'


# User model
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)

    # Relationship to Todos
    todos = db.relationship('Todo', backref='owner', lazy=True)


# Task model (For todo list)
class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Automatically set to the current date and time
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f'<Todo {self.content}>'


# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# Home route (requires login)
@app.route('/')
@login_required
def home():
    tasks = Todo.query.filter_by(user_id=current_user.id).all()
    return render_template('index.html', tasks=tasks)


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists in the database
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:  # Compare plain text password
            login_user(user)  # Log in the user
            return redirect(url_for('home'))  # Redirect to the home page
        else:
            return 'Invalid username or password!'

    return render_template('login.html')


# Logout route
@app.route('/logout')
def logout():
    logout_user()  # Log out the user
    flash('You have been logged out', 'info')  # Optional flash message
    return redirect(url_for('login'))  # Redirect to login page


# Signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username already exists
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return 'Username already exists! Please choose another one.'

        # Create new user
        new_user = User(username=username, password=password)
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('login'))  # After signing up, redirect to login

    return render_template('signup.html')


# Add task route
@app.route('/add', methods=['POST'])
@login_required
def add_task():
    content = request.form['content']
    new_task = Todo(content=content, user_id=current_user.id)
    db.session.add(new_task)
    db.session.commit()
    return redirect(url_for('home'))  # Redirect back to home page after adding a task


# Update task route
@app.route('/update/<int:task_id>', methods=['GET', 'POST'])
@login_required
def update_task(task_id):
    task = Todo.query.get_or_404(task_id)

    if request.method == 'POST':
        # Get the new content for the task
        task.content = request.form['content']
        db.session.commit()
        flash('Task updated successfully!', 'success')
        return redirect(url_for('home'))  # Redirect to the home page after updating

    # Render the update page with the task data
    return render_template('update.html', task=task)


# Delete task route
@app.route('/delete/<int:task_id>', methods=['POST'])
@login_required
def delete_task(task_id):
    task = Todo.query.get_or_404(task_id)
    if task.user_id != current_user.id:
        flash('You cannot delete another user\'s task.', 'danger')
        return redirect(url_for('home'))  # Prevent users from deleting others' tasks

    db.session.delete(task)
    db.session.commit()
    flash('Task deleted successfully!', 'success')
    return redirect(url_for('home'))  # Redirect back to home page after deleting a task


if __name__ == "__main__":
    app.run(debug=True)
