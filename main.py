from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import os

app = Flask(__name__)

# Set up database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define a Task model (represents a row in the tasks table)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)

    def to_dict(self):
        return {'id': self.id, 'description': self.description}

# Create the database file and table if it doesn't exist
with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template('index.html')

# Get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])

# Add a new task
@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    task_text = data.get('task')

    if task_text:
        new_task = Task(description=task_text)
        db.session.add(new_task)
        db.session.commit()
        return jsonify({'message': 'Task added!', 'task': new_task.to_dict()}), 201
    return jsonify({'message': 'Task cannot be empty'}), 400


# Delete a task
@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get(task_id)
    if task:
        db.session.delete(task)
        db.session.commit()
        return jsonify({'message': 'Task deleted!'})
    else:
        return jsonify({'message': 'Task not found'}), 404


@app.route('/debug-tasks')
def debug_tasks():
    tasks = Task.query.all()
    return jsonify([task.to_dict() for task in tasks])
