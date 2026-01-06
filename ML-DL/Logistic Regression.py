import numpy as np

def sigmoid(z):
    g = 1/(1+np.exp(-z))
    return g

def sigmoid_function(w,x,b):
    m = x.shape[0]
    sigmoid_values = []
    z_values = []   
    for i in range(m):
        z = x[i]@w + b
        sigmoid_f = 1/(1+np.exp(-z))
        sigmoid_values.append(sigmoid_f)
        z_values.append(z)
    return z_values,sigmoid_values

def sigmoid_function_no_loop(w,x,b): #same result but better opt since its fully vectorized
    z = x @ w + b
    sigmoid_f = 1/(1+np.exp(-z))
    return z,sigmoid_f

def gradiant_compute(x,y,w,b):
    m = x.shape[0]
    z = x @ w + b
    f_wb = sigmoid(z)
    error = f_wb -y
    dj_dw = (x.T @ error)/m
    dj_db = error.mean()
    return dj_dw, dj_db


def compute_cost(w,b,x,y):
    m = x.shape[0]
    cost = 0
    z = x @ w + b
    f_wb = sigmoid(z)
    cost = -y @ np.log(f_wb) - (1 - y) @ np.log(1 - f_wb)
    cost = cost/m
    return cost

def gradiant_descent(x,y,w,b,alpha,num_iter,lmd):
    j_history = []
    m = x.shape[0]
    for i in range(num_iter):
        dj_dw, dj_db = gradiant_compute(x,y,w,b)
        w = w - alpha * (dj_dw + (lmd / m) * w)
        b = b - alpha * dj_db
        cost = compute_cost(w, b, x, y) + (lmd / (2 * m)) * np.sum(w ** 2)
        j_history.append(cost)
    return w, b, j_history

def predict(X, w, b, threshold=0.5):
    z = X @ w + b
    probs = sigmoid(z)
    preds = np.where(probs >= threshold, "Malignant", "Safe")
    return preds, probs

alpha = 1e-4
w = np.array([0.1,0.2,0.3])
b = 1
x = np.array([[1,2,3],[4,5,6]])
y = np.array([0,1])


print("Initial cost:", compute_cost(w, b, x, y))
w_f, b_f, J_hist = gradiant_descent(x, y, w, b, alpha, 10000,1)
print("Final cost:", J_hist[-1])
print("w:", w_f, "b:", b_f)

preds, probs = predict(x, w_f, b_f)
print("Predicted classes:", preds)
print("Predicted probabilities for being malignant for each data points:", probs)

