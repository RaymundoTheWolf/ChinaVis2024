import torch
import torch.nn as nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split
import mysql.connector
import numpy as np
from salary_predict_model import CNN_Salary_Predict, RNN_Salary_Predict, Transformer_Salary_Predict

job_titles = np.load('../data/job_titles.npy')[::-1]
cities = np.load('../data/cities.npy')[::-1]
company = np.load('../data/company.npy')[::-1]
experience = np.load('../data/experience.npy')[::-1]
education = np.load('../data/education.npy')[::-1]
company_type = np.load('../data/company_type.npy')[::-1]


def load_data_from_database():
    # 连接数据库
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        port="3306",
        password="a21340201152044",
        database="JobWanted"
    )

    # 定义SQL查询
    sql_query = """
        SELECT job_title, city, experience, education, company, company_type, `Avg Monthly Salary`
        FROM rec_inf
    """

    # 执行查询
    cursor = conn.cursor()
    cursor.execute(sql_query)

    # 获取结果
    data = cursor.fetchall()

    # 关闭数据库连接
    conn.close()

    return data


# 从数据库加载数据
data_from_db = load_data_from_database()

# 将job_titles转换为字典，便于查找索引
job_titles_dict = {title: index / len(job_titles) for index, title in enumerate(job_titles)}
cities_dict = {city: index / len(cities) for index, city in enumerate(cities)}
experience_dict = {exp: index / len(experience) for index, exp in enumerate(experience)}
education_dict = {edu: index / len(education) for index, edu in enumerate(education)}
company_dict = {comp: index / len(company) for index, comp in enumerate(company)}
company_type_dict = {ctype: index / len(company_type) for index, ctype in enumerate(company_type)}

# 将数据转换为NumPy数组
data_array = np.zeros((len(data_from_db), 7))  # 初始化一个数组来保存数据
for i, row in enumerate(data_from_db):
    job_title = row[0]
    city = row[1]
    experience = row[2]
    education = row[3]
    company = row[4]
    company_type = row[5]
    avg_monthly_salary = row[6]

    # 将每一列转换为索引位置/列的长度
    job_title_index = job_titles_dict.get(job_title, -1)
    city_index = cities_dict.get(city, -1)
    experience_index = experience_dict.get(experience, -1)
    education_index = education_dict.get(education, -1)
    company_index = company_dict.get(company, -1)
    company_type_index = company_type_dict.get(company_type, -1)

    data_array[i] = [job_title_index * 0.66,
                     city_index * 0.24,
                     experience_index * 0.38,
                     education_index * 0.25,
                     company_index * 0.63,
                     company_type_index * 0.32, avg_monthly_salary]

# 定义每个区间的最小和最大工资
salary_segments = [(0, 5000), (5000, 6500), (6500, 8500), (8500, 12500), (12500, 300000)]

# 初始化label数组
labels = np.zeros(len(data_from_db))

# 将每个`Avg Monthly Salary`的值映射到对应的标签
for i, salary in enumerate(data_array[:, -1]):
    for j, segment in enumerate(salary_segments):
        if segment[0] <= salary < segment[1]:
            labels[i] = j
            break

# 将data_array和labels转换为PyTorch张量
data_tensor = torch.tensor(data_array[:, :6], dtype=torch.float32)
label_tensor = torch.tensor(labels, dtype=torch.long)

# 划分训练集和测试集
train_data, test_data, train_labels, test_labels = train_test_split(data_tensor, label_tensor, test_size=0.2,
                                                                    random_state=42)

# 将数据封装成TensorDataset
train_dataset = TensorDataset(train_data, train_labels)
test_dataset = TensorDataset(test_data, test_labels)

# 定义模型
model = RNN_Salary_Predict(6, 8)

# 定义损失函数和优化器
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(params=model.parameters(), lr=0.0008)

# 定义超参数
num_epochs = 10

# 定义DataLoader
train_loader = DataLoader(train_dataset, batch_size=32, shuffle=True)
test_loader = DataLoader(test_dataset)

# 训练模型
running_loss = 0.0
correct = 0
total = 0

for epoch in range(num_epochs):
    model.train()
    times = 0
    for i, (inputs, labels) in enumerate(train_loader, 1):
        optimizer.zero_grad()
        outputs = model(inputs)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()

        _, predicted = torch.max(outputs, 1)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()
        running_loss += loss.item()
        times += 1
        if i % 2000 == 0:
            print(f"Epoch [{epoch + 1}/{num_epochs}], steps: {i}, Avg Loss: {loss.item():.4f}")

    avg_loss = running_loss / times
    accuracy = correct / total
    print(f"Epoch [{epoch + 1}/{num_epochs}], Avg Loss: {avg_loss:.4f}, Accuracy: {100 * accuracy:.2f}%")
    running_loss = 0.0
    correct = 0
    total = 0


model.eval()
test_loss = 0.0
correct = 0
total = 0

with torch.no_grad():
    for inputs, labels in test_loader:
        outputs = model(inputs)
        _, predicted = torch.max(outputs, 0)
        total += labels.size(0)
        correct += (predicted == labels).sum().item()

test_accuracy = correct / total

print(f"Test Acc: {100 * test_accuracy:.2f}%")