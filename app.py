from flask import Flask, render_template, request, jsonify
from task_scheduler import TaskScheduler, Task, Priority

app = Flask(__name__)

# Inicialize o scheduler
scheduler = TaskScheduler("tasks.db")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/tasks", methods=["GET"])
def get_tasks():
    """Obtém a lista de tarefas."""
    tasks = scheduler.get_tasks()
    task_list = []
    for task in tasks:
        task_list.append({
            "id": task.id,
            "name": task.name,
            "priority": task.priority.name,
            "estimated_time": task.estimated_time,
            "deadline": task.deadline,
            "completed": task.completed
        })
    return jsonify(task_list)

@app.route("/tasks", methods=["POST"])
def add_task():
    """Adiciona uma nova tarefa."""
    data = request.get_json()
    name = data.get("name")
    priority = Priority[data.get("priority").upper()]
    estimated_time = data.get("estimated_time")
    deadline = data.get("deadline")
    task = Task(name, priority, estimated_time, deadline)
    scheduler.add_task(task)
    return jsonify({"message": "Task added successfully"}), 201

@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    """Atualiza uma tarefa existente."""
    data = request.get_json()
    name = data.get("name")
    priority = Priority[data.get("priority").upper()]
    estimated_time = data.get("estimated_time")
    deadline = data.get("deadline")
    completed = data.get("completed")
    task = Task(name, priority, estimated_time, deadline)
    task.id = task_id
    scheduler.update_task(task_id, task)
    return jsonify({"message": "Task updated successfully"})

@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    """Exclui uma tarefa existente."""
    scheduler.delete_task(task_id)
    return jsonify({"message": "Task deleted successfully"})

@app.route("/tasks/<int:task_id>/complete", methods=["PUT"])
def complete_task(task_id):
    """Marca uma tarefa como concluída."""
    scheduler.complete_task(task_id)
    return jsonify({"message": "Task marked as completed"})

if __name__ == "__main__":
    app.run(debug=True)
