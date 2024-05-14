from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import json
import mysql.connector

app = Flask(__name__)
CORS(app)  # 允许跨域请求

"""
地区大图
"""


@app.route('/region_map_data', methods=['GET'])
def get_region_map_data():
    # 从文件中读取 NumPy 数组和字典数据
    cities = np.load('../data/city.npy')
    with open('../data/city_avg_salary_dict.json', 'r') as f:
        city_avg_salary_dict = json.load(f)
    with open('../data/city_count_dict.json', 'r') as f:
        city_count_dict = json.load(f)

    # 构建要发送给前端的数据字典
    region_map_data = {
        'cities': cities.tolist(),  # 转换为 Python 列表
        'city_avg_salary_dict': city_avg_salary_dict,
        'city_count_dict': city_count_dict
    }

    # 将数据转换为 JSON 格式并发送给前端
    return jsonify(region_map_data)


"""
行业大图
"""


@app.route('/field_map_data', methods=['GET'])
def get_field_map_data():
    # 从文件中读取 NumPy 数组和字典数据
    field_type = np.load('../data/field_type.npy')
    with open('../data/field_avg_salary_dict.json', 'r') as f:
        field_avg_salary_dict = json.load(f)
    with open('../data/field_count_dict.json', 'r') as f:
        field_count_dict = json.load(f)

    # 构建要发送给前端的数据字典
    field_map_data = {
        'field_type': field_type.tolist(),  # 转换为 Python 列表
        'field_avg_salary_dict': field_avg_salary_dict,
        'field_count_dict': field_count_dict
    }

    # 将数据转换为 JSON 格式并发送给前端
    return jsonify(field_map_data)


@app.route('/field_click', methods=['POST'])
def handle_filed_click():
    data = request.json
    field_name = data.get('field')
    # 点击函数实现
    print("City clicked:", field_name)
    return jsonify({'message': 'City click data received.'})


"""
职业对比大图
"""


@app.route('/check_box', methods=['POST'])
def send_checkbox_data():
    data = request.json
    type_name = data.get('typeName')
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )
    query = f"SELECT job_title FROM rec_inf WHERE company_type = '{type_name}'"
    cursor = conn.cursor()
    cursor.execute(query)

    results = cursor.fetchall()
    results = [item[0] for item in results]

    # 关闭数据库连接
    cursor.close()
    conn.close()
    return jsonify(results)


@app.route('/job_title_comparison', methods=['POST'])
def handle_job_title_comparison():
    data = request.json
    job_title = data.get('jobTitle', 'e0dd920456695914fed9481503e83b41xW')
    type_name = data.get('typeName')

    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )
    cursor = conn.cursor()

    # 查询城市、工作经验、教育程度和公司
    query = f"SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE job_title = '{job_title}'"
    cursor.execute(query)
    results_job = cursor.fetchall()

    query = f"SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE company_type = '{type_name}'"
    cursor.execute(query)
    results_title = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 将查询结果转换为 NumPy 矩阵
    # 创建空的 NumPy 数组来保存索引值和平均月薪
    matrix_job = np.empty((len(results_job), 3))
    matrix_title = np.empty((len(results_title), 3))

    cities = np.load('../data/cities.npy')[::-1]
    experience = np.load('../data/experience.npy')[::-1]
    education = np.load('../data/education.npy')[::-1]

    city_mapping = {city: index / len(cities) for index, city in enumerate(cities)}
    experience_mapping = {exp: index / len(experience) for index, exp in enumerate(experience)}
    education_mapping = {edu: index / len(education) for index, edu in enumerate(education)}

    # 将查询结果转换为索引值并填充到 NumPy 数组中
    for i, result in enumerate(results_job):
        city_index = city_mapping.get(result[0], -1)
        experience_index = experience_mapping.get(result[1], -1)
        education_index = education_mapping.get(result[2], -1)
        matrix_job[i] = [city_index, experience_index, education_index]
        salary = result[-1]

    for i, result in enumerate(results_title):
        city_index = city_mapping.get(result[0], -1)
        experience_index = experience_mapping.get(result[1], -1)
        education_index = education_mapping.get(result[2], -1)
        matrix_title[i] = [city_index, experience_index, education_index]

    matrix_title = np.mean(matrix_title, axis=0)
    print(matrix_title)

    return jsonify({'matrix_job': matrix_job.tolist(),
                    'matrix_title': matrix_title.tolist(),
                    'salary': salary})


"""
职业平行图获取数据
"""


@app.route('/job_parallel_all', methods=['POST'])
def handle_job_parallel():
    data = request.json
    companyType = data.get('companyType', 'type_BLfSmG')
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="123456",
        database="JobWanted"
    )
    cursor = conn.cursor()

    # 根据行业类型查询数据
    query_company_type = "SELECT job_title, city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE company_type = %s"
    cursor.execute(query_company_type, (companyType,))
    data = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    job_titles = np.load('../data/job_titles.npy')[::-1]
    cities = np.load('../data/cities.npy')[::-1]
    company = np.load('../data/company.npy')[::-1]
    experience = np.load('../data/experience.npy')[::-1]
    education = np.load('../data/education.npy')[::-1]

    # 将job_titles转换为字典，便于查找索引
    job_titles_dict = {title: index / len(job_titles) for index, title in enumerate(job_titles)}
    cities_dict = {city: index / len(cities) for index, city in enumerate(cities)}
    experience_dict = {exp: index / len(experience) for index, exp in enumerate(experience)}
    education_dict = {edu: index / len(education) for index, edu in enumerate(education)}
    company_dict = {comp: index / len(company) for index, comp in enumerate(company)}

    # 将数据转换为NumPy数组
    data_array = np.zeros((len(data), 5))  # 初始化一个数组来保存数据
    job_titles_list = []
    for i, row in enumerate(data):
        job_title = row[0]
        city = row[1]
        experience = row[2]
        education = row[3]
        company = row[4]
        avg_monthly_salary = row[5]

        city_index = cities_dict.get(city, -1)
        experience_index = experience_dict.get(experience, -1)
        education_index = education_dict.get(education, -1)
        company_index = company_dict.get(company, -1)

        job_titles_list.append(job_title)
        data_array[i] = [city_index,
                         experience_index,
                         education_index,
                         company_index,
                         avg_monthly_salary]

    # 返回结果
    print(data_array.tolist())
    return jsonify({"data": data_array.tolist(), "job": job_titles_list})

if __name__ == '__main__':
    app.run(debug=True)
