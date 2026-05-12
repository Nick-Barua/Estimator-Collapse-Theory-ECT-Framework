# Estimator Collapse Theory (ECT) — Reference Implementation & v2.1 Numerical Validation

**The Sophistication Paradox: A Systems-Theoretic Framework for Estimator Collapse in Precision-Guided Autonomous Navigation Architectures**

**Nick Barua¹  ·  Robert J. Douglas¹³**

¹ AN Holdings CO., Nishinomiya, Japan  
³ Kobe Design Lab, Kobe, Japan

Correspondence: s.nick.barua@gmail.com

[![DOI](https://img.shields.io/badge/DOI-10.5281%2Fzenodo.20132174-blue)](https://doi.org/10.5281/zenodo.20132174)
[![Version](https://img.shields.io/badge/version-v2.1-blue)](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework)
[![License](https://img.shields.io/badge/license-Apache--2.0-green)](LICENSE)

---

[![Graphical Abstract](Graphical_Abstract.png)](Graphical_Abstract.png)

---

## Overview

This repository is the reference implementation and archival numerical validation suite for **Estimator Collapse Theory (ECT)**—a systems-theoretic analytical framework establishing that guidance-critical state-estimation destabilisation constitutes a formally characterisable mission-level failure pathway for precision autonomous navigation systems.

ECT identifies a class of **sub-threshold, gate-compliant perturbations**—bounded measurement disturbances calibrated to remain within chi-squared innovation gating thresholds—that systematically corrupt the state estimate of an Extended Kalman Filter (EKF) whilst leaving the filter's self-reported covariance structurally unaffected. The system enters a condition of **estimator inconsistency**: it reports high confidence in a position estimate that has, in fact, diverged beyond operational tolerance. This condition is termed **Estimator Collapse**; the resulting transition to mission-level failure is termed a **Stochastic Mission Kill (SMK)**.

The framework formalises the **Sophistication Paradox**: the counter-intuitive result that high-precision multi-sensor fusion architectures, by expanding their sensor modality count and update rate, simultaneously maximise nominal accuracy and estimator vulnerability surface.

---

## The *Confidently Wrong* Result — v2.1 Archival Finding

The central result of the v2.1 validation run is a structurally inconsistent estimation regime termed ***Confidently Wrong***:

| Quantity | Nominal | Perturbed | Δ |
|---|---|---|---|
| **Filter-reported CEP** (from covariance, Eq. 9) | 2.43 m | 2.43 m | **< 0.01 m** |
| **True Position Error (TPE)** | 2.61 m | 4.37 m | **+67%** |
| **Γt exceedance** (Γt > Γcrit = 6.5) | 0% | **100%** | — |
| **NIS gate compliance** | 95.0% | **94.8%** | −0.2 pp |

The filter's self-reported uncertainty remained effectively invariant—a mean delta below 0.01 m across all 500 runs—whilst true position error grew by 67% and the Estimator Instability Number exceeded the collapse threshold in every run. The filter's internal health monitor registered no anomaly throughout the full 1,200-second trajectory. The 0.2 percentage-point change in NIS compliance is statistically negligible, confirming that the divergence is entirely undetectable by conventional single-epoch innovation monitoring.

> **Note on prior releases:** Results reported in earlier repository versions (e.g., v1.4.1) reflect a different parameterisation and must not be compared directly to the v2.1 archival figures above. The v2.1 run constitutes the canonical numerical validation record corresponding to the submitted manuscript.

---

## Visual Demonstration

The video below illustrates the real-time transition from nominal state estimation to Estimator Collapse under structured perturbation.

https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework/blob/main/ECT_SMK_Conceptual_Overview.mp4

**Panel 1 — Instability Number:** Divergence between actual estimation error and filter-reported covariance, illustrating the loss of estimator consistency.  
**Panel 2 — Telemetry:** Real-time tracking of the Mission Kill Index (MKI) as Γt crosses Γcrit = 6.5.  
**Panel 3 — CEP:** Expansion of true position error relative to the filter's structurally blind covariance-derived CEP.  
**Panel 4 — Information Theory:** Growth of Shannon entropy h(X) of the impact-point distribution toward hmax.

---

## Theoretical Framework

### Extended Kalman Filter Loop and Perturbation Entry Points

The Kalman gain at epoch k is

$$K_k = P_{k|k-1} H_k^\top \left( H_k P_{k|k-1} H_k^\top + R_k \right)^{-1}$$

A measurement $z_k$ is accepted through the chi-squared innovation gate if and only if

$$y_k^\top S_k^{-1} y_k \leq \chi^2_{n,\alpha}$$

where $S_k = H_k P_{k|k-1} H_k^\top + R_k$. Any perturbation $\delta z_k$ satisfying this gate is statistically indistinguishable from legitimate sensor noise at the single-epoch level. ECT exploits the gap between **single-epoch indistinguishability** and **multi-epoch divergence**.

Three principal perturbation entry points are illustrated in Figure 1:

- **Attack Point A:** Sub-threshold measurement bias entering the chi-squared innovation gate.
- **Attack Point B:** Measurement noise covariance $R_k$ inflation, suppressing corrective feedback in the Riccati equation.
- **Attack Point C:** GNSS denial, removing the primary independent cross-sensor validation reference.

[![EKF Loop and Attack Points](Figures/Figure_1.png)](Figures/Figure_1.png)  
*Figure 1. Extended Kalman Filter loop and principal perturbation entry points exploited by the ECT framework.*

### Covariance Growth Under Sub-Threshold Perturbation

Under nominal operation, the negative corrective term in the Kalman–Bucy Riccati equation

$$\dot{P} = FP + PF^\top + Q - PH^\top R^{-1} HP$$

stabilises covariance growth. When a perturbation mechanism inflates $R_k$, the term $R^{-1}$ approaches zero, suppressing corrective feedback and allowing process noise $Q$ to drive persistent upward drift in $\text{tr}(P_{pp,k})$. Individual injected measurements remain, by construction, inside the innovation gate; however, multi-epoch residual analysis—via NIS, NEES, or SPRT—may, in principle, accumulate sufficient evidence to flag the anomaly. Whether a perturbation sequence exists that keeps the pooled NIS statistic below the multi-epoch threshold whilst sustaining covariance growth constitutes the central falsifiable conjecture of ECT, whose formal resolution is the primary objective of the Phase I validation programme.

---

## Dimensionless Characterisation Metrics

ECT introduces four metrics to quantify the estimator-collapse regime:

**Estimator Instability Number $\Gamma_t$**

$$\Gamma_t = \frac{\mathbb{E}\left[\|x_{\text{true}} - x_{\text{attacked}}\|^2\right]}{\mathbb{E}\left[\|x_{\text{true}} - x_{\text{nominal}}\|^2\right]}$$

Estimator collapse is confirmed when $\Gamma_t \geq \Gamma_{\text{crit}}$ and $\dot{\Gamma}_t > 0$ simultaneously.

**Mission Kill Index (MKI)**

$$\text{MKI}_t = \frac{\text{CEP}_t}{R_L}$$

Mission failure is confirmed when $\text{MKI}_t \geq 1$.

**Information-to-Energy Yield $\eta_{\text{info}}$**

$$\eta_{\text{info}} = \frac{\Delta h(X)}{E_{\text{attack}}}$$

where $\Delta h(X)$ is the increase in differential Shannon entropy of the impact-point distribution and $E_{\text{attack}}$ is the total delivered energy (J).

**Economic Reversal Ratio $R_{IE}$** — defined analytically; reserved for Phase II HWIL characterisation.

---

## The Sophistication Paradox and Vulnerability Index

The Vulnerability Index $V_i$ provides a first-order characterisation of a navigation system's susceptibility to ECT-class perturbation:

$$V_i = \frac{N_{\text{sensors}} \times f_{\text{update}}}{R_{\text{hardening}}}$$

where $N_{\text{sensors}}$ is sensor modality count, $f_{\text{update}}$ is filter update frequency (Hz), and $R_{\text{hardening}}$ is a normalised electromagnetic shielding coefficient (1.0 = standard; upper bound ≈ 3.0 for radiation-hardened CMOS).

| System Class | Ns | fupd (Hz) | Rh | Vi (indicative) | Example |
|---|---|---|---|---|---|
| Single-Sensor INS Platform | 1 | 1 | 1.0 | ≈ 1 | Short-range UAV |
| Dual-Modal Midcourse System | 3 | 10 | 1.0 | ≈ 30 | MALE UAV |
| High-Precision Multi-Sensor | 4 | 20 | 1.2 | ≈ 67 | HALE / Orbital |
| High-Dynamics Multi-Sensor | 4 | 80 | 1.0 | ≈ 320 | Re-entry Vehicle |

The Sophistication Paradox follows directly from the $V_i$ taxonomy: each additional sensor modality added to improve nominal CEP introduces a corresponding injection surface accessible to ECT perturbation. The very capability constituting an architecture's primary accuracy advantage simultaneously constitutes its primary estimator vulnerability surface.

---

## 3-D Monte Carlo Validation — v2.1 Archival Run

### Locked Hyperparameter Set

| Parameter | Value |
|---|---|
| EKF state dimension | 6 |
| Monte Carlo runs (N) | 500 |
| Sampling interval (Δt) | 1 s |
| Simulation duration | 1,200 s |
| Perturbation amplitude (A_PERT) | 2.5 m |
| Perturbation frequency (ω) | 0.05 rad/sample |
| Chi-squared gate (χ²₃) | 7.81 |
| Process noise Q | diag(0.01, 0.01, 0.01, 0.001, 0.001, 0.001) |
| GNSS measurement noise R | diag(25, 25, 25) m² |
| Γcrit threshold | 6.5 |
| Code version | v2.1 |
| **Master seed** | **42** |

The master seed is fixed at 42 to guarantee 100% numerical reproducibility of the *Confidently Wrong* signature across independent implementations. Executing the archived script without modification reproduces all reported figures and metric values exactly.

### Perturbation Structure

A bounded sinusoidal structured perturbation

$$\delta z_k = \left[ A\sin(\omega k),\ A\cos(\omega k),\ A\sin\!\left(\omega k + \tfrac{\pi}{3}\right) \right]^\top$$

with $A = 2.5$ m and $\omega = 0.05$ rad/sample is injected into the GNSS measurement channel, calibrated to remain within the 95% chi-squared innovation gate ($\chi^2_3 = 7.81$).

### Results

[![Γt Evolution](Figures/Figure_3.png)](Figures/Figure_3.png)  
*Figure 3. Temporal evolution of Γt under structured perturbation. Median Γt remains bounded; the 5th–95th percentile band demonstrates frequent exceedances of Γcrit = 6.5, producing 100% any-time exceedance across all 500 runs. Nominal filter (green dashed) remains consistent at Γ = 1.*

[![CEP and TPE](Figures/Figure_4.png)](Figures/Figure_4.png)  
*Figure 4. Filter-reported CEP and True Position Error (TPE) under gate-compliant perturbation. (a) Nominal: filter-reported CEP tracks TPE closely. (b) Perturbed: filter-reported CEP remains invariant at 2.43 m whilst TPE grows to 4.37 m — the Confidently Wrong signature. (c) ΔCEP oscillates at the perturbation frequency with amplitude ~10⁻⁷ m. (d) Terminal TPE distribution across N = 500 runs: nominal μ = 2.61 m, perturbed μ = 4.37 m (+67%).*

[![NIS Compliance](Figures/Figure_5.png)](Figures/Figure_5.png)  
*Figure 5. NIS gate compliance under structured perturbation. Nominal: 95.0%. Perturbed: 94.8%. The 0.2 percentage-point difference confirms the estimator inconsistency demonstrated in Figure 3 is entirely undetectable by conventional single-epoch innovation monitoring throughout the full 1,200-second trajectory.*

### Interpretation

For $R_L = 15$ m: MKI = 4.37 / 15 = 0.29 — below the kill threshold for this conservative profile. This result must be interpreted carefully: MKI < 1 does not indicate a healthy estimator. The diagnostic signal is 100% Γt exceedance — the filter has lost its ability to bound its own error, constituting a structurally inconsistent estimation regime. Under terminal-phase precision-guidance tolerances where $R_L \leq 3$ m, MKI = 4.37 / 3 = 1.46 and SMK is confirmed.

---

## Repository Structure
├── ECT_3D_Simulation_v2.1.py         # Archival Monte Carlo simulation (locked, seed 42)
├── ECT_SMK_Conceptual_Overview.mp4   # Conceptual SMK failure transition visualisation
├── Graphical_Abstract.jpg.webp       # Visual framework summary
├── Figures/
│   ├── Figure_1.png                  # EKF loop and perturbation entry points
│   ├── Figure_2.png                  # Four-stage estimator collapse progression
│   ├── Figure_3.png                  # Γt temporal evolution (N=500)
│   ├── Figure_4.png                  # Filter-reported CEP vs TPE (Confidently Wrong)
│   └── Figure_5.png                  # NIS gate compliance
├── Citation                          # BibTeX and plain-text citation records
├── requirements.txt                  # Python dependencies
└── LICENSE                           # Apache 2.0

---

## Countermeasures and Resilient Architecture Design

ECT is published to motivate the design of estimator-resilient navigation architectures. The framework identifies the following primary defence directions:

**Hardware countermeasures.** Electromagnetic hardening (Faraday shielding, radiation-hardened CMOS) elevates Rhardening, reducing Vi and raising the energy cost of perturbation delivery.

**Filter-level defences.** Multi-epoch integrity monitors (NIS, NEES, SPRT) and Interacting Multiple Model (IMM) filtering with adaptive Q/R estimation are necessary first-line defences. However, the two-regime perturbation structure (high-trust seeding followed by gate-compliant divergence) must be calibrated against the full multi-epoch residual history, not merely a single-epoch gate. For UKF and Cubature Kalman Filter architectures, the injected bias must satisfy the gate constraint simultaneously across the entire sigma-point cloud, substantially constraining the admissible null space.

**Multi-layered consistency validation.** Resilient architectures may additionally require cross-sensor residual correlation analysis, adaptive gating, conservative covariance management, and H∞-based robust filtering approaches.

---

## Limitations

The framework is not intended to imply universal vulnerability, but to define the conditions under which sufficiently estimator-dependent architectures become susceptible to non-kinetic mission failure. Principal limitations are:

- The covariance model assumes a linearised 6-state constant-velocity EKF; 6-DOF aerodynamic validation is deferred to Phase I. This limitation is conservative: nonlinear coupling is expected to accelerate divergence.
- The null-space reachability result (Section 2.6 of the manuscript) is a conjecture pending formal analytical proof.
- Γcrit is treated as a system-dependent parameter; its calibration for specific GNC architectures is the primary Phase I objective.
- The scope is presently constrained to exoatmospheric and high-altitude trajectories.
- R_IE is an analytically defined metric reserved for Phase II HWIL characterisation.

---

## Validation Roadmap

**Phase I — 6-DOF Digital Twin and Monte Carlo:** Monte Carlo characterisation of Γcrit across system profiles; formal test of the null-space reachability conjecture; full 6-DOF aerodynamic integration.

**Phase II — HWIL Electronic Warfare Testing:** Physical navigation computer on multi-axis motion simulator; RF spoofing in an anechoic chamber; calibrated false stellar fields for star-tracker optical injection. Primary metric: physical measurement of η_info.

**Phase III — Surrogate Flight Testing:** Sub-orbital sounding rocket with targeted EKF payload; ground-based EW platform illumination during exoatmospheric coast; real-time telemetric validation of Γt divergence.

---

## Reproducibility

The v2.1 simulation engine, perturbation synthesis scripts, and metric implementations are archived on Zenodo at:

> **DOI: [10.5281/zenodo.20132174](https://doi.org/10.5281/zenodo.20132174)**

Executing the archived script without modification (master seed 42, N = 500) reproduces all reported figures and metric values exactly. The Zenodo archive corresponds specifically to the v2.1 archival verification run and constitutes the canonical numerical record for the submitted manuscript.

Concept DOI (all versions): [https://doi.org/10.5281/zenodo.19469720](https://doi.org/10.5281/zenodo.19469720)

---

## Citation
If you use this framework, simulation code, or dimensionless metrics in your research, please cite the manuscript and the Zenodo archive:

**Manuscript:**
@article{barua2026sophistication,
author    = {Barua, Nick and Douglas, Robert J.},
title     = {The Sophistication Paradox: A Systems-Theoretic Framework for
Estimator Collapse in Precision-Guided Autonomous Navigation Architectures},
journal   = {[Springer journal — in press]},
year      = {2026},
note      = {DOI pending}
}

**Software (v2.1 archival):**
@software{barua2026ect_v21,
author    = {Barua, Nick and Douglas, Robert J.},
title     = {Estimator Collapse Theory (ECT): Reference Implementation and v2.1
Numerical Validation},
year      = {2026},
doi       = {10.5281/zenodo.20132174},
url       = {https://doi.org/10.5281/zenodo.20132174},
note      = {Version v2.1, master seed 42, N=500}
}

---

## Dual-Use Statement

This paper presents a theoretical analytical framework for estimator destabilisation in precision navigation systems. It is published in the open scientific literature in accordance with the principle that transparent theoretical formalisation enables the research community to develop appropriate countermeasures, resilient filter architectures, and hardening strategies. No classified information, export-controlled data, or proprietary system specifications have been used. All referenced system parameters are drawn exclusively from open-source, publicly available academic and technical literature.

---

## Funding and Conflicts of Interest

This research received no specific grant from any funding agency in the public, commercial, or not-for-profit sectors. The authors declare no conflicts of interest and received no sponsorship from any defence contractor, government procurement agency, or armaments manufacturer.

---

## Authors

**N. Barua:** Conceptualisation, Methodology, Software, Formal Analysis, Investigation, Writing – Original Draft, Visualisation.  
**R.J. Douglas:** Conceptualisation, Resources, Writing – Review & Editing, Project Administration.

---

*ECT reframes guidance robustness as an estimation-consistency problem, establishing a new analytical direction for resilient autonomous navigation system design.*
