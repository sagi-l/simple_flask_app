import random
import json
import os
from flask import Flask, render_template, redirect, url_for, request, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
import redis

#webhook test 2

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY", "dev_secret")

# Redis configuration from environment
REDIS_HOST = os.environ.get("REDIS_HOST", "redis")
REDIS_PORT = int(os.environ.get("REDIS_PORT", "6379"))
REDIS_PASSWORD = os.environ.get("REDIS_PASSWORD")

redis_client = redis.Redis(
    host=REDIS_HOST,
    port=REDIS_PORT,
    password=REDIS_PASSWORD,
    decode_responses=True
)

TASKS_KEY = 'tasks'

class TaskForm(FlaskForm):
    task = StringField('Task', validators=[DataRequired()])
    submit = SubmitField('Add Task')

def generate_random_color():
    return "#%06x" % random.randint(0, 0xFFFFFF)

def get_tasks():
    tasks_json = redis_client.get(TASKS_KEY)
    if tasks_json:
        return json.loads(tasks_json)
    return []

def save_tasks(tasks):
    redis_client.set(TASKS_KEY, json.dumps(tasks))

@app.route('/', methods=['GET', 'POST'])
def index():
    form = TaskForm()
    if form.validate_on_submit():
        task = form.task.data
        task_color = generate_random_color()
        tasks = get_tasks()
        tasks.append({'task': task, 'color': task_color})
        save_tasks(tasks)
        return redirect(url_for('index'))

    tasks = get_tasks()
    return render_template('index.html', form=form, tasks=tasks)

@app.route('/delete-task/<int:task_id>')
def delete_task(task_id):
    tasks = get_tasks()
    if 0 <= task_id < len(tasks):
        tasks.pop(task_id)
        save_tasks(tasks)
    return redirect(url_for('index'))

@app.route('/update-task-order', methods=['POST'])
def update_task_order():
    data = request.get_json()
    tasks = get_tasks()
    updated_tasks = [tasks[int(i)] for i in data['tasks']]
    save_tasks(updated_tasks)
    return jsonify(success=True)

@app.route('/health')
def health():
    try:
        redis_client.ping()
        return {"status": "ok"}, 200
    except Exception:
        return {"status": "error"}, 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
