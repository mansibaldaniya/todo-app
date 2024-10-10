from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

# Task class
class Task:
    def __init__(self, title, description, category, status="Pending"):
        self.title = title
        self.description = description
        self.category = category
        self.status = status

    def mark_completed(self):
        self.status = "Completed"


# Load tasks from JSON file
def load_tasks():
    try:
        with open('tasks.json', 'r') as f:
            tasks_data = json.load(f)
            tasks = [Task(**task) for task in tasks_data]
            return tasks
    except (FileNotFoundError, json.JSONDecodeError):
        return []

# Save tasks to JSON file
def save_tasks(tasks):
    with open('tasks.json', 'w') as f:
        json.dump([task.__dict__ for task in tasks], f)

# Index route to show all tasks
@app.route('/')
def index():
    tasks = load_tasks()
    return render_template('index.html', tasks=tasks)

# Route to add a new task
@app.route('/add', methods=['GET', 'POST'])
def add_task():
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        category = request.form['category']
        status = request.form['status']
        tasks = load_tasks()
        new_task = Task(title, description, category, status)
        tasks.append(new_task)
        save_tasks(tasks)
        return redirect(url_for('index'))
    return render_template('add_task.html')

# Route to mark a task as completed
@app.route('/complete/<int:task_id>')
def mark_completed(task_id):
    tasks = load_tasks()
    tasks[task_id].mark_completed()
    save_tasks(tasks)
    return redirect(url_for('index'))

# Route to delete a task
@app.route('/delete/<int:task_id>')
def delete_task(task_id):
    tasks = load_tasks()
    del tasks[task_id]
    save_tasks(tasks)
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
