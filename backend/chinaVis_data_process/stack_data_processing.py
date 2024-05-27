import json
import mysql.connector
import numpy as np


def load_data_from_database_by_city(city):
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="123456",
        database="JobWanted"
    )

    try:
        # 定义SQL查询
        sql_query = """
            SELECT company_type, company, AVG(`Avg Monthly Salary`) AS avg_salary
            FROM rec_inf
            WHERE city LIKE %s
            GROUP BY company, company_type;
        """

        # 执行查询
        cursor = conn.cursor()
        cursor.execute(sql_query, (city + '%',))  # 在参数中使用模糊匹配符，仅匹配以 city 开头的城市名

        # 获取结果
        data = cursor.fetchall()
    finally:
        # 关闭游标和数据库连接
        cursor.close()
        conn.close()

    return data


def process_data(city):
    # 从数据库加载数据
    data_from_db = load_data_from_database_by_city(city)
    data_array = np.zeros((len(data_from_db), 3), dtype=object)
    for i, row in enumerate(data_from_db):
        company_type = row[0]
        company_name = row[1]
        avg_salary = float(row[2])

        data_array[i] = [company_type, company_name, avg_salary]

    return data_array


def StackDataJsonfy(city):
    res = process_data(city)
    stack_dict = {record[0]: [record[1], record[2]] for record in res}
    return stack_dict
