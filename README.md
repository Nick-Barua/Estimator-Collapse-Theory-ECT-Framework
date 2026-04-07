# Estimator Collapse Theory (ECT) Framework

This repository provides the reference implementation for **Estimator Collapse Theory (ECT)** and **Stochastic Mission Kill (SMK)** as formalised in:  
> *Barua, N. (2026). Estimator Collapse Theory: Stochastic Mission Kill for Ballistic Interception.*

## 📌 Abstract
[cite_start]ECT defines a new analytical regime in which ballistic mission failure emerges through estimator destabilisation[cite: 391]. [cite_start]Unlike classical divergence, this framework focuses on **gate-compliant perturbations** that induce a "Confidently Wrong" regime[cite: 441, 477].

## 🧪 Minimal Constructive Demonstration
[cite_start]The included `ekf_scalar_demo.py` reproduces the numerical results of Section 2.5, demonstrating that a sub-threshold bias can drive the **Estimator Instability Number** $\Gamma(t)$ above the critical threshold $\Gamma_{crit} \approx 6.5$ within a 15-minute midcourse engagement window [cite: 513-514].

## 📊 Key Dimensionless Metrics
* [cite_start]**$\Gamma(t)$**: Ratio of attacked MSE to nominal MSE[cite: 470].
* [cite_start]**MKI**: Mission Kill Index ($CEP(t) / R_L$)[cite: 486].
* [cite_start]**$\mathcal{R}_{IE}$**: Economic Reversal Ratio ($C_D / C_A$)[cite: 645].
