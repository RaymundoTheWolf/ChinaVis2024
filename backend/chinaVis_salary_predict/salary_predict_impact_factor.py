import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.metrics import mean_absolute_error

# 加载数据
factor_array = np.load('../data/factor_array.npy')

# 提取前六列和最后一列
X = factor_array[:, :6]  # 自变量
y = factor_array[:, -1]  # 因变量

# 统计每一列的不同值个数
unique_counts = np.apply_along_axis(lambda x: len(np.unique(x)), axis=0, arr=X)

print("每一列的不同值个数:", unique_counts)

# 创建线性回归模型
model = LinearRegression()

# 拟合模型
model.fit(X, y)

# 打印回归系数
print("回归系数:", model.coef_)

# 打印截距
print("截距:", model.intercept_)

# 进行预测
y_pred = model.predict(X)

# 计算R^2值
r_squared = r2_score(y, y_pred)
print("R^2 值:", r_squared)

# 计算MAE
mae = mean_absolute_error(y, y_pred)
print("平均绝对误差 (MAE):", mae)

# 计算相关系数
correlations = np.corrcoef(factor_array[:, :6], factor_array[:, -1], rowvar=False)

# 打印相关系数
print("各自变量与因变量的相关系数：")
for i, col_name in enumerate(["自变量1", "自变量2", "自变量3", "自变量4", "自变量5", "自变量6"]):
    print(f"{col_name}:", correlations[i][-1])

coef_sum = 0
for i in model.coef_:
    coef_sum += np.fabs(i)

impact_coef = []
for i in model.coef_:
    impact_coef.append(np.fabs(i) / coef_sum)
print(impact_coef)