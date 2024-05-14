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


"""
多维度分析salary 3D散点图
"""


@app.route('/3d_scatter_data', methods=['GET'])
def get_3d_scatter_data():
    # 从文件中读取字典数据
    with open('../data/scatterDate/job_dict.json', 'r') as f:
        job_dict = json.load(f)
    # 构建要发送给前端的数据字典
    scatter_data = {
        'job_dict': job_dict
    }

    # 将数据转换为 JSON 格式并发送给前端
    return jsonify(scatter_data)


@app.route('/field_click', methods=['POST'])
def handle_filed_click():
    data = request.json
    field_name = data.get('field')
    # 点击函数实现
    """
        此处留有3D散点图的数据跳转
    """
    print("City clicked:", field_name)
    return jsonify({'message': 'City click data received.'})


"""
职业对比大图
"""


@app.route('/check_box', methods=['GET'])
def send_checkbox_data():
    job_titles = np.load('../data/job_titles.npy')
    check_box_data = {
        'job_titles': job_titles.tolist()[:100]
    }
    return jsonify(check_box_data)


@app.route('/job_title_comparison', methods=['POST'])
def handle_job_title_comparison():
    data = request.json
    job_title1 = data.get('jobTitle1', 'e0dd920456695914fed9481503e83b41xW')
    job_title2 = data.get('jobTitle2', '509fc26050f1433dd9baf56cfe91c111vF')

    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )
    cursor = conn.cursor()

    # 查询公司类型
    query_company_type = "SELECT company_type FROM rec_inf WHERE job_title = %s LIMIT 1"
    cursor.execute(query_company_type, (job_title1,))
    company_type1 = cursor.fetchone()[0]

    query_company_type = "SELECT company_type FROM rec_inf WHERE job_title = %s LIMIT 1"
    cursor.execute(query_company_type, (job_title2,))
    company_type2 = cursor.fetchone()[0]

    # 查询城市、工作经验、教育程度和公司
    query = f"SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE company_type = '{company_type1}'"
    cursor.execute(query)
    results_job1 = cursor.fetchall()

    query = f"SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE company_type = '{company_type2}'"
    cursor.execute(query)
    results_job2 = cursor.fetchall()

    # 关闭数据库连接
    cursor.close()
    conn.close()

    # 将查询结果转换为 NumPy 矩阵
    # 创建空的 NumPy 数组来保存索引值和平均月薪
    matrix_job1 = np.empty((len(results_job1), 5))
    matrix_job2 = np.empty((len(results_job2), 5))

    cities = np.load('../data/cities.npy')[::-1]
    company = np.load('../data/company.npy')[::-1]
    experience = np.load('../data/experience.npy')[::-1]
    education = np.load('../data/education.npy')[::-1]

    city_mapping = {city: index / len(cities) for index, city in enumerate(cities)}
    experience_mapping = {exp: index / len(experience) for index, exp in enumerate(experience)}
    education_mapping = {edu: index / len(education) for index, edu in enumerate(education)}
    company_mapping = {comp: index / len(company) for index, comp in enumerate(company)}

    # 将查询结果转换为索引值并填充到 NumPy 数组中
    for i, result in enumerate(results_job1):
        city_index = city_mapping.get(result[0], -1)
        experience_index = experience_mapping.get(result[1], -1)
        education_index = education_mapping.get(result[2], -1)
        company_index = company_mapping.get(result[3], -1)
        avg_salary = result[4]
        matrix_job1[i] = [city_index, experience_index, education_index, company_index, avg_salary]

    for i, result in enumerate(results_job2):
        city_index = city_mapping.get(result[0], -1)
        experience_index = experience_mapping.get(result[1], -1)
        education_index = education_mapping.get(result[2], -1)
        company_index = company_mapping.get(result[3], -1)
        avg_salary = result[4]
        matrix_job2[i] = [city_index, experience_index, education_index, company_index, avg_salary]

    # 返回结果
    ans1 = []
    ans2 = []
    correlations_job1 = np.corrcoef(matrix_job1[:, :4], matrix_job1[:, -1], rowvar=False)
    for i in range(len(correlations_job1)):
        ans1.append(correlations_job1[i][-1])
    correlations_job2 = np.corrcoef(matrix_job2[:, :4], matrix_job2[:, -1], rowvar=False)
    for i in range(len(correlations_job2)):
        ans2.append(correlations_job2[i][-1])
    return jsonify({'correlations_job1': ans1[:4], 'correlations_job2': ans2[:4]})


if __name__ == '__main__':
    app.run(debug=True)
