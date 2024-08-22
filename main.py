import random
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key_here'

# In-memory storage for tasks
tasks = []

# Define the form class
class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    submit = SubmitField('Add Task')

# Function to generate a random color
def generate_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

# Route for the main page
@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        task = form.task.data
        if task:
            task_color = generate_random_color()
            tasks.append({'task': task, 'color': task_color})
        return redirect(url_for('index'))

    return render_template('index.html', form=form, tasks=tasks)

# Route to delete a task
@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
    return redirect(url_for('index'))

# Route to update the task order (optional for drag-and-drop persistence)
@app.route('/update-task-order', methods=['POST'])
def update_task_order():
    data = request.get_json()
    # Update the tasks list based on the new order
    updated_tasks = []
    for task_id in data['tasks']:
        updated_tasks.append(tasks[int(task_id)])
    tasks[:] = updated_tasks  # Replace the old tasks list with the updated one
    return jsonify(success=True)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
