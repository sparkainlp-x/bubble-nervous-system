"""Demo for bubble-nervous-system v0.1.0.
Run: python demo.py
Steps, in order: bubble -> observer -> calibrator (refused, then
applied) -> full sweep -> optimizer with held-out test -> passport.
"""
from bubble import Bubble
from calibrator import Calibrator
from observer import Observer
from optimizer import optimise
from sweep import full_sweep


def main():
    print("bubble-nervous-system v0.1.0 — full nervous system in a bubble")
    b = Bubble(seed=42)
    print(f"inside: 128 neurons, 4 responses, frozen tau = {b.true_tau:.3f}, J = {b.true_j:.3f}")
    print(f"assumed before calibration: tau = {b.assumed_tau:.2f}, freq = {b.assumed_freq_hz} Hz, p0 = {b.assumed_p0:.2f}")
    obs = Observer(b, sigma=0.05, seed=42)
    r = obs.measure_routing()
    print(f"observer routing (REPORTED): reflex = {r.value['reflex']:.2f}, central = {r.value['central']:.2f}, lesion_reflex = {r.value['lesion_reflex']}")
    g = obs.measure_gate()
    print(f"observer gate: {len(g.value['in'])} in + {len(g.value['ood'])} ood reports, half-width = {g.half_width:.3f}")
    f = obs.measure_frequency()
    print(f"observer frequency accepts: {f.value}")
    i = obs.measure_injection()
    print(f"observer injection: stock {i.value['stock']}/40, injected {i.value['injected']}/40, net mean = {i.value['net_mean']:.3f}, random injected = {i.value['random_injected']}/40")
    cal = Calibrator(b)
    # First, refused: no review signoff yet.
    calib, fail = cal.calibrate(obs.reports)
    print(f"calibration before signoff: {'refused: ' + fail.reason if fail else 'applied'}")
    b.set_review_signoff(True)
    calib, fail = cal.calibrate(obs.reports)
    if fail:
        print(f"calibration after signoff: refused: {fail.reason}")
    else:
        print(f"calibration after signoff: tau = {calib['tau']:.3f} (J = {calib['tau_j']:.3f}), freq = {calib['freq_hz']} Hz, injection_on = {calib['injection_on']}, net mean = {calib['injection_net_mean']:.3f}")
        cal.apply(calib)
        print(f"assumed after calibration: tau = {b.assumed_tau:.3f}, freq = {b.assumed_freq_hz} Hz")
    print("full sweep (3 seeds, 4 sigmas, 4 frequencies, injection at 7 Hz)...")
    sw = full_sweep()
    for label, s in sw["summary"].items():
        print(f"  {label}: accept mean = {s['accept_rate_mean']:.3f}, range = {s['accept_rate_range']}, accuracy-on-accepted mean = {s['accuracy_on_accepted_mean']}, net mean = {s['net_mean']}")
    print(f"routing across seeds: {sw['routing']}")
    print("optimizer (train grid, held-out test)...")
    opt = optimise(Bubble(seed=42))
    if opt["refused"]:
        print(f"  refused: {opt['reason']}")
    else:
        print(f"  train best: tau = {opt['train_best']['tau']:.2f}, freq = {opt['train_best']['f_hz']} Hz, accuracy-on-accepted = {opt['train_best']['accuracy_on_accepted']:.3f}")
        print(f"  held-out test: accuracy-on-accepted = {opt['test']['accuracy_on_accepted']:.3f}, false-accept = {opt['test']['false_accept_rate']:.3f}")
        print(f"  frozen gate on same test: accuracy-on-accepted = {opt['frozen_test']['accuracy_on_accepted']:.3f}")
        print(f"  improvement (test, shadow - frozen) = {opt['improvement_test']:.3f}")
    print("headline: WITHHELD — synthetic, observer-reported data only.")


if __name__ == "__main__":
    main()
