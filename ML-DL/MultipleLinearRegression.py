import math
import numpy as np

X_train = np.array([[2104, 5, 1, 45],
                    [1416, 3, 2, 40],
                    [ 852, 2, 1, 35]], dtype=float)
y_train = np.array([460, 232, 178], dtype=float)

mu_x  = X_train.mean(axis=0)
sig_x = X_train.std(axis=0, ddof=0)
X_norm = (X_train - mu_x) / sig_x

mu_y  = y_train.mean()
sig_y = y_train.std(ddof=0)
y_norm = (y_train - mu_y) / sig_y

def compute_cost(X, y, w, b):
    m = len(X)
    cost = 0.0
    for i in range(m): # can do without loop
        f_wb = b + X[i] @ w
        cost += (f_wb - y[i])**2
    return cost / (2*m)

def gradient_compute(X, y, w, b):
    m = len(X)
    dj_dw = np.zeros_like(w)
    dj_db = 0.0
    for i in range(m):
        f_wb = b + X[i] @ w
        err  = (f_wb - y[i])
        dj_dw += err * X[i]
        dj_db += err
    return dj_dw / m, dj_db / m

def gradient_descent(X, y, w, b, alpha, num_iters, compute_cost_, gradient_compute): 
    J_history = []
    lmd = 0
    m = len(X)
    for i in range(num_iters):
        dj_dw, dj_db = gradient_compute(X, y, w, b)
        w = w * (1-alpha*(lmd/m)) - alpha * dj_dw
        b = b - alpha * dj_db
        J = compute_cost_(X, y, w, b) # outputta lambda'nın etkisini görmüyoruz
        if i < 10000:
            J_history.append(J)
        if i % max(1, math.ceil(num_iters/10)) == 0:
            print(f"Iter {i:4}: J {J:0.2e}  |dw| {np.linalg.norm(dj_dw):.3e}  db {dj_db:.3e}  "
                  f"||w|| {np.linalg.norm(w):.3e}  b {b:.3e}")
    return w, b, J_history


m, n = X_norm.shape
w0 = np.zeros(n)
b0 = 0.0
alpha = 1e-8
num_iters = 100000

w_z, b_z, J_hist = gradient_descent(X_norm, y_norm, w0, b0, alpha, num_iters,
                                    compute_cost, gradient_compute)

print(f"(w', b') in z-space:\n  w'={w_z}\n  b'={b_z:.4f}")

w_orig = (sig_y / sig_x) * w_z
b_orig = mu_y - (w_orig * mu_x).sum() + sig_y * b_z

print(f"(w, b) in original units:\n  w={w_orig}\n  b={b_orig:.4f}")

def predict_raw(x_row):
    return float(x_row @ w_orig + b_orig)

x_example = np.array([1200, 3, 1, 40], dtype=float)
print(f"ŷ(x_example) = {predict_raw(x_example):.2f}")
J_final = compute_cost(X_norm, y_norm, w_z, b_z)

print("Final cost (normalized space):", J_final)
