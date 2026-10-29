# Preregistration — bubble-nervous-system v0.1.0

Before any demo run, the rules are fixed:

- Inside the bubble: membrane-nervous-system v0.2.0, vendored unchanged
  (nervous.py, human.py, injection.py). 128 neurons, 4 responses,
  gate calibrated once (100 in, 100 random, sigma 0.15, seed 11),
  tau frozen by midpoint-of-max-J, patterns never added, rescued
  probes never stored.
- Outside: Observer (sigma 0.05, REPORTED only) and Calibrator
  (gates + >=3 reports + half-width < 0.20, or refuse).
- Calibrator estimates tau by Youden's J on reported overlaps,
  frequency by highest reported accept rate, injection ON only if
  reported net lower bound > 0 and injected > stock.
- Sweep: seeds (42, 7, 123), sigmas (0.0, 0.15, 0.30, 0.50),
  frequencies (0.25, 1.2, 7.0, 10.0), n=40 per cell, injection at
  7 Hz only. Summary reports mean AND range across seeds.
- Optimizer: grid tau 0.00-1.00 step 0.01, frequencies as above,
  objective accuracy-on-accepted on train, constraints
  false-accept <= 0.05 and accept >= 0.50 on train, final result
  on held-out test probes (different RNG stream).
- Headline: WITHHELD always in this package. All data are synthetic
  and observer-reported, so no headline is allowed by the passport rule.

Bars, fixed before running:
- Observer must not mutate tau or patterns (tested).
- Calibrator must refuse without review signoff (tested).
- Injection at sigma 0.30, 7 Hz must stay net-negative in the record;
  it must not be tuned away to look positive.
- Lesion must break reflex (inf) while central stays finite.
- Optimizer test false-accept must stay <= 0.10, or the result is
  reported as a failure, not a success.
