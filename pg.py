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
        if self.pool:
            await self.pool.close()
            print("连接池已关闭。")

    async def get_lesson_count(self):
        if not self.pool:
            print("错误：连接池不可用。")
            return None
            
        try:
            async with self.pool.acquire() as connection:
                count = await connection.fetchval("SELECT COUNT(*) FROM lesson_user")
                print(f"用户表的数据总量: {count}")
                return count
        except Exception as e:
            print(f"查询失败: {e}")
            return None

    async def create_lesson(self, param):
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
            return True
        except exceptions.UniqueViolationError as e:
            # 捕获主键或唯一约束冲突的常见错误
            print(f"插入失败：数据已存在或违反唯一约束。 {e}")
            return False
        except Exception as e:
            print(f"插入失败: {e}")
            return False
        
    async def get_need_to_send_session(self, current_hour):
        if not self.pool:
            print("错误：连接池不可用。")
            return False
        sql = "SELECT email,lessonName,lessonContent,process FROM lesson_user WHERE lessonTime @> $1 and finish == false;"

        param = [f'["{current_hour}"]']

        async with self.pool.acquire() as connection:
            try:
                result = await connection.fetch(sql, param)
                return result
            except Exception as e:
                print(f"查询失败: {e}")
                return None
