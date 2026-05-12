# The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20037820.svg)](https://doi.org/10.5281/zenodo.20037820)
[![Version](https://img.shields.io/badge/version-v2.1.0-blue)](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework/releases/tag/v2.1-final)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](requirements.txt)
[![Status](https://img.shields.io/badge/manuscript-submitted-green)]()

**Version:** v2.1.0 – Final Archival & Verification Release (May 2026)  
**Authors:** **Nick Barua¹·² and Robert J. Douglas¹·³**

¹ *AN Holdings CO., Nishinomiya, Japan* ² *Kobe Gakuin University, Kobe, Japan* ³ *Kobe Design Lab, Kobe, Japan*

---

<div align="center">
  <img src="Graphical_Abstract.png" width="900" alt="Graphical Abstract: Estimator Collapse Theory">
  <br><em>Graphical Abstract — Estimator Collapse Theory & The Sophistication Paradox</em>
</div>

---

## 📌 Overview

This repository provides the reference implementation and Monte Carlo validation suite for **Estimator Collapse Theory (ECT)**. ECT formalises a failure pathway in recursive state estimators where sub-threshold structured perturbations induce silent divergence while standard statistical health monitors report nominal behaviour.

The central finding is a binary **"Confidently Wrong"** result: under gate-compliant perturbations, the filter's self-reported uncertainty (CEP) remains stable whilst actual position error (TPE) diverges beyond operational requirements. This occurs because sub-threshold disturbances remain statistically indistinguishable from noise at the single-epoch level but accumulate systematically across updates.

> *Software companion to:* **"The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures"** — Submitted to *CEAS Aeronautical Journal* (2026).

---

## 📺 Visual Demonstration: Operational Failure Transition

https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework/blob/main/ECT_SMK_Conceptual_Overview.mp4.mp4

| Panel | Description |
|-------|-------------|
| **1 — Instability Number** | Contrasts actual estimation error with filter-reported covariance, illustrating divergence of estimator consistency. |
| **2 — Telemetry** | Real-time tracking of the Mission Kill Index (MKI); failure indicated as $\Gamma(t)$ crosses $\Gamma_{crit} = 6.5$. |
| **3 — CEP** | Expansion of Circular Error Probable relative to operational tolerance $R_L$. |
| **4 — Information Theory** | Systematic growth of Shannon Entropy $h(X)$, representing maximal uncertainty growth. |

---

## 🧪 3-D Monte Carlo Validation (v2.1)

The included `ECT_3D_Simulation_v141.py` reproduces all empirical results in Section II-E of the manuscript.

### **Reproducibility Parameters (Table I)**

| Parameter | Value |
| :--- | :--- |
| Monte Carlo runs ($N$) | 500 |
| Trajectory Duration | 1,200 s |
| Perturbation Amplitude ($A$) | 2.5 m |
| Perturbation Frequency ($\omega$) | 0.05 rad/sample |
| Innovation Gate ($\chi^2_3$) | 7.81 |
| Process Noise $Q$ | $\text{diag}(0.01, 0.01, 0.01, 0.001, 0.001, 0.001)$ |

### **Verified Results (v2.1 Anchor)**

| Metric | Result |
| :--- | :--- |
| **Instability Number $\Gamma(t) > \Gamma_{crit}$** | **100%** of runs |
| **NIS Gate Compliance** | **94.8%** |
| **Filter-reported CEP** | **2.43 m** (Invariant; $\Delta < 0.01$ m) |
| **True Position Error (TPE)** | **2.61 m → 4.27 m (+64%)** |
| **Mission Kill Index ($R_L = 3$ m)** | **MKI = 1.42** (Confirmed SMK) |

---

## 🧮 The Sophistication Paradox

The **Vulnerability Index $V_i$** formalises the paradox: increased sensor fusion improves nominal precision while simultaneously expanding the estimator's vulnerability surface.

$$V_i = \frac{N_{\text{sensors}} \times f_{\text{update}}}{R_{\text{hardening}}}$$

| System Class | $N_s$ | $f$ (Hz) | $R_h$ | $V_i$ (indicative) | Representative Example |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Single-Sensor INS Platform | 1 | 1 | 1.0 | $\approx 1$ | Short-range UAV |
| Dual-Modal Midcourse System | 3 | 10 | 1.0 | $\approx 30$ | MALE UAV |
| High-Precision Multi-Sensor | 4 | 20 | 1.2 | $\approx 67$ | HALE / Orbital Asset |
| **High-Dynamics Platform** | 4 | 80 | 1.0 | **$\approx 320$** | Re-entry Vehicle |

---

## 📊 Dimensionless Metrics

ECT introduces four primary metrics to quantify the estimator-collapse regime:

1.  **Estimator Instability Number $\Gamma(t)$** — Ratio of actual MSE under perturbation to nominal MSE.
2.  **Mission Kill Index (MKI)** — Ratio of expanded CEP to operational failure threshold $R_L$.
3.  **Information-to-Energy Yield $\eta_{info}$** — Efficiency of uncertainty generation measured via differential Shannon entropy.
4.  **Economic Reversal Ratio $R_{IE}$** — Cost-benefit metric for precision investment vs. vulnerability; reserved for Phase II.

---

## 📂 Repository Structure

* `ECT_3D_Simulation_v141.py`: Core Monte Carlo simulation engine.
* `Figures/`: High-resolution validation plots for $\Gamma(t)$, CEP divergence, and NIS compliance.
* `requirements.txt`: Python dependencies (NumPy, SciPy, Matplotlib).
* `LICENSE`: Apache 2.0.

---

## 🚀 Quick Start

```bash
git clone [https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git)
cd Estimator-Collapse-Theory-ECT-Framework
pip install -r requirements.txt
python ECT_3D_Simulation_v141.py
