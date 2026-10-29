"""Optimizer: grid-search the assumed model, with held-out validation.

Objective, stated before any search:
  maximise accuracy-on-accepted on TRAIN probes
  subject to false-accept rate <= 0.05 on TRAIN random fields
  and accept rate >= 0.50 on TRAIN in-distribution probes
  (a gate that accepts almost nothing is not a better gate).
Grid: tau 0.00..1.00 step 0.01, frequency in (0.25, 1.2, 7.0, 10.0).
The best TRAIN point is then evaluated once on TEST probes
(different RNG stream). The TEST number is the reported result;
the TRAIN number is never the headline. If no grid point satisfies
the constraints, the optimizer refuses and returns the frozen gate
as the baseline, with the failure kept in the record.
"""
import random

from bubble import Bubble
from nervous import noisy, rand_field


def evaluate_shadow(bubble, tau, f_hz, probes, truths, rand_fields):
    accepts = 0
    correct = 0
    for f, t in zip(probes, truths):
        dec, resp, _ = bubble.decide_shadow(f, f_hz, tau=tau, freq_hz=f_hz)
        if dec == "accept":
            accepts += 1
            if resp == bubble.system.RESPONSE_NAMES[t]:
                correct += 1
    false_accepts = sum(1 for f in rand_fields
                        if bubble.decide_shadow(f, f_hz, tau=tau, freq_hz=f_hz)[0] == "accept")
    return {
        "tau": tau, "f_hz": f_hz,
        "accept_rate": accepts / len(probes) if probes else 0.0,
        "accuracy_on_accepted": (correct / accepts) if accepts else 0.0,
        "false_accept_rate": false_accepts / len(rand_fields) if rand_fields else 0.0,
        "accepts": accepts, "correct": correct,
    }


def optimise(bubble, sigma=0.15, n_train=100, n_test=100):
    sys = bubble.system
    rng = random.Random(201)
    train_probes = [noisy(sys.patterns[k % 4], sigma, rng) for k in range(n_train)]
    train_truths = [k % 4 for k in range(n_train)]
    train_rand = [rand_field(128, rng) for _ in range(n_train)]
    rng2 = random.Random(202)
    test_probes = [noisy(sys.patterns[k % 4], sigma, rng2) for k in range(n_test)]
    test_truths = [k % 4 for k in range(n_test)]
    test_rand = [rand_field(128, rng2) for _ in range(n_test)]
    best = None
    for tau_i in range(101):
        tau = tau_i / 100.0
        for f_hz in (0.25, 1.2, 7.0, 10.0):
            ev = evaluate_shadow(bubble, tau, f_hz, train_probes,
                                 train_truths, train_rand)
            if ev["false_accept_rate"] > 0.05:
                continue
            if ev["accept_rate"] < 0.50:
                continue
            if best is None or ev["accuracy_on_accepted"] > best["accuracy_on_accepted"]:
                best = ev
    if best is None:
        return {"refused": True, "reason": "no_grid_point_meets_constraints",
                "baseline_tau": bubble.true_tau, "baseline_freq": 7.0}
    test_ev = evaluate_shadow(bubble, best["tau"], best["f_hz"],
                              test_probes, test_truths, test_rand)
    # Frozen-gate baseline on the same test probes, for comparison.
    frozen_accepts = 0
    frozen_correct = 0
    for f, t in zip(test_probes, test_truths):
        dec, resp = bubble.decide_true(f, 7.0)[:2]
        if dec == "accept":
            frozen_accepts += 1
            if resp == sys.RESPONSE_NAMES[t]:
                frozen_correct += 1
    frozen = {
        "accept_rate": frozen_accepts / len(test_probes),
        "accuracy_on_accepted": (frozen_correct / frozen_accepts) if frozen_accepts else 0.0,
    }
    return {"refused": False, "train_best": best, "test": test_ev,
            "frozen_test": frozen,
            "improvement_test": test_ev["accuracy_on_accepted"] - frozen["accuracy_on_accepted"]}
