import sqlite3

# 连接到数据库
conn = sqlite3.connect('back/instance/database.db')

# 创建游标
cursor = conn.cursor()

# 查看所有表
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# 查询某个表的数据
table_name = "score"  # 替换为你的表名
cursor.execute(f"SELECT * FROM {table_name};")
rows = cursor.fetchall()

# 打印数据
print(f"Data from {table_name}:")
for row in rows:
    print(row)

# 关闭连接
conn.close()
