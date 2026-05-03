# The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures

**Version:** v1.4.1 – Submission-Ready 3D Release (May 2026)

This repository provides the reference implementation and numerical validation scripts for the analytical framework formalised in the paper:  
[cite_start]**"The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures"** (Barua, 2026)[cite: 973, 1215].

## 📌 Abstract
[cite_start]Estimator Collapse Theory (ECT) defines a formal regime in which navigation failure emerges through state-estimator destabilisation rather than physical destruction[cite: 977, 1214]. [cite_start]This framework identifies a class of sub-threshold perturbations—bounded measurement disturbances calibrated to remain within statistical gating thresholds—that can systematically corrupt the state estimate of an Extended Kalman Filter (EKF)[cite: 978, 1211]. [cite_start]This release provides empirical validation via 3D kinematic Monte Carlo simulation, demonstrating the "Confidently Wrong" failure mode where actual state error diverges whilst the onboard filter reports nominal consistency[cite: 982, 1223].

## 🏷️ Keywords
Estimator Collapse Theory; Stochastic Mission Kill; Multi-sensor Fusion; GNC Robustness; Systems Resilience; Kalman Filter Consistency; [cite_start]Circular Error Probable[cite: 983].

## 🧪 3D Monte Carlo Validation (v1.4.1)
[cite_start]The included `ECT_3D_Simulation_v141.py` reproduces the empirical results described in Section II-E of the manuscript[cite: 1063].
* [cite_start]**Setup:** 3D kinematic EKF (6-state vector: $[x, y, z, v_x, v_y, v_z]^T$) with dual-sensor modality (GNSS and Range)[cite: 1065, 1067].
* [cite_start]**Dynamics:** Constant-velocity model with sampling interval $\Delta t = 1$ s and process noise $Q = \text{diag}(0.01, 0.01, 0.01, 0.001, 0.001, 0.001)$[cite: 1065, 1066].
* [cite_start]**Sample Size:** $N = 500$ Monte Carlo runs over a 1,200-second trajectory[cite: 1070].
* **Findings:**
    * **$\Gamma(t)$ Collapse Rate:** 100% (Estimator instability threshold $\Gamma_{crit} = 6.5$ exceeded in all runs).
    * **NIS Gate Compliance:** 92–96% (Perturbations remained statistically inconspicuous to the 95% chi-squared gate).
    * [cite_start]**Outcome:** Empirical confirmation of the gate-compliant divergence regime in high-dimensional state space[cite: 1070, 1076].

## 🖼️ Validation Figures
* **Figure 2:** Temporal Evolution of $\Gamma(t)$ demonstrating 100% collapse rate.

* **Figure 4:** CEP expansion pathways showing median divergence of 7.8 m.

* **Figure 5:** NIS gate compliance confirming the stealthy nature of structured perturbations.

## 📊 Key Dimensionless Metrics
[cite_start]The framework introduces four primary metrics to quantify the estimator-collapse regime[cite: 979, 1215]:
* [cite_start]**$\Gamma(t)$**: **Estimator Instability Number**, defined as the ratio of actual Mean Squared Error (MSE) under perturbation to nominal MSE[cite: 1038].
* [cite_start]**MKI**: **Mission Kill Index**, defined as the ratio of the expanded Circular Error Probable (CEP) to the operational tolerance radius $R_L$[cite: 1050, 1051].
* [cite_start]**$\eta_{info}$**: **Information-to-Energy Yield**, quantifying the uncertainty-generation efficiency of a perturbation mechanism using differential Shannon entropy $\Delta h(X)$[cite: 1056, 1058].
* **$R_{IE}$**: **Economic Reversal Ratio**, comparing the amortised cost of an SMK engagement to the unit cost of the threat[cite: 1177, 1178].

## 🔗 Repository and Archival Record
The archived, citable version of this release is available on Zenodo:  
[cite_start]**DOI:** 10.5281/zenodo.19469720 [cite: 1071, 1227]

## 📖 Citation
If you use this work, please cite:  
Barua, N. (2026). *The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures*. [cite_start]Zenodo. https://doi.org/10.5281/zenodo.19469720 [cite: 1227]
