import json

import mysql.connector

# 连接到MySQL数据库
import numpy as np

conn = mysql.connector.connect(
    host="localhost",  # 主机地址
    user="root",  # 数据库用户名
    port="3306",          # 端口号
    password="123456",  # 数据库密码
    database="JobWanted"  # 数据库名称
)

# 创建游标对象
cursor = conn.cursor()

# 执行查询语句，获取所有行业类型，对应的平均月薪和其中的公司
cursor.execute("SELECT company_type, AVG(`Avg Monthly Salary`) FROM rec_inf GROUP BY company_type")
field_avg_salary_data = cursor.fetchall()

# 执行查询语句，获取所有城市值和对应的出现次数
cursor.execute("SELECT company_type, COUNT(*) FROM rec_inf GROUP BY company_type")
field_count_data = cursor.fetchall()

# 关闭游标
cursor.close()

# 关闭连接
conn.close()

# 提取不同行业值
field_type = [record[0] for record in field_avg_salary_data]

# 提取不同城市对应的平均月薪
avg_salaries = np.array([record[1] for record in field_avg_salary_data])

# 构建城市平均月薪的字典，将 Decimal 类型的值转换为浮点数
field_avg_salary_dict = {record[0]: float(record[1]) for record in field_avg_salary_data}

# 构建城市出现次数的字典
field_count_dict = {record[0]: record[1] for record in field_count_data}

# 将 NumPy 数组和字典储存到文件中
np.save('../data/field_type.npy', field_type)
with open('../data/field_avg_salary_dict.json', 'w') as f:
    json.dump(field_avg_salary_dict, f)
with open('../data/field_count_dict.json', 'w') as f:
    json.dump(field_count_dict, f)





