#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys, re, math, os
import numpy as np
from scipy.optimize import minimize

LOG10 = math.log(10.0)

def logistic(z):
    return 1.0 / (1.0 + math.exp(-z))

def elo_from_z(z):
    return z * 400.0 / LOG10

def parse_log(text):
    # Candidate model name (Engine B)
    m_b = re.search(r'第二引擎设置.*?-model\s+"([^"]+)"', text, re.S)
    model_b = os.path.basename(m_b.group(1)) if m_b else "EngineB"

    # 总局数: 20 比分: 11:9
    m_tot = re.search(r"总局数[:：]\s*([0-9]+)\s+比分[:：]\s*([0-9]+)\s*[:：]\s*([0-9]+)", text)
    total_games = int(m_tot.group(1)) if m_tot else 0
    wins_a_total = int(m_tot.group(2)) if m_tot else 0
    wins_b_total = int(m_tot.group(3)) if m_tot else 0

    # 引擎1 (Baseline)
    m_e1 = re.search(
        r"引擎1.*?总胜局[:：]\s*([0-9]+).*?执黑胜局[:：]\s*([0-9]+).*?执白胜局[:：]\s*([0-9]+).*?总用时[:：]\s*([0-9.]+).*?总计算量[:：]\s*([0-9,]+)",
        text, re.S)
    if m_e1:
        wins_a_total = int(m_e1.group(1))
        wins_a_black = int(m_e1.group(2))
        wins_a_white = int(m_e1.group(3))
        avg_time_a = float(m_e1.group(4))
        playouts_a = int(m_e1.group(5).replace(",", ""))
    else:
        wins_a_black = wins_a_white = 0
        avg_time_a = 0.0
        playouts_a = 0

    # 引擎2 (Candidate)
    m_e2 = re.search(
        r"引擎2.*?总胜局[:：]\s*([0-9]+).*?执黑胜局[:：]\s*([0-9]+).*?执白胜局[:：]\s*([0-9]+).*?总用时[:：]\s*([0-9.]+).*?总计算量[:：]\s*([0-9,]+)",
        text, re.S)
    if m_e2:
        wins_b_total = int(m_e2.group(1))
        wins_b_black = int(m_e2.group(2))
        wins_b_white = int(m_e2.group(3))
        avg_time_b = float(m_e2.group(4))
        playouts_b = int(m_e2.group(5).replace(",", ""))
    else:
        wins_b_black = wins_b_white = 0
        avg_time_b = 0.0
        playouts_b = 0

    return {
        "model_b": model_b,
        "total_games": total_games,
        "wins_a_total": wins_a_total, "wins_b_total": wins_b_total,
        "wins_a_black": wins_a_black, "wins_a_white": wins_a_white,
        "avg_time_b": avg_time_b, "playouts_b": playouts_b
    }

def fit_two_color(kb, nb, kw, nw):
    def nll(theta):
        z0, g = theta
        pb = logistic(z0 + g); pw = logistic(z0 - g)
        eps = 1e-12
        ll = kb*math.log(pb+eps)+(nb-kb)*math.log(1-pb+eps) \
           + kw*math.log(pw+eps)+(nw-kw)*math.log(1-pw+eps)
        return -ll
    res = minimize(nll, [0,0], method="BFGS")
    return res.x

def main():
    text = sys.stdin.read()
    info = parse_log(text)
    n = info["total_games"]
    nb = nw = n//2
    kb, kw = info["wins_a_black"], info["wins_a_white"]

    z0, g = fit_two_color(kb, nb, kw, nw)
    elo_ab = elo_from_z(z0)  # baseline minus candidate
    baseline = 14085

    # Candidate perspective
    elo_diff_b = -elo_ab
    calc_elo_b = baseline + elo_diff_b

    # === Full Report (Baseline perspective) ===
    print("=== Elo Report ===")
    print(f"Games: {n}, Score A:B = {info['wins_a_total']}:{info['wins_b_total']}")
    print(f"Elo(A−B): {elo_ab:.2f}")
    print(f"Color advantage (A as Black): {elo_from_z(g):.2f}")
    print(f"Win rate A: {100.0*info['wins_a_total']/n:.1f}%")
    print(f"Baseline Elo: {baseline}")
    print(f"Calculated Elo (A): {baseline + elo_ab:.2f}")

    # === One-line Summary (Candidate perspective) ===
    wins = info['wins_b_total']
    losses = info['wins_a_total']
    winrate = round(100.0 * wins / n, 1)
    print()
    print(f"{info['model_b']}\t{n}\t{wins}\t{losses}\t{winrate}\t"
          f"{info['avg_time_b']:.3f}\t{info['playouts_b']:,}\t"
          f"{baseline}\t{elo_diff_b:.2f}\t{calc_elo_b:.2f}")

if __name__ == "__main__":
    main()
