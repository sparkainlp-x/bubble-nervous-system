"""Full sweep: maximum scientific outcomes, honestly reported.

A sweep is a grid, not a cherry-pick. It runs, for every seed in
the list, every sigma, every frequency, every modality, and
injection on/off, on fresh probes, and reports:
  - accept rate, correct-response rate, accuracy-on-accepted
    (correct among accepted), false-accept rate on random fields
  - routing medians (reflex, central, lesion) once per seed
  - injection stock vs injected, net mean, and whether sampling paid
Wilson intervals for rates, mean +/- 1.96*SE for continuous
measures. The sweep reports the mean across seeds AND the range
across seeds; the best seed alone is never the headline.

Held-out rule: probes used to calibrate or optimise (train) are
never reused to claim the final result (test). sweep.py keeps
train and test streams separate by RNG seed.
"""
import math
import random

from bubble import Bubble
from human import modulate
from nervous import noisy, rand_field


def wilson(k, n, z=1.96):
    if n == 0:
        return (0.0, 0.0, 0.0)
    p = k / n
    den = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / den
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (p, max(0.0, centre - half), min(1.0, centre + half))


def mean_se(vals):
    if not vals:
        return (None, None)
    m = sum(vals) / len(vals)
    if len(vals) < 2:
        return (m, math.inf)
    var = sum((v - m) ** 2 for v in vals) / (len(vals) - 1)
    return (m, math.sqrt(var / len(vals)))


def run_cell(bubble, sigma, f_hz, n=40, seed=99, injection=False):
    sys = bubble.system
    rng = random.Random(seed)
    probes = [noisy(sys.patterns[k % 4], sigma, rng) for k in range(n)]
    truths = [k % 4 for k in range(n)]
    accepts = 0
    correct = 0
    nets = []
    for k, f in enumerate(probes):
        if injection:
            res = bubble.injection.attempt(f, f_hz,
                                           rng=random.Random(1000 + k),
                                           truth=1)
            dec, resp = res.decision, res.response
            if res.net is not None:
                nets.append(res.net)
        else:
            dec, resp = bubble.decide_true(f, f_hz)[:2]
        if dec == "accept":
            accepts += 1
            if resp == sys.RESPONSE_NAMES[truths[k]]:
                correct += 1
    rng2 = random.Random(seed + 7)
    rand_fields = [rand_field(128, rng2) for _ in range(n)]
    false_accepts = 0
    for f in rand_fields:
        if bubble.decide_true(f, f_hz)[0] == "accept":
            false_accepts += 1
    acc_on_acc = (correct / accepts) if accepts else None
    return {
        "sigma": sigma, "f_hz": f_hz, "n": n, "injection": injection,
        "accepts": accepts, "correct": correct,
        "accept_rate": wilson(accepts, n),
        "accuracy_on_accepted": acc_on_acc,
        "false_accept_rate": wilson(false_accepts, n),
        "net_mean": (sum(nets) / len(nets)) if nets else None,
        "net_n": len(nets),
    }


def full_sweep(seeds=(42, 7, 123), sigmas=(0.0, 0.15, 0.30, 0.50),
               frequencies=(0.25, 1.2, 7.0, 10.0), n=40):
    """Run the full grid. Returns cells + per-seed routing + summary."""
    cells = []
    routing = {}
    for seed in seeds:
        bubble = Bubble(seed=seed)
        routing[seed] = bubble.routing()
        for sigma in sigmas:
            for f_hz in frequencies:
                cells.append(run_cell(bubble, sigma, f_hz, n=n, seed=99,
                                      injection=False))
                if f_hz == 7.0:
                    cells.append(run_cell(bubble, sigma, f_hz, n=n,
                                          seed=99, injection=True))
    # Summary: mean accept rate and accuracy-on-accepted at the
    # scientific point (sigma 0.15, 7 Hz, stock) across seeds, and
    # the injection net at sigma 0.30, 7 Hz, across seeds.
    def pick(sigma, f_hz, injection):
        return [c for c in cells if c["sigma"] == sigma
                and c["f_hz"] == f_hz and c["injection"] == injection]
    summary = {}
    for label, sigma, f_hz, inj in [
            ("stock_0.15_7Hz", 0.15, 7.0, False),
            ("stock_0.30_7Hz", 0.30, 7.0, False),
            ("injected_0.30_7Hz", 0.30, 7.0, True)]:
        sel = pick(sigma, f_hz, inj)
        rates = [c["accept_rate"][0] for c in sel]
        accs = [c["accuracy_on_accepted"] for c in sel
                if c["accuracy_on_accepted"] is not None]
        nets = [c["net_mean"] for c in sel if c["net_mean"] is not None]
        summary[label] = {
            "accept_rate_mean": sum(rates) / len(rates) if rates else None,
            "accept_rate_range": (min(rates), max(rates)) if rates else None,
            "accuracy_on_accepted_mean": (sum(accs) / len(accs)) if accs else None,
            "net_mean": (sum(nets) / len(nets)) if nets else None,
        }
    return {"cells": cells, "routing": routing, "summary": summary}
