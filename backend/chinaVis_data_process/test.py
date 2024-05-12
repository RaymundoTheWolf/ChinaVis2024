import json

with open('../data/field_avg_salary_dict.json', 'r') as f:
    field_avg_salary_dict = json.load(f)
print(len(field_avg_salary_dict))
