import json

import mysql.connector
import numpy as np


def load_data_from_database_by_field(field):
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="123456",
        database="JobWanted"
    )

    # 定义SQL查询
    sql_query = "SELECT job_title, city, experience, education, company, `Avg Monthly Salary` " \
                "FROM rec_inf where company_type = '" + field + "'"

    # 执行查询
    cursor = conn.cursor()
    cursor.execute(sql_query)

    # 获取结果
    data = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return data


def process_data(field):
    cities = np.load('../data/cities.npy')[::-1]
    experience = np.load('../data/experience.npy')[::-1]
    education = np.load('../data/education.npy')[::-1]

    # 从数据库加载数据
    data_from_db = load_data_from_database_by_field(field)
    # 将job_titles转换为字典，便于查找索引
    cities_dict = {city: index / len(cities) for index, city in enumerate(cities)}
    experience_dict = {exp: index / len(experience) for index, exp in enumerate(experience)}
    education_dict = {edu: index / len(education) for index, edu in enumerate(education)}

    # 将数据转换为NumPy数组
    # 初始化一个数组来保存数据
    data_array = np.zeros((len(data_from_db), 6), dtype=object)
    for i, row in enumerate(data_from_db):
        job_title = row[0]
        city = row[1]
        experience = row[2]
        education = row[3]
        company = row[4]
        avg_monthly_salary = row[5]

        city_index = cities_dict.get(city, -1)
        experience_index = experience_dict.get(experience, -1)
        education_index = education_dict.get(education, 0)

        data_array[i] = [job_title,
                         city_index * 0.24,
                         experience_index * 0.38,
                         education_index * 0.25,
                         company,
                         avg_monthly_salary]

    return data_array


def Jsonfy(field):
    res = process_data(field)
    # 提取不同职位名称
    job_title = [record[0] for record in res]
    # 获得地区得分
    city_score = [record[1] for record in res]
    # 获得经验评分
    exp_score = [record[2] for record in res]
    # 获得学历评分
    edu_score = [record[3] for record in res]
    # 获得公司信息
    company = [record[4] for record in res]
    # 获得平均薪资
    job_avg_salary = [record[5] for record in res]

    # 创建该职业字典 职位:工资,公司,三维指标(地区，经验，学历)
    job_dict = {record[0]: [record[5], record[4], [record[1], record[2], record[3]]] for record in res}
    return job_dict
