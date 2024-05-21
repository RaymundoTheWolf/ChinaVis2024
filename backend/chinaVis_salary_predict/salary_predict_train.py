import numpy as np
import mysql.connector
import torch
from sklearn.model_selection import train_test_split
from xgboost import XGBClassifier  # Import XGBoost
from sklearn.metrics import accuracy_score
import joblib  # Used for saving and loading models

# Load data
job_titles = np.load('../data/job_titles.npy')[::-1]
cities = np.load('../data/cities.npy')[::-1]
company = np.load('../data/company.npy')[::-1]
experience = np.load('../data/experience.npy')[::-1]
education = np.load('../data/education.npy')[::-1]
company_type = np.load('../data/company_type.npy')[::-1]


# Load data from database
def load_data_from_database():
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )

    sql_query = """
        SELECT job_title, city, experience, education, company, company_type, `Avg Monthly Salary`
        FROM rec_inf
    """

    cursor = conn.cursor()
    cursor.execute(sql_query)

    data = cursor.fetchall()

    conn.close()

    return data


data_from_db = load_data_from_database()

# Convert job_titles to dictionary for lookup
job_titles_dict = {title: index / len(job_titles) for index, title in enumerate(job_titles)}
cities_dict = {city: index / len(cities) for index, city in enumerate(cities)}
experience_dict = {exp: index / len(experience) for index, exp in enumerate(experience)}
education_dict = {edu: index / len(education) for index, edu in enumerate(education)}
company_dict = {comp: index / len(company) for index, comp in enumerate(company)}
company_type_dict = {ctype: index / len(company_type) for index, ctype in enumerate(company_type)}

# Convert data to NumPy array
data_array = np.zeros((len(data_from_db), 6))
for i, row in enumerate(data_from_db):
    job_title = row[0]
    city = row[1]
    experience = row[2]
    education = row[3]
    company = row[4]
    company_type = row[5]
    avg_monthly_salary = row[6]

    job_title_index = job_titles_dict.get(job_title, -1)
    city_index = cities_dict.get(city, -1)
    experience_index = experience_dict.get(experience, -1)
    education_index = education_dict.get(education, -1)
    company_index = company_dict.get(company, -1)
    company_type_index = company_type_dict.get(company_type, -1)

    data_array[i] = [job_title_index,
                     city_index,
                     experience_index,
                     education_index,
                     company_index, avg_monthly_salary]

# Define salary segments
salary_segments = [(0, 5500), (5500, 7500), (7500, 10500), (10500, 300000)]

# Initialize label array
labels = np.zeros(len(data_from_db))

# Map 'Avg Monthly Salary' to corresponding label
for i, salary in enumerate(data_array[:, -1]):
    for j, segment in enumerate(salary_segments):
        if segment[0] <= salary < segment[1]:
            labels[i] = j
            break

# Split data_array and labels into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(data_array[:, :5], labels, test_size=0.2, random_state=42)

# Define and train XGBoost model
model = XGBClassifier(n_estimators=200, random_state=42, max_depth=6)  # Change model to XGBClassifier
model.fit(X_train, y_train)

# Save the model
joblib.dump(model, '../../../../VisProject/backend/chinaVis_salary_predict/xgboost_salary_predict_model.pkl')

# Evaluate the model
y_pred = model.predict(X_test)
test_accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {100 * test_accuracy:.2f}%")
