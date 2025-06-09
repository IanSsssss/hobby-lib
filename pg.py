import asyncpg
from asyncpg import exceptions

class AsyncPgDB:
    def __init__(self, host, database, user, password, port):
        self.host = host
        self.database = database
        self.user = user
        self.password = password
        self.port = port
        self.pool = None # asyncpg 通常使用连接池以获得更佳性能

    async def create_pool(self):
        """创建数据库连接池。"""
        try:
            self.pool = await asyncpg.create_pool(
                host=self.host,
                database=self.database,
                user=self.user,
                password=self.password,
                port=self.port
            )
            print("数据库连接池创建成功。")
        except exceptions.InvalidPasswordError as e:
            print(f"连接失败：密码错误或用户不存在。 {e}")
            self.pool = None
        except OSError as e:
            print(f"连接失败：无法连接到主机 {self.host}:{self.port}。请检查网络或数据库服务状态。 {e}")
            self.pool = None
        except Exception as e:
            print(f"创建连接池时发生未知错误: {e}")
            self.pool = None
            
    async def close_pool(self):
        """关闭数据库连接池。"""
        if self.pool:
            await self.pool.close()
            print("连接池已关闭。")

    async def get_lesson_count(self):
        """获取 lesson_user 表中的数据总量。"""
        if not self.pool:
            print("错误：连接池不可用。")
            return None
            
        try:
            # 从连接池获取一个连接
            async with self.pool.acquire() as connection:
                # fetchval可以直接获取单个值，非常方便
                count = await connection.fetchval("SELECT COUNT(*) FROM lesson_user")
                print(f"用户表的数据总量: {count}")
                return count
        except Exception as e:
            print(f"查询失败: {e}")
            return None

    async def create_lesson(self, param):
        """
        在 lesson_user 表中插入一条新数据。
        注意：asyncpg 使用 $1, $2 等作为参数占位符。
        """
        if not self.pool:
            print("错误：连接池不可用。")
            return False
            
        sql = (
            "INSERT INTO lesson_user (email, lessonName, lessonContent, process, finish, lessonTime) "
            "VALUES ($1, $2, $3, $4, $5, $6)"
        )
        try:
            async with self.pool.acquire() as connection:
                await connection.execute(
                    sql,
                    param['email'],
                    param['lessonName'],
                    param['lessonContent'],
                    param['process'],
                    param['finish'],
                    param['lessonTime']
                )
            print("数据插入成功。")
            return True
        except exceptions.UniqueViolationError as e:
            # 捕获主键或唯一约束冲突的常见错误
            print(f"插入失败：数据已存在或违反唯一约束。 {e}")
            return False
        except Exception as e:
            print(f"插入失败: {e}")
            return False