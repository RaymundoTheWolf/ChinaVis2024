import json

import mysql.connector

# 连接到MySQL数据库
import numpy as np

conn = mysql.connector.connect(
    host="localhost",  # 主机地址
    user="root",  # 数据库用户名
    port="3306",          # 端口号
    password="",  # 数据库密码
    database="JobWanted"  # 数据库名称
)

# 创建游标对象
cursor = conn.cursor()

# 执行查询语句，获取所有城市值和对应的平均月薪
cursor.execute("SELECT city, AVG(`Avg Monthly Salary`) FROM rec_inf GROUP BY city")
city_avg_salary_data = cursor.fetchall()

# 执行查询语句，获取所有城市值和对应的出现次数
cursor.execute("SELECT city, COUNT(*) FROM rec_inf GROUP BY city")
city_count_data = cursor.fetchall()

# 关闭游标
cursor.close()

# 关闭连接
conn.close()

# 提取不同城市值
cities = [record[0] for record in city_avg_salary_data]

# 提取不同城市对应的平均月薪
avg_salaries = np.array([record[1] for record in city_avg_salary_data])

# 构建城市平均月薪的字典，将 Decimal 类型的值转换为浮点数
city_avg_salary_dict = {record[0]: float(record[1]) for record in city_avg_salary_data}

# 构建城市出现次数的字典
city_count_dict = {record[0]: record[1] for record in city_count_data}

# 将 NumPy 数组和字典储存到文件中
np.save('../data/city.npy', cities)
with open('../data/city_avg_salary_dict.json', 'w') as f:
    json.dump(city_avg_salary_dict, f)
with open('../data/city_count_dict.json', 'w') as f:
    json.dump(city_count_dict, f)





