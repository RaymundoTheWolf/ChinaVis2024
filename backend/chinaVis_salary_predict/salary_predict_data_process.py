import mysql.connector
import numpy as np


def get_sorted_titles(input_column):
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="123456",
        database="JobWanted"
    )

    # 定义SQL查询
    sql_query = f"""
        SELECT {input_column}, AVG(`Avg Monthly Salary`) AS avg_monthly_salary
        FROM rec_inf
        GROUP BY {input_column}
        ORDER BY avg_monthly_salary DESC
    """

    # 执行查询
    cursor = conn.cursor()
    cursor.execute(sql_query)

    # 获取结果
    results = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    # 仅保留每个元素的第一个部分
    results = [result[0] for result in results]

    # 将结果转换为NumPy数组
    result_array = np.array(results)

    return result_array


# 调用函数并传入job_title作为参数
job_titles_for_model = get_sorted_titles('job_title')
cities_for_model = get_sorted_titles('city')
company_for_model = get_sorted_titles('company')
experience_for_model = get_sorted_titles('experience')
education_for_model = get_sorted_titles('education')
type_for_model = get_sorted_titles('company_type')

# 定义文件名
job_titles_file = '../data/job_titles.npy'
cities_file = '../data/cities.npy'
company_file = '../data/company.npy'
experience_file = '../data/experience.npy'
education_file = '../data/education.npy'
type_file = '../data/company_type.npy'

# 保存数组到文件
np.save(job_titles_file, job_titles_for_model)
np.save(cities_file, cities_for_model)
np.save(company_file, company_for_model)
np.save(experience_file, experience_for_model)
np.save(education_file, education_for_model)
np.save(type_file, type_for_model)