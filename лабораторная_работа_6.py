# -*- coding: utf-8 -*-
"""Лабораторная работа 6.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1FGr22lIyqDGbUFfZpyfW7pnm6SfsIYMC
"""

print('Лабораторная работа 6')

!pip install flask-ngrok
!pip install pyngrok

from flask import Flask, render_template_string
import sqlite3
import threading
from pyngrok import ngrok
import os
# Установка переменной окружения для Flask
os.environ["FLASK_ENV"] = "development"

app = Flask(__name__)
port = 5000

# Установка токена для ngrok
ngrok.set_auth_token("2qD3Sf1rysQhbvbkP1k6d2BMU7f_2T5jgBiQhFijN8dLJ5Nqs")

# Открытие туннеля ngrok к HTTP серверу
public_url = ngrok.connect(port).public_url
print(" * ngrok tunnel \"{}\" -> \"http://127.0.0.1:{}\"".format(public_url, port))

app = Flask(__name__)

# Создание и заполнение базы данных
def create_db():
    connection  = sqlite3.connect('present.db')
    cursor = connection.cursor()
    cursor.execute('''CREATE TABLE gifts (
                         name TEXT,
                         gift TEXT,
                         price INTEGER,
                         status TEXT)''')
    data = [
      ('Зеленкова Ирина', 'Кольцо', 6000, 'не куплен'),
      ('Зеленков Миша', 'Лего', 3000, 'куплен'),
      ('Зеленкова Зеленкова Вероника', 'Кукла', 2500, 'куплен'),
      ('Зеленков Александр', 'Туалетная вода', 6000, 'не куплен'),
      ('Лазарева Ксения', 'Пазл', 1500, 'куплен'),
      ('Лазарева Мария', 'Игрушка', 1500, 'куплен'),
      ('Савин Дмитрий', 'Машинка', 2000, 'не куплен'),
      ('Савин Владимир', 'Книга', 1500, 'не куплен'),
      ('Асеева Анна', 'Пудра', 2500, 'не куплен'),
      ('Ознобкин Денис', 'Набор', 2500, 'куплен')
   ]

    cursor.executemany('''INSERT INTO gifts VALUES (?, ?, ?, ?)''', data )
    connection.commit()
    connection.close()

# Получение данных о подарках из базы данных
def get_gifts():
    connection = sqlite3.connect('present.db')
    cursor = connection.cursor()
    cursor.execute('SELECT * FROM gifts')
    gifts = cursor.fetchall()
    connection.close()
    return gifts

@app.route('/')
def index():
    gifts = get_gifts()
    return render_template_string('''
    <!DOCTYPE html>
    <html lang="ru">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Список подарков</title>
    </head>
    <body>
        <h1>Список подарков</h1>
        <table border="1">
            <tr>

                <th>ФИО</th>
                <th>Название подарка</th>
                <th>Стоимость</th>
                <th>Статус</th>
            </tr>
            {% for gift in gifts %}
            <tr>
                <td>{{ gift[0] }}</td>
                <td>{{ gift[1] }}</td>
                <td>{{ gift[2] }}</td>
                <td>{{ gift[3] }}</td>

            </tr>
            {% endfor %}
        </table>
    </body>
    </html>
    ''', gifts=gifts)

if __name__ == '__main__':
    # Сначала создаем и заполняем БД
    create_db()
    # Запускаем приложение на порту 5000
    from google.colab import output
    output.serve_kernel_port_as_window(5000)
    app.run()