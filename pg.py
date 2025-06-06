import psycopg2
from psycopg2 import OperationalError

def create_connection():
    """创建 PostgreSQL 数据库连接"""
    try:
        connection = psycopg2.connect(
            host="localhost", 
            database="hobby-lib",
            user="myuser",
            password="password", 
            port="5432" 
        )
        print("连接成功")
        return connection
    except OperationalError as e:
        print(f"连接失败: {e}")
        return None

def get_user_count(connection):
    try:
        cursor = connection.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        count = cursor.fetchone()[0]
        print(f"用户表的数据总量: {count}")
        return count
    except Exception as e:
        print(f"查询失败: {e}")
        return None
    finally:
        cursor.close()

def pgInit():
    connection = create_connection()
    if connection:
        get_user_count(connection)
        connection.close()
        print("连接已关闭")