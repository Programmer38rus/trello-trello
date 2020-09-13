from trello import TrelloApi
import requests
import sys

# Данные авторизации в API Trello  
auth_params = {
    "key": "50dad6f927983cc0b4a97d8db35c464f",
    "token": "3bc4e981b5d354f489eaf4e11df01a8251c022ee8214a1a867bcb716b719a652"}

# Адрес, на котором расположен API Trello, # Именно туда мы будем отправлять HTTP запросы. 
base_url = "https://api.trello.com/1/{}"  
board_id = "Js8lvcmU"

# trello = TrelloApi(api_key, token)

# response = trello.boards.new("Mother!")

# for i, k in response.items():
#     print(f"{i}: {k}")

def read():

    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        # print(str(column['pos']) + ' ' +column['name'])
        task_data = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        num_task = str(len(task_data))
        print(f"\n{column['name']}: количество задач {num_task}\n")
        if not task_data:
            # print(column)
            print("\t" + 'Нет задач!')
            continue
        for task in task_data:      
            print('\t' + task['name'])  
        # else:
        #     for i in task_data:
        #         print(i['desc'])
# print(base_url.format('boards') + '/' + base_id + '/lists')

def create(name, column_name):

    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    for column in column_data:
        if column['name'] == column_name:
            requests.post(base_url.format('cards'), data={'name': name, 'idList':column['id'], **auth_params})
            break

def cc(name):
    
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()
    for column in column_data:
        if column['name'] == name:
            name = input("Такое имя уже существует \nВведите другое: ")       
    requests.post(base_url.format('boards') + '/' + board_id + '/lists', data={'name': name, 'pos': "bottom", **auth_params})

    print(f"Колонка с именем '{name}' создана")

def move(name, column_name):
    """
    Функция для перемещения задач по колонкам
    """
    column_data = requests.get(base_url.format('boards') + '/' + board_id + '/lists', params=auth_params).json()

    tasks_names = {}
    enum = 0
    
    for column in column_data:
        column_tasks = requests.get(base_url.format('lists') + '/' + column['id'] + '/cards', params=auth_params).json()
        for task in column_tasks:
            # проверяем наличие введенной пользователем задачи в trello
            # и создаем словарь с совпадениями
            if task['name'] == name:
                enum += 1
                
                tasks_names[str(enum)] = {"id": task["id"], "name": task['name'], "desc": task["desc"], "List": column['name']}
        
    
    if len(tasks_names) == 1:
            task_id = tasks_names["1"]["id"]
    elif len(tasks_names) > 1:
        for id, task in tasks_names.items():
            print(id + " " + task["name"] + "  Описание: " + task["desc"] + " --LIST: " + task["List"])
        id = input("Выберите какую задачу переместить?\nВведите id:")
        task_id = tasks_names[id]["id"]
        print(task_id)
   
    for column in column_data:
        if column['name'] == column_name:
            try:
                requests.put(base_url.format('cards') + '/' + task_id + '/idList', data={'value': column['id'], **auth_params})
            except UnboundLocalError:
                read()
                name = input(f"Задача с именеи {name} отсутствует!\nВведите другое: ")
                move(name, column_name)
            break

if __name__ == "__main__":
    if len(sys.argv) <= 2:
        read()
    elif sys.argv[1] == 'create':
        create(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'move':
        move(sys.argv[2], sys.argv[3])
    elif sys.argv[1] == 'cc':
        cc(sys.argv[2])
