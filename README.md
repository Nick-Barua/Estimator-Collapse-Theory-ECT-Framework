# The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.20037820.svg)](https://doi.org/10.5281/zenodo.20037820)
[![Version](https://img.shields.io/badge/version-v2.1.0-blue)](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework/releases/tag/v2.1-final)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8%2B-blue)](requirements.txt)
[![Status](https://img.shields.io/badge/manuscript-submitted-green)]()

**Version:** v2.1.0 – Final Archival & Verification Release (May 2026)  
**Authors:** **Nick Barua¹·² and Robert J. Douglas¹·³**

[cite_start]¹ *AN Holdings CO., Nishinomiya, Japan* ² *Kobe Gakuin University, Kobe, Japan* ³ *Kobe Design Lab, Kobe, Japan* [cite: 354, 355, 356, 357]

---

<div align="center">
  <img src="Graphical_Abstract.png" width="900" alt="Graphical Abstract: Estimator Collapse Theory">
  <br><em>Graphical Abstract — Estimator Collapse Theory & The Sophistication Paradox</em>
</div>

---

## 📌 Overview

[cite_start]This repository provides the reference implementation and Monte Carlo validation suite for **Estimator Collapse Theory (ECT)** — a systems-theoretic framework characterising how state-estimation destabilisation constitutes a formal failure pathway in precision autonomous navigation architectures[cite: 360, 361].

[cite_start]The central finding is a binary **"Confidently Wrong"** result: under gate-compliant perturbations, the filter's self-reported uncertainty (CEP) remains stable whilst actual position error (TPE) diverges beyond operational requirements[cite: 366]. [cite_start]This occurs because sub-threshold disturbances remain statistically indistinguishable from noise at the single-epoch level but accumulate systematically across updates[cite: 381, 382].

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

## 🧮 The Sophistication Paradox

ECT formalises the **Sophistication Paradox** via the Vulnerability Index $V_i$:

$$V_i = \frac{N_{\text{sensors}} \times f_{\text{update}}}{R_{\text{hardening}}}$$

[cite_start]This captures a counter-intuitive relationship: advanced multi-sensor fusion architectures improve nominal precision while simultaneously expanding the estimator's vulnerability surface[cite: 364, 384].

<div align="center">
  <img src="Figure_1.png" width="800" alt="EKF Loop and Attack Points">
  [cite_start]<br><em>Fig 1. Extended Kalman Filter loop and principal perturbation entry points (A: Measurement Bias, B: Covariance Inflation, C: GNSS Denial)[cite: 413, 414, 415, 416].</em>
</div>

| System Class | $N_s$ | $f$ (Hz) | $R_h$ | $V_i$ (indicative) | Representative Example |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Single-Sensor INS Platform | 1 | 1 | 1.0 | $\approx 1$ | [cite_start]Short-range UAV [cite: 549] |
| Dual-Modal Midcourse System | 3 | 10 | 1.0 | $\approx 30$ | [cite_start]MALE UAV [cite: 549] |
| High-Precision Multi-Sensor | 4 | 20 | 1.2 | $\approx 67$ | [cite_start]HALE / Orbital Asset [cite: 549] |
| **High-Dynamics Platform** | 4 | 80 | 1.0 | **$\approx 320$** | [cite_start]Re-entry Vehicle [cite: 549] |

---

## 🧪 3-D Monte Carlo Validation (v2.1)

[cite_start]The included `ECT_3D_Simulation_v141.py` reproduces all empirical results in Section II-E of the manuscript[cite: 457, 459].

### [cite_start]**Reproducibility Parameters (Table I)** [cite: 481, 482]

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
| **Instability Number $\Gamma(t) > \Gamma_{crit}$** | [cite_start]**100%** of runs [cite: 465] |
| **NIS Gate Compliance** | [cite_start]**94.8%** [cite: 466] |
| **Filter-reported CEP** | [cite_start]**2.43 m** (Invariant; $\Delta < 0.01$ m) [cite: 468] |
| **True Position Error (TPE)** | [cite_start]**2.61 m → 4.27 m (+64%)** [cite: 469] |
| **Mission Kill Index ($R_L = 3$ m)** | [cite_start]**MKI = 1.42** (Confirmed SMK) [cite: 476] |

<div align="center">
  <img src="Figure_2.png" width="900" alt="Estimator Instability Evolution">
  <br><em>Fig 2. Temporal evolution of the Estimator Instability Number Γ(t). [cite_start]Panel D confirms the SMK condition while internal covariance remains bounded[cite: 437, 438, 439].</em>
</div>

<div align="center">
  <img src="Figure_3.png" width="900" alt="Gamma(t) Distribution">
  [cite_start]<br><em>Fig 3. 100% any-time exceedance of Γ_crit = 6.5 across N=500 runs[cite: 558, 559, 560].</em>
</div>

<div align="center">
  <img src="Figure_4.png" width="900" alt="CEP Expansion">
  [cite_start]<br><em>Fig 4. The "Confidently Wrong" signature: filter-reported CEP (red) remains invariant while TPE (blue dashed) diverges[cite: 574, 576, 578].</em>
</div>

---

## 📂 Repository Structure

* [cite_start]`ECT_3D_Simulation_v141.py`: Core Monte Carlo simulation engine[cite: 459, 479].
* `Figures/`: High-resolution validation plots (Figures 1–4).
* `requirements.txt`: Python dependencies (NumPy, SciPy, Matplotlib).
* `LICENSE`: Apache 2.0.

---

## 🚀 Quick Start

```bash
git clone [https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git)
cd Estimator-Collapse-Theory-ECT-Framework
pip install -r requirements.txt
python ECT_3D_Simulation_v141.py
