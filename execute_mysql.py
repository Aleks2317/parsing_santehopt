import mysql.connector
from mysql.connector import Error


# def create_connection(host_name, user_name, user_password):
#     """
#     1 - устанавливает соединение с базой данный
#     2 - Выполнение запроса для создания БД
#     """
#     connection = None
#
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             password=user_password
#         )
#
#         print("Connection to MySQL DB successful")
#
#     except Error as e:
#         print(f"The error '{e}' occurres")
#
#     return connection
# print('ok')
# connection = create_connection("192.168.1.4", "alex", "3EDCxzaq!")


# def create_database(connection, query):
#     """
#     создание базы данных
#
#     """
#     cursor = connection.cursor()
#     try:
#         cursor.execute(query)
#         print("Database created successfully")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
# create_database_query = "CREATE DATABASE sm_app"
# create_database(connection, create_database_query)
#
#
# def create_connection(host_name, user_name, user_password, db_name):
#
#     """
#     обращение к конкретной базе данных
#
#     """
#     connection = None
#     try:
#         connection = mysql.connector.connect(
#             host=host_name,
#             user=user_name,
#             passwd=user_password,
#             database=db_name
#         )
#         print("Connection to MySQL DB successful")
#     except Error as e:
#         print(f"The error '{e}' occurred")
#
#     return connection
#
connection = create_connection("192.168.1.4", "alex", "3EDCxzaq!", "sm_app")


# создание таблицы

def execute_query(connection, query):
    cursor = connection.cursor()
    try:
        cursor.execute(query)
        connection.commit()
        print("Query executed successfully")
    except Error as e:
        print(f"The error '{e}' occurred")


# Описываем таблицу users

create_users_table = """
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT,
  name TEXT NOT NULL,
  age INT,
  gender TEXT,
  nationality TEXT,
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

execute_query(connection, create_users_table)

create_posts_table = """
CREATE TABLE IF NOT EXISTS posts (
  id INT AUTO_INCREMENT,
  title TEXT NOT NULL,
  description TEXT NOT NULL,
  user_id INTEGER NOT NULL,
  FOREIGN KEY fk_user_id (user_id) REFERENCES users(id),
  PRIMARY KEY (id)
) ENGINE = InnoDB
"""

execute_query(connection, create_posts_table)