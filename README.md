# Estimator Collapse Theory (ECT) Framework

This repository provides the reference implementation and numerical validation scripts for the analytical framework and metrics formalised in:

> **Barua, N. (2026). Estimator Collapse Theory: Stochastic Mission Kill for Ballistic Interception.**

## 📌 Abstract
Estimator Collapse Theory (ECT) defines a new analytical regime in which ballistic mission kill emerges through state-estimator destabilisation rather than physical destruction. Unlike classical divergence analyses, this framework focuses on sub-threshold, gate-compliant perturbations that induce a "Confidently Wrong" failure regime.

## 🧪 Minimal Constructive Demonstration
The included `ekf_scalar_demo.py` reproduces the numerical results of Section 2.5 of the manuscript. It demonstrates that a calibrated innovation bias can drive the **Estimator Instability Number** $\Gamma(t)$ above the critical collapse threshold $\Gamma_{crit} \approx 6.5$ within a standard midcourse engagement window.

## 📊 Key Dimensionless Metrics
The framework introduces four primary metrics to quantify the estimator-collapse regime:
* **$\Gamma(t)$**: The Estimator Instability Number, defined as the ratio of actual Mean Squared Error (MSE) under perturbation to nominal MSE.
* **MKI**: The Mission Kill Index, defined as the ratio of the expanded Circular Error Probable (CEP) to the lethal radius $R_L$.
* **$\eta_{info}$**: The Information-to-Energy Yield, quantifying the uncertainty-generation efficiency of a perturbation mechanism.
* **$\mathcal{R}_{IE}$**: The Economic Reversal Ratio, comparing the amortised cost of a Stochastic Mission Kill (SMK) engagement to the unit cost of the threat.

## 🖼️ Validation Figures
High-resolution 600 DPI outputs from the analytical framework:

### Figure 3: Temporal Evolution of Γ(t)
![Figure 3](Figure3_Temporal_Evolution.png)
*Evolution of the instability number demonstrating the "Confidently Wrong" regime where true state error diverges while filter covariance remains deceptively bounded.*

### Figure 5: CEP Expansion Pathways
![Figure 5](Figure5_CEP_Expansion_Pathways.png)
*Comparative expansion pathways across threat classes, illustrating the "Sophistication Paradox".*

## 🚀 Quick Start
```bash
# Clone the repository
git clone [https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git)
cd Estimator-Collapse-Theory-ECT-Framework

# Install dependencies
pip install -r requirements.txt

# Run the EKF scalar demonstration
python ekf_scalar_demo.py
