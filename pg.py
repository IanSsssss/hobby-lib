import psycopg2
from psycopg2 import OperationalError

class PostgreSQLDatabase:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.connection = None

    def create_connection(self):
        try:
            self.connection = psycopg2.connect(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("连接成功")
        except OperationalError as e:
            print(f"连接失败: {e}")
            self.connection = None

    def close_connection(self):
        if self.connection:
            self.connection.close()
            print("连接已关闭")

    def get_lesson_count(self):
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT COUNT(*) FROM lesson_user")
            count = cursor.fetchone()[0]
            print(f"用户表的数据总量: {count}")
            return count
        except Exception as e:
            print(f"查询失败: {e}")
            return None
        finally:
            cursor.close()

    def create_lesson(self, param):
        try:
            cursor = self.connection.cursor()
            cursor.execute(
                "INSERT INTO lesson_user (email, lessonName, lessonContent, process, finish, lessonTime) "
                "VALUES (%s, %s, %s, %s, %s, %s)",
                (
                    param['email'],
                    param['lessonName'],
                    param['lessonContent'],
                    param['process'],
                    param['finish'],
                    param['lessonTime']
                )
            )
            self.connection.commit()
            print("数据插入成功")
        except Exception as e:
            print(f"插入失败: {e}")
            self.connection.rollback()
        finally:
            cursor.close()

# def main():
#     # 数据库配置
#     db_config = {
#         "host": "localhost",
#         "database": "hobby-lib",
#         "user": "myuser",
#         "password": "password",
#         "port": "5432"
#     }

#     # 初始化数据库对象
#     db = PostgreSQLDatabase(**db_config)

#     # 创建连接
#     db.create_connection()

#     if db.connection:
#         # 查询 lesson_user 表的数据总量
#         db.get_lesson_count()

#         # 插入一条数据
#         lesson_data = {
#             "email": "123@qq.com",
#             "lessonName": "modern_art",
#             "lessonContent": [['xxx'], ['xxx'], ['xxx']],
#             "process": [0, 1],
#             "finish": True,
#             "lessonTime": 18
#         }
#         db.create_lesson(lesson_data)

#         # 关闭连接
#         db.close_connection()