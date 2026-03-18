# app.py
from flask import Flask, request, jsonify, send_from_directory
from datetime import datetime
import os

app = Flask(__name__, static_folder='.', static_url_path='')

tasks = []
task_id_counter = 1

@app.route('/')
def index():
    return send_from_directory('.', 'index.html')

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def create_task():
    global task_id_counter
    data = request.json
    
    if not data or not data.get('title'):
        return jsonify({'error': 'Title is required'}), 400
    
    task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'completed': False,
        'priority': data.get('priority', 'medium'),
        'dueDate': data.get('dueDate'),
        'createdAt': datetime.now().isoformat()
    }
    
    tasks.append(task)
    task_id_counter += 1
    
    return jsonify(task), 201

@app.route('/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    for task in tasks:
        if task['id'] == task_id:
            task['completed'] = not task['completed']
            return jsonify(task)
    return jsonify({'error': 'Task not found'}), 404

@app.route('/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    tasks = [task for task in tasks if task['id'] != task_id]
    return jsonify({'message': 'Task deleted'}), 200

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)