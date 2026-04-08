# Estimator Collapse Theory (ECT) Framework

**Version:** v1.2.0 – Submission-Ready Release (April 2026)

[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.19450239.svg)](https://doi.org/10.5281/zenodo.19450239)

This repository provides the reference implementation and numerical validation scripts for the analytical framework formalised in:

> **Barua, N. (2026). Estimator Collapse Theory: Stochastic Mission Kill for Ballistic Interception.**

## 📌 Abstract
[cite_start]Estimator Collapse Theory (ECT) defines a new analytical regime in which ballistic mission kill emerges through state-estimator destabilisation rather than physical destruction[cite: 436, 440]. [cite_start]Unlike classical divergence analyses, this framework focuses on sub-threshold, gate-compliant perturbations that induce a **"Confidently Wrong"** failure regime[cite: 441, 486]. [cite_start]In this state, actual position error grows exponentially while the onboard filter reports deceptively stable internal covariance[cite: 522, 560]. [cite_start]This release assumes a baseline LEO architecture with 100 MW peak pulse power[cite: 584, 722].

## 🏷️ Keywords
Estimator Collapse Theory; Stochastic Mission Kill; Analytical Framework; State Estimation; Sensor Fusion; Guidance, Navigation, and Control; Systems Resilience; Covariance Divergence; Circular Error Probable; Economic Reversal Ratio; [cite_start]Mission Kill Index [cite: 448-449].

## 🧪 Minimal Constructive Demonstration
[cite_start]The included `ekf_scalar_demo.py` reproduces the numerical results of **Section 2.5** of the manuscript [cite: 545-561]. [cite_start]It demonstrates that a calibrated innovation bias can drive the **Estimator Instability Number** $\Gamma(t)$ above the critical collapse threshold $\Gamma_{crit} \approx 6.5$ within a standard 15-minute midcourse engagement window [cite: 558-560].

## 📊 Key Dimensionless Metrics
[cite_start]The framework introduces four primary metrics to quantify the estimator-collapse regime[cite: 442, 466]:

* [cite_start]**$\Gamma(t)$**: The **Estimator Instability Number**, defined as the ratio of actual Mean Squared Error (MSE) of the position state estimate under attack to the nominal MSE [cite: 514-515].
* [cite_start]**MKI**: The **Mission Kill Index**, defined as the ratio of the expanded Circular Error Probable (CEP) to the lethal radius $R_L$ [cite: 530-531].
* [cite_start]**$\eta_{info}$**: The **Information-to-Energy Yield**, quantifying the uncertainty-generation efficiency of a perturbation mechanism using differential Shannon entropy $\Delta h(X)$ [cite: 534-536].
* **$\mathcal{R}_{IE}$**: The **Economic Reversal Ratio**, comparing the amortised cost of an SMK engagement to the unit cost of the threat [cite: 699-700].

## 🖼️ Validation Figures
High-resolution 600 DPI outputs from the analytical framework:

### Figure 1: The Drift-to-Fail Paradigm Shift
![Figure 1](Figure1_Paradigm_Shift.png)
[cite_start]*A conceptual illustration comparing kinetic interception with Stochastic Mission Kill (SMK) [cite: 476-479].*

### Figure 2: EKF Attack Surface
![Figure 2](Figure2_EKF_Attack_Surface.png)
[cite_start]*Detailed signal flow showing where sub-threshold bias and covariance inflation ($R_k$) are injected [cite: 504-507].*

### Figure 3: Temporal Evolution of $\Gamma(t)$
![Figure 3](Figure3_Temporal_Evolution.png)
*Evolution of the instability number demonstrating the "Confidently Wrong" regime. Threshold crossing ($\Gamma_{crit} \approx 6.5$) is achieved at $T \approx 11$ minutes [cite: 527-529].*

### Figure 5: CEP Expansion Pathways
![Figure 5](Figure5_CEP_Expansion.png)
[cite_start]*Comparative expansion pathways across threat classes, illustrating the **Sophistication Paradox** [cite: 640-641].*

### Figure 6: Interception Economics
![Figure 6](Figure6_Interception_Economics.png)
*Cost-per-engagement comparison. [cite_start]The SMK constellation is hypothesised to achieve economic reversal ($\mathcal{R}_{IE} < 1$) with an amortised engagement cost of **~$750K ($0.75M)** [cite: 706-714, 716].*

## 🎥 SMK Video
[▶ Watch the SMK validation video](./stochastic_mission_kill.mp4)

## 🔗 Repository and Archival Record
This GitHub repository contains the active development version of the ECT framework. The corresponding archived and citable release is available on Zenodo:
**DOI:** [10.5281/zenodo.19450239](https://doi.org/10.5281/zenodo.19450239)

## 📖 Citation
If you use this work, please cite:
> Barua, N. (2026). *Estimator Collapse Theory: Stochastic Mission Kill for Ballistic Interception*. Zenodo. https://doi.org/10.5281/zenodo.19450239

**Associated References:**
* [31] Lewis, G.N.; Postol, T.A. Video Evidence on the Effectiveness of the Patriot Missile Defense System. *Sci. Glob. [cite_start]Secur.* **1993**, *4*, 1–63 [cite: 819-820].
* [35] Pasqualetti, F.; Dörfler, F.; Bullo, F. Control-theoretic methods for cyber-physical security. *IEEE Trans. Control Netw. Syst.* **2014**, *1*, 50–71 [cite: 826-827].

## 🚀 Quick Start
```bash
# Clone the repository
git clone [https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git](https://github.com/Nick-Barua/Estimator-Collapse-Theory-ECT-Framework.git)

# Enter the directory
cd Estimator-Collapse-Theory-ECT-Framework

# Install dependencies
pip install -r requirements.txt

# Run the EKF scalar demonstration (Matches Section 2.5 results)
python ekf_scalar_demo.py
