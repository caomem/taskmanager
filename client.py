import requests

# Função para criar uma nova tarefa
def create_task(name, priority, estimated_time, deadline=None):
    url = 'http://localhost:5000/tasks'
    data = {
        'name': name,
        'priority': priority,
        'estimated_time': estimated_time,
        'deadline': deadline
    }
    response = requests.post(url, json=data)
    if response.status_code == 201:
        print("Tarefa criada com sucesso!")
    else:
        print("Erro ao criar a tarefa.")

# Função para obter as tarefas do dia
def get_daily_tasks():
    url = 'http://localhost:5000/daily_tasks'
    response = requests.get(url)
    if response.status_code == 200:
        tasks = response.json()
        print("Tarefas do dia:")
        for task in tasks:
            print(f"- {task['name']} ({task['estimated_time']} horas), Prioridade: {task['priority']}, Deadline: {task['deadline']}")
    else:
        print("Erro ao obter as tarefas do dia.")

# Função para marcar uma tarefa como concluída
def complete_task(task_name):
    url = f'http://localhost:5000/complete_task/{task_name}'
    response = requests.put(url)
    if response.status_code == 200:
        print(f"Tarefa '{task_name}' marcada como concluída.")
    else:
        print(f"Erro ao marcar a tarefa '{task_name}' como concluída.")

# Exemplos de uso
create_task("Estudar para a prova", 3, 4, deadline="2024-02-19")
create_task("Preparar relatório", 2, 3, deadline="2024-03-10")
create_task("Reunião de equipe", 1, 2, deadline="2024-02-19")
create_task("Responder emails", 2, 1, deadline="2024-03-02")

get_daily_tasks()

complete_task("Responder emails")
