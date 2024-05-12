import numpy as np
import pandas as pd

original_job_wanted_df = pd.read_excel('data/JobWanted.xlsx')


# 定义处理薪资字段的函数
def process_salary(salary_str):
    if '·' in salary_str:  # 如果格式为5-10K·13薪
        salary_parts = salary_str.split('·')
        salary_range = salary_parts[0]
        salary_range = salary_range.replace('K', '')
        months = int(salary_parts[1].split('薪')[0])
        min_salary = int(salary_range.split('-')[0]) * 1000
        max_salary = int(salary_range.split('-')[1]) * 1000
    elif '元/天' in salary_str:  # 如果格式为60-80元/天
        salary_range = salary_str.split('元/天')[0]
        min_salary = int(salary_range.split('-')[0]) * 22
        max_salary = int(salary_range.split('-')[1]) * 22
        months = 12
    elif '元/时' in salary_str:  # 如果格式为60-80元/时
        salary_range = salary_str.split('元/时')[0]
        min_salary = int(salary_range.split('-')[0]) * 8 * 22
        max_salary = int(salary_range.split('-')[1]) * 8 * 22
        months = 12
    elif '元/单' in salary_str:  # 如果格式为60-80元/单
        salary_range = salary_str.split('元/单')[0]
        min_salary = int(salary_range.split('-')[0]) * 50 * 22
        max_salary = int(salary_range.split('-')[1]) * 50 * 22
        months = 12
    elif '元/月' in salary_str:  # 如果格式为60-80元/月
        salary_range = salary_str.split('元/月')[0]
        min_salary = int(salary_range.split('-')[0])
        max_salary = int(salary_range.split('-')[1])
        months = 12
    elif '元/周' in salary_str:  # 如果格式为60-80元/周
        salary_range = salary_str.split('元/周')[0]
        min_salary = int(salary_range.split('-')[0]) * 4
        max_salary = int(salary_range.split('-')[1]) * 4
        months = 12
    else:  # 如果格式为5-10K
        salary_range = salary_str.replace('K', '')
        min_salary = int(float(salary_range.split('-')[0]) * 1000)
        max_salary = int(float(salary_range.split('-')[1]) * 1000)
        months = 12

    avg_salary = (min_salary + max_salary) / 2
    min_yearly_salary = min_salary * months
    max_yearly_salary = max_salary * months
    avg_yearly_salary = avg_salary * months

    return min_salary, max_salary, avg_salary, min_yearly_salary, max_yearly_salary, avg_yearly_salary


# 删除 salary 列
original_job_wanted_df = original_job_wanted_df[~original_job_wanted_df['salary'].str.contains("面议")]
original_job_wanted_df = original_job_wanted_df[~original_job_wanted_df['salary'].str.contains("以上")]
# 重新索引
original_job_wanted_df.reset_index(drop=True, inplace=True)
# 应用函数并生成新列
original_job_wanted_df['Min Monthly Salary'], original_job_wanted_df['Max Monthly Salary'], original_job_wanted_df[
    'Avg Monthly Salary'], original_job_wanted_df['Min Yearly Salary'], original_job_wanted_df[
    'Max Yearly Salary'], original_job_wanted_df['Avg Yearly Salary'] = zip(
    *original_job_wanted_df['salary'].apply(process_salary))
# 删除不满足条件的行
processed_job_wanted_df = original_job_wanted_df.dropna()
processed_job_wanted_df = processed_job_wanted_df[
    ~processed_job_wanted_df.apply(lambda row: row.astype(str).str.strip().eq('').any(), axis=1)]
# 添加有无奖金列
processed_job_wanted_df['Has Bonus'] = processed_job_wanted_df['salary'].str.contains("薪").astype(int)
processed_job_wanted_df.to_excel('processedJobWanted.xlsx', index=False)


