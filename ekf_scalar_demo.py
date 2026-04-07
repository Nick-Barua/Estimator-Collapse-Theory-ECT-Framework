import numpy as np

# --- Parameters from Section 2.5 ---
dt = 30.0 # [cite: 508]
F = np.array([[1.0, dt], [0.0, 1.0]]) # State transition [cite: 508]
Q = np.diag([0.01, 0.001]) # Process noise [cite: 509]
H = np.array([[0.0, 1.0]]) # Measurement matrix [cite: 509]
R_nom = 1.0 # Nominal measurement noise [cite: 510]
R_attacked = 1.3 # HPM-inflated noise [cite: 510]
chi2_threshold = 3.84 # 95% gate [cite: 512]

# --- Perturbation Logic from Section 3.1 ---
def get_perturbation(k):
    # Sub-threshold stellar bias [cite: 505, 511]
    return 1.2 * np.sin(0.05 * k)

# --- Core ECT Metrics ---
def calculate_gamma(mse_attacked, mse_nominal):
    # Estimator Instability Number [cite: 470]
    return mse_attacked / mse_nominal
