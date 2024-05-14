from flask import Flask, jsonify, request
from flask_cors import CORS
import numpy as np
import json
import mysql.connector
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
from sklearn.preprocessing import StandardScaler

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
    return jsonify(results[:1000])


def fetch_data(query, param):
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )
    cursor = conn.cursor()
    cursor.execute(query, (param,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


@app.route('/job_title_comparison', methods=['POST'])
def handle_job_title_comparison():
    data = request.json
    job_title = data.get('jobTitle', 'e0dd920456695914fed9481503e83b41xW')
    type_name = data.get('typeName')
    job_titles = data.get('jobList')

    query_job = "SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE job_title = %s"
    query_type = "SELECT city, experience, education, company, `Avg Monthly Salary` FROM rec_inf WHERE company_type = %s"

    with ThreadPoolExecutor() as executor:
        future_job = executor.submit(fetch_data, query_job, job_title)
        future_type = executor.submit(fetch_data, query_type, type_name)

        results_job = future_job.result()
        results_type = future_type.result()

    df_job = pd.DataFrame(results_job, columns=['city', 'experience', 'education', 'company', 'Avg Monthly Salary'])
    df_type = pd.DataFrame(results_type, columns=['city', 'experience', 'education', 'company', 'Avg Monthly Salary'])

    max_salary = df_type['Avg Monthly Salary'].max()
    min_salary = df_type['Avg Monthly Salary'].min()

    city_counts = df_type['city'].value_counts()
    city_name = city_counts.index.tolist()
    city_times = city_counts.values.tolist()

    cities = np.load('../data/cities.npy')[::-1]
    experience = np.load('../data/experience.npy')[::-1]
    education = np.load('../data/education.npy')[::-1]

    city_mapping = {city: index / len(cities) for index, city in enumerate(cities)}
    experience_mapping = {exp: index / len(experience) for index, exp in enumerate(experience)}
    education_mapping = {edu: index / len(education) for index, edu in enumerate(education)}

    df_job['city_index'] = df_job['city'].map(city_mapping).fillna(-1)
    df_job['experience_index'] = df_job['experience'].map(experience_mapping).fillna(-1)
    df_job['education_index'] = df_job['education'].map(education_mapping).fillna(-1)

    df_type['city_index'] = df_type['city'].map(city_mapping).fillna(-1)
    df_type['experience_index'] = df_type['experience'].map(experience_mapping).fillna(-1)
    df_type['education_index'] = df_type['education'].map(education_mapping).fillna(-1)

    matrix_job = df_job[['city_index', 'experience_index', 'education_index']].to_numpy()
    matrix_type = df_type[['city_index', 'experience_index', 'education_index']].to_numpy()

    scaler = StandardScaler()
    matrix_job_standard = scaler.fit_transform(matrix_job)
    matrix_type_standard = scaler.transform(matrix_type)

    job_score = np.dot(matrix_job_standard, matrix_type_standard.T)[0]
    sorted_indices = np.argsort(job_score)
    matrix_type = np.mean(matrix_type, axis=0)
    top_3_indices = sorted_indices[-4:][::-1]
    top_jobs = [job_titles[top_3_indices[1]], job_titles[top_3_indices[2]], job_titles[top_3_indices[3]]]

    return jsonify({
        'matrix_job': matrix_job.tolist(),
        'matrix_title': matrix_type.tolist(),
        'max_salary': int(max_salary),
        'min_salary': int(min_salary),
        'city_name': city_name[:10],
        'city_times': city_times[:10],
        'top_jobs': top_jobs,
        'salary': int(df_job['Avg Monthly Salary'][0])
    })


"""
职业平行图获取数据
"""


@app.route('/job', methods=['POST'])
def handle_job_parallel():
    data = request.json
    companyType = data.get('companyType', 'type_BLfSmG')
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
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
    return jsonify({"data": data_array.tolist(), "job": job_titles_list})


if __name__ == '__main__':
    app.run(debug=True)
