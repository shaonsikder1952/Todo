from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Optional but recommended to avoid warnings

db = SQLAlchemy(app)

class Todo(db.Model):  # Fixed incorrect 'db.model' → 'db.Model'
    id = db.Column(db.Integer, primary_key=True)  # Fixed 'db.column' → 'db.Column', 'db.integer' → 'db.Integer'
    content = db.Column(db.String(200), nullable=False)  # Fixed 'db.string' → 'db.String'
    completed = db.Column(db.Integer, default=0)  # Fixed 'db.integer' → 'db.Integer'
    date_created = db.Column(db.DateTime, default=datetime.utcnow)  # Fixed 'data_created' → 'date_created'

    def __repr__(self):
        return f'<Task {self.id}>'  # Fixed missing closing bracket

@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Todo(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'There was an issue adding your task'
    else:
        tasks = Todo.query.order_by(Todo.date_created.desc()).all()  # Latest tasks first
        return render_template('index.html', tasks=tasks)

@app.route('/delete/<int:id>', methods=['GET', 'POST'])
def delete(id):
    task_to_delete = Todo.query.get_or_404(id)  # Fetch the task by ID

    try:
        db.session.delete(task_to_delete)  # Delete the task from the database
        db.session.commit()
        return redirect('/')  # Redirect to the home page
    except:
        return 'There was an issue deleting your task'

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    task_to_update = Todo.query.get_or_404(id)  # Fetch the task by ID

    if request.method == 'POST':
        task_content = request.form['content']  # Get the updated content from the form
        task_to_update.content = task_content  # Update the task content

        try:
            db.session.commit()  # Commit the changes to the database
            return redirect('/')  # Redirect to the home page
        except:
            return 'There was an issue updating your task'
    else:
        return render_template('update.html', task=task_to_update)  # Render the update form with current task data

if __name__ == "__main__":
    app.run(debug=True)
