import numpy as np

def run_simulation():
    # --- 1. Parameters from Manuscript Section 2.5 ---
    dt = 30.0  # Time step
    F_k = np.array([[1.0, dt], [0.0, 1.0]])  # Dynamics
    Q = np.diag([0.01, 0.001])  # Process noise
    H = np.array([[0.0, 1.0]])  # Velocity measurement
    
    R_nom = 1.0  # Nominal noise
    R_attacked = 1.3  # HPM-inflated noise
    
    P_0 = np.diag([1.0, 0.1])  # Initial covariance
    x_true = np.array([[0.0], [100.0]])  # Initial state
    
    # Simulation settings
    steps = 30  # ~15 minutes of coast 
    trials = 1000  # Monte Carlo iterations 
    
    mse_nominal = np.zeros(steps)
    mse_attacked = np.zeros(steps)

    print(f"Running ECT Validation ({trials} Monte Carlo iterations)...")

    for _ in range(trials):
        x_nom = x_true.copy()
        x_atk = x_true.copy()
        P_nom = P_0.copy()
        P_atk = P_0.copy()
        curr_x_true = x_true.copy()

        for k in range(steps):
            # True State Update
            curr_x_true = F_k @ curr_x_true + np.random.multivariate_normal([0, 0], Q).reshape(2, 1)

            # --- Nominal Filter ---
            # Predict
            x_nom = F_k @ x_nom
            P_nom = F_k @ P_nom @ F_k.T + Q
            # Update
            z_nom = H @ curr_x_true + np.random.normal(0, np.sqrt(R_nom))
            y_nom = z_nom - H @ x_nom
            S_nom = H @ P_nom @ H.T + R_nom
            K_nom = P_nom @ H.T / S_nom
            x_nom = x_nom + K_nom @ y_nom
            P_nom = (np.eye(2) - K_nom @ H) @ P_nom
            mse_nominal[k] += (curr_x_true[0, 0] - x_nom[0, 0])**2

            # --- Attacked Filter (ECT Regime) ---
            # Predict
            x_atk = F_k @ x_atk
            P_atk = F_k @ P_atk @ F_k.T + Q
            # Update with Sub-threshold Bias
            delta_z = 1.2 * np.sin(0.05 * k) 
            z_atk = H @ curr_x_true + np.random.normal(0, np.sqrt(R_attacked)) + delta_z
            y_atk = z_atk - H @ x_atk
            S_atk = H @ P_atk @ H.T + R_attacked
            K_atk = P_atk @ H.T / S_atk
            x_atk = x_atk + K_atk @ y_atk
            P_atk = (np.eye(2) - K_atk @ H) @ P_atk
            mse_attacked[k] += (curr_x_true[0, 0] - x_atk[0, 0])**2

    # Average results
    mse_nominal /= trials
    mse_attacked /= trials

    # --- 2. Result Verification ---
    k_target = 26 # t ≈ 13 minutes
    gamma_t = mse_attacked[k_target] / mse_nominal[k_target]
    
    print("-" * 30)
    print(f"Results at t ≈ 13 minutes (Step {k_target}):")
    print(f"Nominal MSE: {mse_nominal[k_target]:.2f}")
    print(f"Attacked MSE: {mse_attacked[k_target]:.2f}")
    print(f"Gamma(t): {gamma_t:.2f}")
    print("-" * 30)
    
    # Validation against critical threshold defined in Section 2.5
    if gamma_t > 6.5:
        print(f"SUCCESS: Gamma({gamma_t:.2f}) > Gamma_crit(6.5).")
        print("Result confirms Estimator Collapse Theory (Section 2.5).")
    else:
        print("WARNING: Result does not reach the collapse threshold.")

if __name__ == "__main__":
    run_simulation()
