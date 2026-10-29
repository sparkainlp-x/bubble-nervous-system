# Bubble Nervous System v0.1.0

The full membrane-nervous-system, inside a bubble, with an external
observer and an external calibrator, built for maximum scientific
outcomes — meaning: the most honest, reproducible, and testable
outcomes, not the most flattering numbers.

## What is inside

Vendored unchanged from membrane-nervous-system v0.2.0:
`nervous.py` (128 neurons: sensory 40, spinal 32, central 24, motor 32,
4 responses: withdraw, grasp, balance, cool-alert, gate tau frozen by
Youden's J), `human.py` (imposed Gaussian frequency sensitivity,
centre 7.0 Hz, width 1.5 Hz), `injection.py` (Crystallize injection
on rejection only, p0 0.75, 20 variants, cost 0.01 per sample, tau
frozen, patterns never added).

## What is outside

- `bubble.py` — the boundary. Holds the system, keeps assumed vs
  true parameters apart, and exposes only the assumed model publicly.
- `observer.py` — measures routing, gate overlaps, frequency accepts,
  and injection outcomes, with declared noise (sigma 0.05), tagged
  REPORTED, never MEASURED. Measuring does not mutate the system.
- `calibrator.py` — estimates tau, frequency, and injection on/off
  from reports only, or refuses (missing signoff, <3 reports, or
  half-width >= 0.20). Applying a calibration changes the ASSUMED
  model only; the frozen true gate is never overwritten.
- `sweep.py` — the full grid: 3 seeds, 4 sigmas, 4 frequencies,
  injection at 7 Hz, with Wilson intervals and mean + range across
  seeds, never the best seed alone.
- `optimizer.py` — grid search on train probes, subject to
  false-accept <= 0.05 and accept >= 0.50, with the final result on
  held-out test probes.
- `passport.py` — SHA-256 seal over code + parameters + results.
  Headline always WITHHELD here: synthetic, observer-reported data.

## Run

```
python demo.py
python3 -m unittest tests -v
```

## Honest limits

NOT a human nervous system, NOT neuroscience, NOT a medical device,
NOT a diagnosis, NOT a measurement of any real person. Synthetic
classical toy only. Calibration improves the assumed model, not the
true system. Injection at sigma 0.30, 7 Hz, does not pay for itself
(net mean negative) — that negative is kept in the record. A lesion
breaks the reflex route in the graph; that is a graph property, not
a claim about real lesions.

## Credits

Project author: Jean-François Brisson (Spark).
Related work: Mun Seok Lee's Digital to Wave paradigm (Zenodo
records 21947036 and 21947108) is cited as inspiration for the wave
and membrane work; this source citation does not indicate package
coauthorship. Brisson built the package's new code with AI
assistance. Vendored components retain their upstream attributions
and license terms, as documented in DESIGN.md.
