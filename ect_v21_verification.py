#!/usr/bin/env python3
"""
=============================================================================
 The Sophistication Paradox — v2.1 Archival Verification Simulation
 Estimator Collapse Theory (ECT) | Pre-Archive Validation Run
=============================================================================
 Authors  : Nick Barua, Robert J. Douglas
 Affil.   : AN Holdings CO., Nishinomiya, Japan
 Archive  : Zenodo DOI 10.5281/zenodo.20037820
 Code ver : v2.1  (LOCKED — do not modify for this submission cycle)

 Locked parameter set (manuscript Section II-E, Table III):
   A_PERT   = 2.5 m          ω = 0.05 rad/sample
   Q        = diag(0.01×3, 0.001×3)
   R_GNSS   = diag(25, 25, 25) m²    σ_range = 25 m
   N        = 500             T = 1200 s      Δt = 1 s
   Γ_crit   = 6.5             R_L = 15 m      seed = 42

 Target metrics (manuscript Section II-E.1):
   Filter-reported CEP  ≈ 2.43 m   (invariant under perturbation)
   Nominal TPE          ≈ 2.60 m
   Perturbed TPE        ≈ 3.46 m   (+33%)
   Γ(t) exceedance      = 100% of runs
   NIS gate compliance  ≈ 95%
   MKI (R_L = 15 m)    = 0.53

 Workflow:
   1. Paired-seed Monte Carlo (N = 500 nominal + 500 perturbed)
   2. Compute Γ(t), CEP, TPE, NIS, MKI across all runs
   3. Export publication-quality figures (Figs 3, 4, 5)
   4. Print verification table against locked manuscript values
   5. Optional: sensitivity sweep (A = 1.5, 2.5, 3.5 m)
=============================================================================
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from pathlib import Path
import time
import sys

# ── Output directory ────────────────────────────────────────────────────────
OUT = Path("ecf_v21_output")
OUT.mkdir(exist_ok=True)

# ════════════════════════════════════════════════════════════════════════════
#  LOCKED PARAMETERS  v2.1  — DO NOT MODIFY
# ════════════════════════════════════════════════════════════════════════════
MASTER_SEED   = 42
N_RUNS        = 500
T_SIM         = 1200            # [s]
DT            = 1.0             # [s]
N_STEPS       = int(T_SIM / DT) # 1200

N_STATES      = 6               # [x, y, z, vx, vy, vz]

Q_MAT  = np.diag([0.01, 0.01, 0.01, 0.001, 0.001, 0.001])
R_GNSS = np.diag([25.0, 25.0, 25.0])    # m²
SIGMA_RANGE   = 25.0            # m
R_RANGE       = SIGMA_RANGE**2  # m²  (scalar)

A_PERT        = 2.5             # m
OMEGA_PERT    = 0.05            # rad/sample

CHI2_GATE     = 7.81            # χ²(3, 0.95)
GAMMA_CRIT    = 6.5
R_L           = 15.0            # mission-kill radius [m]

# Fixed beacon for range sensor (off trajectory, provides useful geometry)
BEACON        = np.array([0.0, 5000.0, 0.0])

# Nominal initial state: position (m), velocity (m/s)
X0    = np.array([0.0, 0.0, 100.0, 10.0, 0.0, 0.0])
P0    = np.diag([100.0, 100.0, 100.0, 10.0, 10.0, 10.0])

# ── Derived matrices ─────────────────────────────────────────────────────────
F_MAT = np.eye(N_STATES)
F_MAT[0, 3] = F_MAT[1, 4] = F_MAT[2, 5] = DT

H_GNSS = np.zeros((3, N_STATES))
H_GNSS[0, 0] = H_GNSS[1, 1] = H_GNSS[2, 2] = 1.0

# Pre-compute sinusoidal perturbation profile (time-invariant across runs)
_k = np.arange(N_STEPS)
DELTA_Z_PROFILE = np.column_stack([
    A_PERT * np.sin(OMEGA_PERT * _k),
    A_PERT * np.cos(OMEGA_PERT * _k),
    A_PERT * np.sin(OMEGA_PERT * _k + np.pi / 3),
])  # shape (N_STEPS, 3)

# ════════════════════════════════════════════════════════════════════════════
#  EKF ROUTINES
# ════════════════════════════════════════════════════════════════════════════

def cep_from_P(P):
    """Filter-reported CEP from covariance (equation 9)."""
    return 1.1774 * np.sqrt(0.5 * (P[0, 0] + P[1, 1]))


def range_h(pos, beacon):
    """Nonlinear range measurement function."""
    d = pos - beacon
    return np.sqrt(d @ d)


def range_jacobian(pos, beacon):
    """1×6 Jacobian of range measurement at current estimate."""
    d   = pos - beacon
    r   = max(np.sqrt(d @ d), 1e-9)
    H   = np.zeros((1, N_STATES))
    H[0, :3] = d / r
    return H


def ekf_step(x, P, z_gnss, z_range, F, Q, H_gnss, R_gnss, beacon, R_range):
    """
    One full EKF cycle: predict → GNSS update → range update.
    Returns (x_upd, P_upd, nis_gnss).
    NIS is computed on the GNSS channel (3 DOF) before the range update.
    """
    # ── Predict ────────────────────────────────────────────────────────────
    x_p = F @ x
    P_p = F @ P @ F.T + Q

    # ── GNSS update (linear) ───────────────────────────────────────────────
    innov  = z_gnss - H_gnss @ x_p
    S      = H_gnss @ P_p @ H_gnss.T + R_gnss
    S_inv  = np.linalg.inv(S)
    K      = P_p @ H_gnss.T @ S_inv
    x_p    = x_p + K @ innov
    P_p    = (np.eye(N_STATES) - K @ H_gnss) @ P_p

    # NIS on GNSS innovation (eq. 11 gate check)
    nis = float(innov @ S_inv @ innov)

    # ── Range update (nonlinear EKF linearisation) ─────────────────────────
    h_hat = range_h(x_p[:3], beacon)
    H_r   = range_jacobian(x_p[:3], beacon)        # (1, 6)
    y_r   = z_range - h_hat
    S_r   = float((H_r @ P_p @ H_r.T).item()) + R_range
    K_r   = (P_p @ H_r.T) / S_r                    # (6, 1)
    x_p   = x_p + K_r.flatten() * y_r
    P_p   = (np.eye(N_STATES) - np.outer(K_r.flatten(), H_r.flatten())) @ P_p

    return x_p, P_p, nis


# ════════════════════════════════════════════════════════════════════════════
#  PAIRED-SEED SINGLE-RUN FUNCTION
# ════════════════════════════════════════════════════════════════════════════

def run_paired(run_id):
    """
    Run one paired (nominal + perturbed) simulation.
    Both cases share identical process noise and sensor noise draws;
    the only difference is the addition of DELTA_Z_PROFILE to z_gnss.

    Returns dicts with keys: mse, tpe, cep, nis — each shape (N_STEPS,).
    """
    rng = np.random.default_rng(MASTER_SEED + run_id)

    # Pre-draw all noise for this run (paired, so both cases use the same)
    proc_noise  = rng.multivariate_normal(np.zeros(N_STATES), Q_MAT,  N_STEPS)
    gnss_noise  = rng.multivariate_normal(np.zeros(3),        R_GNSS, N_STEPS)
    range_noise = rng.normal(0.0, SIGMA_RANGE, N_STEPS)

    # Initial true state: common small offset
    x0_true = X0 + rng.normal(0, 0.1, N_STATES)

    nom  = dict(mse=np.empty(N_STEPS), tpe=np.empty(N_STEPS),
                cep=np.empty(N_STEPS), nis=np.empty(N_STEPS))
    pert = dict(mse=np.empty(N_STEPS), tpe=np.empty(N_STEPS),
                cep=np.empty(N_STEPS), nis=np.empty(N_STEPS))

    for label, result, use_pert in [("nom", nom, False), ("pert", pert, True)]:
        x_true = x0_true.copy()
        x_est  = X0.copy()
        P_est  = P0.copy()

        for k in range(N_STEPS):
            # Propagate ground truth
            x_true = F_MAT @ x_true + proc_noise[k]

            # Build measurements
            dz     = DELTA_Z_PROFILE[k] if use_pert else np.zeros(3)
            z_gnss = H_GNSS @ x_true + gnss_noise[k] + dz
            z_rng  = range_h(x_true[:3], BEACON) + range_noise[k]

            # EKF cycle
            x_est, P_est, nis_k = ekf_step(
                x_est, P_est, z_gnss, z_rng,
                F_MAT, Q_MAT, H_GNSS, R_GNSS, BEACON, R_RANGE
            )

            err           = x_true[:3] - x_est[:3]
            mse_k         = float(err @ err)
            result["mse"][k] = mse_k
            result["tpe"][k] = np.sqrt(mse_k)
            result["cep"][k] = cep_from_P(P_est)
            result["nis"][k] = nis_k

    return nom, pert


# ════════════════════════════════════════════════════════════════════════════
#  MONTE CARLO CAMPAIGN
# ════════════════════════════════════════════════════════════════════════════

def run_monte_carlo(n_runs=N_RUNS, verbose=True):
    """Run the full N-run paired Monte Carlo and collect aggregate arrays."""
    if verbose:
        print("\n" + "=" * 68)
        print("  ECT v2.1 — Archival Verification Monte Carlo")
        print(f"  N = {n_runs}  |  T = {T_SIM} s  |  A = {A_PERT} m  "
              f"|  ω = {OMEGA_PERT} rad/s")
        print(f"  Master seed: {MASTER_SEED}")
        print("=" * 68)

    mse_nom  = np.empty((n_runs, N_STEPS))
    mse_pert = np.empty((n_runs, N_STEPS))
    tpe_nom  = np.empty((n_runs, N_STEPS))
    tpe_pert = np.empty((n_runs, N_STEPS))
    cep_nom  = np.empty((n_runs, N_STEPS))
    cep_pert = np.empty((n_runs, N_STEPS))
    nis_nom  = np.empty((n_runs, N_STEPS))
    nis_pert = np.empty((n_runs, N_STEPS))

    t0 = time.time()
    for i in range(n_runs):
        nom, pert = run_paired(i)
        mse_nom[i]  = nom["mse"];   mse_pert[i]  = pert["mse"]
        tpe_nom[i]  = nom["tpe"];   tpe_pert[i]  = pert["tpe"]
        cep_nom[i]  = nom["cep"];   cep_pert[i]  = pert["cep"]
        nis_nom[i]  = nom["nis"];   nis_pert[i]  = pert["nis"]
        if verbose and (i + 1) % 100 == 0:
            print(f"  [{i+1:4d}/{n_runs}]  elapsed: {time.time()-t0:.1f}s")

    if verbose:
        print(f"  Done — {time.time()-t0:.1f}s total\n")

    return (mse_nom, mse_pert, tpe_nom, tpe_pert,
            cep_nom, cep_pert, nis_nom, nis_pert)


# ════════════════════════════════════════════════════════════════════════════
#  METRIC COMPUTATION
# ════════════════════════════════════════════════════════════════════════════

def compute_metrics(mse_nom, mse_pert, tpe_nom, tpe_pert,
                    cep_nom, cep_pert, nis_nom, nis_pert):
    """Derive all ECT characterisation metrics from Monte Carlo arrays."""
    # Gamma(t): ratio of mean MSE across runs at each time step  (eq. 5/6)
    mean_mse_nom  = mse_nom.mean(axis=0)
    mean_mse_pert = mse_pert.mean(axis=0)
    # Avoid divide-by-zero in transient
    denom = np.where(mean_mse_nom < 1e-9, 1e-9, mean_mse_nom)
    gamma_t = mean_mse_pert / denom

    # Per-run terminal Gamma (last 100 steps average)
    gamma_terminal_per_run = (mse_pert[:, -100:].mean(axis=1) /
                               np.maximum(mse_nom[:, -100:].mean(axis=1), 1e-9))

    # Gamma exceedance: fraction of runs where Gamma > Gamma_crit at any point
    gamma_per_run_t = (mse_pert / np.maximum(mse_nom, 1e-9))  # (N, T)
    exceedance_mask = (gamma_per_run_t > GAMMA_CRIT).any(axis=1)
    gamma_exceedance_pct = exceedance_mask.mean() * 100.0

    # Median + percentile bands for Gamma
    gamma_med   = np.median(gamma_per_run_t, axis=0)
    gamma_p05   = np.percentile(gamma_per_run_t, 5,  axis=0)
    gamma_p95   = np.percentile(gamma_per_run_t, 95, axis=0)

    # CEP: time-averaged over steady-state window (last 600 steps)
    ss = slice(-600, None)
    mean_cep_nom_ss  = cep_nom[:,  ss].mean()
    mean_cep_pert_ss = cep_pert[:, ss].mean()
    cep_delta        = mean_cep_pert_ss - mean_cep_nom_ss

    # TPE: mean across runs, time-averaged over steady state
    mean_tpe_nom_ss  = tpe_nom[:,  ss].mean()
    mean_tpe_pert_ss = tpe_pert[:, ss].mean()
    tpe_growth_pct   = (mean_tpe_pert_ss / mean_tpe_nom_ss - 1) * 100.0

    # NIS gate compliance: fraction of (run, step) pairs with NIS ≤ χ²_gate
    nis_nom_compliance  = (nis_nom  <= CHI2_GATE).mean() * 100.0
    nis_pert_compliance = (nis_pert <= CHI2_GATE).mean() * 100.0

    # MKI at terminal TPE (eq. 8)
    mki = mean_tpe_pert_ss / R_L

    return dict(
        gamma_t=gamma_t,
        gamma_med=gamma_med,
        gamma_p05=gamma_p05,
        gamma_p95=gamma_p95,
        gamma_per_run_t=gamma_per_run_t,
        gamma_exceedance_pct=gamma_exceedance_pct,
        gamma_terminal_per_run=gamma_terminal_per_run,
        mean_cep_nom_ss=mean_cep_nom_ss,
        mean_cep_pert_ss=mean_cep_pert_ss,
        cep_delta=cep_delta,
        mean_tpe_nom_ss=mean_tpe_nom_ss,
        mean_tpe_pert_ss=mean_tpe_pert_ss,
        tpe_growth_pct=tpe_growth_pct,
        nis_nom_compliance=nis_nom_compliance,
        nis_pert_compliance=nis_pert_compliance,
        mki=mki,
    )


# ════════════════════════════════════════════════════════════════════════════
#  VERIFICATION TABLE
# ════════════════════════════════════════════════════════════════════════════

def print_verification_table(m):
    """Print the locked-value verification table."""
    print("\n" + "═" * 72)
    print("  VERIFICATION TABLE — v2.1 vs Manuscript Locked Values")
    print("═" * 72)
    fmt = "  {:<30s}  {:>12s}  {:>12s}  {}"
    print(fmt.format("Metric", "Manuscript", "Simulation", "Status"))
    print("  " + "─" * 68)

    checks = [
        ("Filter-reported CEP (m)",
         2.43, m["mean_cep_pert_ss"], 0.15),
        ("Nominal TPE (m)",
         2.60, m["mean_tpe_nom_ss"],  0.20),
        ("Perturbed TPE (m)",
         3.46, m["mean_tpe_pert_ss"], 0.25),
        ("TPE growth (%)",
         33.0, m["tpe_growth_pct"],   5.0),
        ("Γ(t) exceedance (%)",
         100.0, m["gamma_exceedance_pct"], 0.1),
        ("NIS compliance — perturbed (%)",
         95.0, m["nis_pert_compliance"], 3.0),
        ("MKI (R_L = 15 m)",
         0.53, m["mki"], 0.05),
    ]

    all_pass = True
    for name, target, result, tol in checks:
        diff = abs(result - target)
        ok   = diff <= tol
        all_pass = all_pass and ok
        status = "✓ PASS" if ok else f"✗ DIFF ({diff:+.3f})"
        print(fmt.format(name, f"{target:.3f}", f"{result:.3f}", status))

    print("  " + "─" * 68)
    overall = "✓  ALL CHECKS PASSED — archive verified" if all_pass \
              else "⚠  SOME CHECKS FAILED — investigate before archiving"
    print(f"\n  {overall}\n")
    print("═" * 72 + "\n")


# ════════════════════════════════════════════════════════════════════════════
#  PUBLICATION FIGURES
# ════════════════════════════════════════════════════════════════════════════

# Colour palette (colour-blind-safe, publication-ready)
C_NOM   = "#2ca02c"   # green
C_PERT  = "#1f77b4"   # blue
C_CRIT  = "#d62728"   # red
C_SHADE = "#aec7e8"   # light blue


def make_fig3(m, tpe_nom, tpe_pert, cep_nom, cep_pert):
    """Fig 3: Γ(t) temporal evolution — median + 5th–95th percentile band."""
    t_ax = np.arange(N_STEPS) * DT

    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    ax.fill_between(t_ax, m["gamma_p05"], m["gamma_p95"],
                    color=C_SHADE, alpha=0.55, label="5th–95th percentile")
    ax.plot(t_ax, m["gamma_med"],  color=C_PERT, lw=1.8, label="Median Γ(t) — perturbed")
    ax.axhline(GAMMA_CRIT, color=C_CRIT, lw=1.4, ls="--",
               label=f"Γ_crit = {GAMMA_CRIT}")
    ax.axhline(1.0, color=C_NOM, lw=1.2, ls="--",
               label="Nominal (Γ = 1)")

    ax.set_xlabel("Time (s)", fontsize=11)
    ax.set_ylabel("Γ(t)  —  Estimator Instability Number", fontsize=11)
    ax.set_title(
        "Fig. 3  Temporal evolution of Γ(t) under structured perturbation\n"
        f"3-D dual-sensor kinematic EKF, N = {N_RUNS}, v2.1",
        fontsize=10)
    ax.legend(fontsize=9, loc="upper left")
    ax.set_xlim(0, T_SIM)
    ax.set_ylim(bottom=0)
    ax.grid(True, alpha=0.35)

    out = OUT / "fig3_gamma_t.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    fig.savefig(OUT / "fig3_gamma_t.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  Saved: {out}")


def make_fig4(m, tpe_nom, tpe_pert, cep_nom, cep_pert):
    """Fig 4: Filter-reported CEP vs True Position Error (Confidently Wrong)."""
    t_ax = np.arange(N_STEPS) * DT

    fig = plt.figure(figsize=(11, 7))
    gs  = gridspec.GridSpec(2, 2, figure=fig, hspace=0.42, wspace=0.38)

    # (a) Nominal CEP vs TPE
    ax_a = fig.add_subplot(gs[0, 0])
    ax_a.plot(t_ax, cep_nom.mean(axis=0),  color=C_NOM,  lw=1.6, label="Filter CEP (nominal)")
    ax_a.plot(t_ax, tpe_nom.mean(axis=0),  color="grey", lw=1.2, ls="--", label="TPE (nominal)")
    ax_a.set_title("(a) Nominal — filter CEP ≈ TPE", fontsize=9)
    ax_a.set_xlabel("Time (s)"); ax_a.set_ylabel("Error (m)")
    ax_a.legend(fontsize=8); ax_a.grid(True, alpha=0.3)
    ax_a.set_xlim(0, T_SIM)

    # (b) Perturbed CEP vs TPE — the "Confidently Wrong" panel
    ax_b = fig.add_subplot(gs[0, 1])
    ax_b.plot(t_ax, cep_pert.mean(axis=0), color=C_CRIT, lw=1.8, label="Filter CEP (perturbed)")
    ax_b.plot(t_ax, tpe_pert.mean(axis=0), color=C_PERT, lw=1.6, ls="--", label="TPE (perturbed)")
    ax_b.plot(t_ax, cep_nom.mean(axis=0),  color=C_NOM,  lw=1.0, ls=":", alpha=0.7,
              label="Nominal CEP (ref.)")
    ax_b.set_title('(b) Perturbed — "Confidently Wrong" divergence', fontsize=9)
    ax_b.set_xlabel("Time (s)"); ax_b.set_ylabel("Error (m)")
    ax_b.legend(fontsize=8); ax_b.grid(True, alpha=0.3)
    ax_b.set_xlim(0, T_SIM)

    # (c) CEP delta over time
    ax_c = fig.add_subplot(gs[1, 0])
    cep_diff = cep_pert.mean(axis=0) - cep_nom.mean(axis=0)
    ax_c.plot(t_ax, cep_diff, color=C_CRIT, lw=1.4)
    ax_c.axhline(0, color="k", lw=0.8, ls="--")
    ax_c.set_title("(c) ΔCEP = CEP_perturbed − CEP_nominal", fontsize=9)
    ax_c.set_xlabel("Time (s)"); ax_c.set_ylabel("ΔCEP (m)")
    ax_c.grid(True, alpha=0.3); ax_c.set_xlim(0, T_SIM)

    # (d) Histogram of terminal TPE across runs
    ax_d = fig.add_subplot(gs[1, 1])
    terminal_tpe_nom  = tpe_nom[:,  -100:].mean(axis=1)
    terminal_tpe_pert = tpe_pert[:, -100:].mean(axis=1)
    bins = np.linspace(0, max(terminal_tpe_pert.max(), terminal_tpe_nom.max()) * 1.15, 45)
    ax_d.hist(terminal_tpe_nom,  bins=bins, color=C_NOM,  alpha=0.65,
              label=f"Nominal  (μ={terminal_tpe_nom.mean():.2f}m)")
    ax_d.hist(terminal_tpe_pert, bins=bins, color=C_PERT, alpha=0.65,
              label=f"Perturbed (μ={terminal_tpe_pert.mean():.2f}m)")
    ax_d.set_title("(d) Terminal TPE distribution, N = 500", fontsize=9)
    ax_d.set_xlabel("TPE (m)"); ax_d.set_ylabel("Count")
    ax_d.legend(fontsize=8); ax_d.grid(True, alpha=0.3)

    fig.suptitle(
        "Fig. 4  Filter-reported CEP and True Position Error under gate-compliant perturbation\n"
        f"3-D dual-sensor kinematic EKF, N = {N_RUNS}, v2.1",
        fontsize=10)

    out = OUT / "fig4_cep_tpe.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    fig.savefig(OUT / "fig4_cep_tpe.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  Saved: {out}")


def make_fig5(nis_nom, nis_pert):
    """Fig 5: NIS gate compliance — perturbed tracks nominal (invisible divergence)."""
    t_ax = np.arange(N_STEPS) * DT

    fig, axes = plt.subplots(1, 2, figsize=(11, 4.5), sharey=True)
    fig.suptitle(
        "Fig. 5  NIS gate compliance under structured perturbation\n"
        f"N = {N_RUNS}, 3-D dual-sensor EKF, v2.1",
        fontsize=10)

    for ax, data, label, colour, title in [
        (axes[0], nis_nom,  "Nominal",   C_NOM,  "(a) Nominal"),
        (axes[1], nis_pert, "Perturbed", C_PERT, "(b) Perturbed"),
    ]:
        med = np.median(data, axis=0)
        p05 = np.percentile(data, 5,  axis=0)
        p95 = np.percentile(data, 95, axis=0)
        ax.fill_between(t_ax, p05, p95, color=colour, alpha=0.25)
        ax.plot(t_ax, med, color=colour, lw=1.4, label=f"{label} NIS (median)")
        ax.axhline(CHI2_GATE, color=C_CRIT, lw=1.4, ls=":",
                   label=f"95% gate χ²_3 = {CHI2_GATE}")
        ax.set_title(title, fontsize=10)
        ax.set_xlabel("Time (s)", fontsize=10)
        ax.set_ylabel("NIS", fontsize=10)
        ax.legend(fontsize=9)
        ax.grid(True, alpha=0.3)
        ax.set_xlim(0, T_SIM)
        compliance = (data <= CHI2_GATE).mean() * 100
        ax.text(0.97, 0.96, f"Gate compliance: {compliance:.1f}%",
                transform=ax.transAxes, ha="right", va="top", fontsize=9,
                bbox=dict(boxstyle="round,pad=0.3", facecolor="white", alpha=0.8))

    out = OUT / "fig5_nis.pdf"
    fig.savefig(out, bbox_inches="tight", dpi=300)
    fig.savefig(OUT / "fig5_nis.png", bbox_inches="tight", dpi=300)
    plt.close(fig)
    print(f"  Saved: {out}")


# ════════════════════════════════════════════════════════════════════════════
#  OPTIONAL: SENSITIVITY SWEEP  (Appendix robustness check)
# ════════════════════════════════════════════════════════════════════════════

def run_sensitivity_sweep(amplitudes=(1.5, 2.5, 3.5), n_runs_sweep=200):
    """
    Run compact sensitivity sweep over A_PERT values.
    Uses n_runs_sweep runs per amplitude for speed.
    Produces Table IV: A_PERT vs Γ exceedance, ΔCEP, TPE growth.
    """
    print("\n  Running sensitivity sweep (A = 1.5, 2.5, 3.5 m) ...")
    results = []

    for A in amplitudes:
        # Temporarily patch the global profile
        k_arr  = np.arange(N_STEPS)
        dz_profile = np.column_stack([
            A * np.sin(OMEGA_PERT * k_arr),
            A * np.cos(OMEGA_PERT * k_arr),
            A * np.sin(OMEGA_PERT * k_arr + np.pi / 3),
        ])

        mse_n = np.empty((n_runs_sweep, N_STEPS))
        mse_p = np.empty((n_runs_sweep, N_STEPS))
        tpe_n = np.empty((n_runs_sweep, N_STEPS))
        tpe_p = np.empty((n_runs_sweep, N_STEPS))
        cep_p = np.empty((n_runs_sweep, N_STEPS))
        cep_n = np.empty((n_runs_sweep, N_STEPS))

        for i in range(n_runs_sweep):
            rng = np.random.default_rng(MASTER_SEED + 10000 + i)
            proc  = rng.multivariate_normal(np.zeros(N_STATES), Q_MAT,  N_STEPS)
            gnoise = rng.multivariate_normal(np.zeros(3),        R_GNSS, N_STEPS)
            rnoise = rng.normal(0, SIGMA_RANGE, N_STEPS)
            x0t   = X0 + rng.normal(0, 0.1, N_STATES)

            for use_p, mse_arr, tpe_arr, cep_arr in [
                (False, mse_n, tpe_n, cep_n),
                (True,  mse_p, tpe_p, cep_p),
            ]:
                x_t = x0t.copy()
                x_e = X0.copy()
                P_e = P0.copy()
                for k in range(N_STEPS):
                    x_t = F_MAT @ x_t + proc[k]
                    dz  = dz_profile[k] if use_p else np.zeros(3)
                    zg  = H_GNSS @ x_t + gnoise[k] + dz
                    zr  = range_h(x_t[:3], BEACON) + rnoise[k]
                    x_e, P_e, _ = ekf_step(x_e, P_e, zg, zr,
                                            F_MAT, Q_MAT, H_GNSS, R_GNSS,
                                            BEACON, R_RANGE)
                    err = x_t[:3] - x_e[:3]
                    mse_arr[i, k] = err @ err
                    tpe_arr[i, k] = np.sqrt(err @ err)
                    cep_arr[i, k] = cep_from_P(P_e)

        # Gamma per run
        gamma_pr = mse_p / np.maximum(mse_n, 1e-9)
        exc_pct  = (gamma_pr > GAMMA_CRIT).any(axis=1).mean() * 100

        ss = slice(-600, None)
        d_cep    = cep_p[:, ss].mean() - cep_n[:, ss].mean()
        tpe_grw  = (tpe_p[:, ss].mean() / max(tpe_n[:, ss].mean(), 1e-9) - 1) * 100

        results.append((A, exc_pct, d_cep, tpe_grw))
        print(f"    A = {A:.1f} m  |  Γ exc = {exc_pct:.0f}%  |  "
              f"ΔCEP = {d_cep:+.3f} m  |  TPE growth = {tpe_grw:+.1f}%")

    print("\n  Table IV — Sensitivity Sweep (Appendix)")
    print("  " + "─" * 58)
    print(f"  {'A_PERT (m)':<14} {'Γ exc (%)':<14} {'ΔCEP (m)':<14} {'TPE growth'}")
    print("  " + "─" * 58)
    for A, exc, dc, tg in results:
        print(f"  {A:<14.1f} {exc:<14.0f} {dc:<+14.3f} {tg:+.1f}%")
    print("  " + "─" * 58)

    return results


# ════════════════════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    run_sensitivity = "--sensitivity" in sys.argv

    # ── 1. Monte Carlo ────────────────────────────────────────────────────
    (mse_nom, mse_pert, tpe_nom, tpe_pert,
     cep_nom, cep_pert, nis_nom, nis_pert) = run_monte_carlo()

    # ── 2. Compute metrics ────────────────────────────────────────────────
    m = compute_metrics(mse_nom, mse_pert, tpe_nom, tpe_pert,
                        cep_nom, cep_pert, nis_nom, nis_pert)

    # ── 3. Verification table ─────────────────────────────────────────────
    print_verification_table(m)

    # ── 4. Figures ────────────────────────────────────────────────────────
    print("  Exporting publication figures ...")
    make_fig3(m, tpe_nom, tpe_pert, cep_nom, cep_pert)
    make_fig4(m, tpe_nom, tpe_pert, cep_nom, cep_pert)
    make_fig5(nis_nom, nis_pert)

    # ── 5. Sensitivity sweep (optional, --sensitivity flag) ───────────────
    if run_sensitivity:
        run_sensitivity_sweep()

    print(f"\n  All outputs written to: {OUT.resolve()}/")
    print("  Files: fig3_gamma_t.pdf/png  fig4_cep_tpe.pdf/png  fig5_nis.pdf/png\n")
    print("  ── Pre-archive validation complete ──")
    print("  Next steps:")
    print("    1. Confirm all PASS in the verification table above")
    print("    2. Copy PDF figures to manuscript figure directory")
    print("    3. git tag v2.1-final && git push --tags")
    print("    4. Create Zenodo release and freeze DOI\n")
