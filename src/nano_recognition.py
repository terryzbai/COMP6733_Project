import numpy as np
from sklearn.model_selection import train_test_split
import gesture_recognition as gr

print('-----')
# Sigmoid 函数
def sigmoid(z):
    return 1 / (1 + np.exp(-z))

# 假设函数
def predict(X, w, b):
    return sigmoid(np.dot(X, w) + b)

# 成本函数
def compute_cost(X, y, w, b):
    m = X.shape[0]
    h = predict(X, w, b)
    cost = (-1/m) * np.sum(y * np.log(h) + (1 - y) * np.log(1 - h))
    return cost

# 梯度下降
def gradient_descent(X, y, w, b, alpha, num_iterations):
    m = X.shape[0]
    for i in range(num_iterations):
        h = predict(X, w, b)
        dw = (1/m) * np.dot(X.T, (h - y))
        db = (1/m) * np.sum(h - y)
        
        w -= alpha * dw
        b -= alpha * db
        
        if i % 100 == 0:
            cost = compute_cost(X, y, w, b)
            print(f"Iteration {i}: Cost {cost}")
    
    return w, b

X, y = gr.getDataset('./tb_data')


labels, counts = np.unique(y, return_counts=True)

# Print unique values and their counts
for label, count in zip(labels, counts):
    print(f'Value: {label}, Count: {count}')
# Split the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# 初始化参数
w = np.zeros(X_train.shape[1])
b = 0
alpha = 0.1
num_iterations = 1000

# 训练模型
w, b = gradient_descent(X_train, y_train, w, b, alpha, num_iterations)

# 测试模型


y_pred = predict(X_test, w, b) > 0.5
accuracy = np.mean(y_pred == y_test)

print(f"Test Accuracy: {accuracy}")
