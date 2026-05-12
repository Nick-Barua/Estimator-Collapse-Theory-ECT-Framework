# The Sophistication Paradox: Estimator Collapse Theory (ECT) Framework

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20132174-blue?style=flat-square)](https://doi.org/10.5281/zenodo.20132174)
[![Version](https://img.shields.io/badge/version-v2.1.0-blue)](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework/releases/tag/v2.1-final)
[![License](https://img.shields.io/badge/license-Apache%202.0-green)](LICENSE)

**Version:** v2.1.0 – Final Archival & Verification Release (May 2026)  
**Authors:** Nick Barua¹·² and Robert J. Douglas¹·³

¹ *AN Holdings CO., Nishinomiya, Japan* | ² *Kobe Gakuin University, Kobe, Japan* | ³ *Kobe Design Lab, Kobe, Japan*

---

<div align="center">
  <img src="Graphical_Abstract.png" width="900" alt="Graphical Abstract — Estimator Collapse Theory and The Sophistication Paradox">
  <br><em>Graphical Abstract — Estimator Collapse Theory &amp; The Sophistication Paradox</em>
</div>

---

## Overview

This repository provides the reference implementation and Monte Carlo validation suite for **Estimator Collapse Theory (ECT)**. ECT formalises a failure pathway in recursive state estimators — specifically the Extended Kalman Filter (EKF) — where sub-threshold structured perturbations induce silent divergence whilst standard statistical health monitors report nominal behaviour.

ECT identifies a class of perturbations bounded within the chi-squared innovation gate that are statistically indistinguishable from legitimate sensor noise at the single-epoch level, yet accumulate systematically across successive filter updates to corrupt the state estimate beyond operational tolerance. The resulting condition — where the filter reports high confidence in a position estimate that has become operationally meaningless — is termed **Estimator Collapse**. The mission-level consequence is a **Stochastic Mission Kill (SMK)**.

> *Software companion to:* **"The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures"** — Barua, N. & Douglas, R. J. Submitted to *CEAS Aeronautical Journal* (2026).

---

## The "Confidently Wrong" Signature

The central finding is a structural decoupling between a filter's self-reported uncertainty and physical reality. Under gate-compliant perturbations:

- The filter's internal covariance — and the CEP derived from it — remains effectively **invariant**
- The actual trajectory error (True Position Error, TPE) **diverges** beyond operational tolerance
- The filter's health monitor registers **no anomaly** throughout

This is the **"Confidently Wrong"** regime: the system is certain, and wrong, simultaneously.

<div align="center">
  <img src="Figures/Figure_4.png" width="850" alt="The Confidently Wrong Signature — Filter-reported CEP vs True Position Error">
  <br><em>Fig. 4. The "Confidently Wrong" signature. Filter-reported CEP (red) remains effectively invariant at 2.43 m whilst TPE (blue dashed) diverges to 4.37 m (+67%). Panel (c) confirms |ΔCEP| &lt; 0.01 m. Panel (d): terminal TPE distribution across all N = 500 runs. 3-D dual-sensor kinematic EKF, v2.1.</em>
</div>

---

## Verified Results (v2.1 Archival Anchor)

The following results were generated using Master Seed 42 over N = 500 paired-seed runs across a 1,200-second trajectory. They constitute the locked empirical anchor for this release and reproduce exactly when `ECT_3D_Simulation_v2_1.py` is executed without modification.

| Metric | Result |
| :--- | :--- |
| Instability Number Γ(t) > Γ_crit | **100%** of runs |
| NIS Gate Compliance | **94.8%** (statistically undetectable by conventional single-epoch monitors) |
| Filter-reported CEP | **2.43 m** (effectively invariant; \|Δ\| < 0.01 m from nominal) |
| True Position Error (TPE) | **2.61 m → 4.37 m (+67%)** |
| Mission Kill Index (R_L = 15 m) | **MKI = 0.29** |
| Mission Kill Index (R_L = 3 m) | **MKI = 1.46** (confirmed SMK) |

The 0.2 percentage-point difference in NIS compliance between the nominal (95.0%) and perturbed (94.8%) cases is statistically negligible, confirming that the 100% Γ(t) exceedance is **entirely undetectable** by conventional innovation monitoring throughout the full trajectory.

<div align="center">
  <img src="Figures/Figure_3.png" width="850" alt="Monte Carlo Gamma Exceedance — N=500 runs">
  <br><em>Fig. 3. 100% any-time exceedance of Γ_crit = 6.5 across N = 500 paired-seed runs. Median Γ(t) (blue) with 5th–95th percentile band (shaded). Nominal filter (green dashed) remains consistent at Γ = 1. 3-D dual-sensor kinematic EKF, v2.1.</em>
</div>

<div align="center">
  <img src="Figures/Figure_5.png" width="850" alt="NIS Gate Compliance — Nominal vs Perturbed">
  <br><em>Fig. 5. NIS gate compliance: perturbed case (94.8%) is visually indistinguishable from nominal (95.0%), confirming that 100% Γ(t) exceedance is entirely undetectable by conventional single-epoch innovation monitoring. N = 500, 3-D dual-sensor EKF, v2.1.</em>
</div>

---

## ECT Framework

### Estimator Instability Number Γ(t)

The primary instability indicator is defined as the ratio of actual mean squared error (MSE) under perturbation to nominal MSE:

$$\Gamma(t) = \frac{E\left[\|x_{\text{true}} - \hat{x}_{\text{attacked}}\|^2\right]}{E\left[\|x_{\text{true}} - \hat{x}_{\text{nominal}}\|^2\right]}$$

Estimator collapse is confirmed when both conditions hold simultaneously:

$$\Gamma(t) \geq \Gamma_{\text{crit}} \quad \text{and} \quad \frac{d\Gamma}{dt} > 0$$

<div align="center">
  <img src="Figures/Figure_2.png" width="850" alt="Temporal Evolution of Estimator Instability Number">
  <br><em>Fig. 2. Temporal evolution of Γ(t) under structured perturbation. Panel C: Γ(t) crosses Γ_crit at T ≈ 11 min (demonstration-normalised units), marking the transition to the SMK regime. Panel D: confirmed SMK condition. The filter's internal covariance P_k remains bounded throughout — illustrating the covariance–truth divergence characteristic of Estimator Collapse.</em>
</div>

### Principal Perturbation Entry Points

<div align="center">
  <img src="Figures/Figure_1.png" width="800" alt="EKF Loop and Principal Perturbation Entry Points">
  <br><em>Fig. 1. Extended Kalman Filter loop and principal perturbation entry points exploited by the ECT framework. Attack Point A: sub-threshold measurement bias entering the chi-squared innovation gate. Attack Point B: measurement noise covariance R_k inflation, reducing Kalman gain and suppressing corrective feedback. Attack Point C: GNSS denial, removing primary independent cross-sensor validation.</em>
</div>

### Dimensionless Characterisation Metrics

ECT introduces four primary metrics to characterise the failure regime:

| Metric | Definition | Validation Status |
| :--- | :--- | :--- |
| Γ(t) | Ratio of actual MSE to nominal MSE — primary instability indicator | Validated (v2.1) |
| MKI | Ratio of realised TPE to operational failure threshold R_L | Validated (v2.1) |
| η_info | Uncertainty generation efficiency per unit delivered energy (Shannon entropy increase per joule) | Analytically estimated (v2.1); Phase II HWIL for closed-loop measurement |
| R_IE | Economic cost–benefit ratio of guidance degradation achieved relative to energy cost | Reserved for Phase II HWIL |

---

## The Sophistication Paradox

ECT formalises the **Sophistication Paradox** via the Vulnerability Index V_i: the counter-intuitive result that high-precision multi-sensor fusion architectures simultaneously maximise nominal accuracy and estimator vulnerability surface.

$$V_i = \frac{N_{\text{sensors}} \times f_{\text{update}}}{R_{\text{hardening}}}$$

where N_sensors is sensor modality count, f_update is filter update frequency (Hz), and R_hardening is a normalised electromagnetic shielding coefficient (1.0: standard; up to 3.0: fully hardened).

Each additional sensor modality added to improve nominal CEP introduces a corresponding injection surface accessible to ECT-class perturbations. The very capability that constitutes an architecture's primary accuracy advantage simultaneously constitutes its primary estimator vulnerability surface.

| System Class | N_s | f (Hz) | R_h | V_i (indicative) | Representative Example |
| :--- | :---: | :---: | :---: | :---: | :--- |
| Single-Sensor INS Platform | 1 | 1 | 1.0 | ≈ 1 | Short-range UAV |
| Dual-Modal Midcourse System | 3 | 10 | 1.0 | ≈ 30 | MALE UAV |
| High-Precision Multi-Sensor Platform | 4 | 20 | 1.2 | ≈ 67 | HALE / Orbital Asset |
| **High-Dynamics Multi-Sensor Platform** | **4** | **80** | **1.0** | **≈ 320** | **Re-entry Vehicle** |

V_i values are first-order theoretical estimates intended as empirical vulnerability proxies. System-specific Phase I Monte Carlo calibration is required for quantitative characterisation.

---

## Reproducibility Parameters (Table I — v2.1 Locked)

| Parameter | Value |
| :--- | :--- |
| EKF state dimension | 6 |
| Monte Carlo runs (N) | 500 (paired-seed) |
| Trajectory duration | 1,200 s |
| Sampling interval (Δt) | 1 s |
| Perturbation amplitude (A) | 2.5 m |
| Perturbation frequency (ω) | 0.05 rad/sample |
| Innovation gate (χ²₃) | 7.81 (95% significance) |
| Process noise Q | diag(0.01, 0.01, 0.01, 0.001, 0.001, 0.001) |
| GNSS measurement noise R | diag(25, 25, 25) m² |
| Γ_crit threshold | 6.5 |
| Master seed | 42 |
| Code version | v2.1.0 |

The master seed is fixed to 42 to ensure 100% numerical reproducibility of the "Confidently Wrong" signature across independent implementations.

---

## Repository Structure

Estimator-Collapse-Theory-ECT-Framework/
├── ECT_3D_Simulation_v2_1.py   # Core Monte Carlo simulation engine (v2.1.0 locked parameters)
├── Figures/
│   ├── Figure_1.png            # EKF loop and perturbation entry points
│   ├── Figure_2.png            # Temporal evolution of Γ(t)
│   ├── Figure_3.png            # Monte Carlo Γ(t) exceedance (N = 500)
│   ├── Figure_4.png            # "Confidently Wrong" CEP vs TPE signature
│   └── Figure_5.png            # NIS gate compliance (nominal vs perturbed)
├── Graphical_Abstract.png      # Visual overview of ECT framework
├── requirements.txt            # Python dependencies
└── LICENSE                     # Apache 2.0

---

## Quick Start

```bash
git clone https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git
cd Estimator-Collapse-Theory-ECT-Framework
pip install -r requirements.txt
python ECT_3D_Simulation_v2_1.py
```

**Expected outputs:** Figures 3–5 regenerated to `/ecf_v21_output/`, verification table printed to console. All metrics should match the locked values in the Reproducibility Parameters table above.

---

## Validation Roadmap

| Phase | Scope | Primary Deliverable |
| :--- | :--- | :--- |
| **Current (v2.1)** | 3-D kinematic EKF, dual-sensor, Monte Carlo | Gate-compliant divergence regime confirmed; "Confidently Wrong" signature demonstrated |
| **Phase I** | 6-DOF digital twin, full Monte Carlo characterisation | Γ_crit boundary as function of R_L; formal NIS/SPRT detectability bounds |
| **Phase II** | Hardware-in-the-loop (HWIL), anechoic chamber | Physical measurement of η_info; R_IE closed-loop characterisation |
| **Phase III** | Surrogate sub-orbital flight test | Real-time Γ(t) validation in vacuum environment |

---

## Citation

If you use this code or framework, please cite the companion paper and this repository:

```bibtex
@article{barua2026sophistication,
  title   = {The Sophistication Paradox: A Systems-Theoretic Framework for Estimator
             Collapse in Precision-Guided Autonomous Navigation Architectures},
  author  = {Barua, Nick and Douglas, Robert J.},
  journal = {CEAS Aeronautical Journal},
  year    = {2026},
  note    = {Will be submitted}
}

@software{barua2026ect,
  author    = {Barua, Nick and Douglas, Robert J.},
  title     = {The Sophistication Paradox: Estimator Collapse Theory (ECT) Framework v2.1.0},
  year      = {2026},
  publisher = {Zenodo},
  doi       = {10.5281/zenodo.20132174},
  url       = {https://doi.org/10.5281/zenodo.20132174}
}
```

## Licence

This project is licensed under the [Apache 2.0 Licence](LICENSE).

© 2026 Nick Barua and Robert J. Douglas, AN Holdings CO., Nishinomiya, Japan.
