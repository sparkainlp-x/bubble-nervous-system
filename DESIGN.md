# DESIGN — bubble-nervous-system v0.1.0

## Why a bubble

The scientific gain is separation. Without a bubble, the system,
the measurement, and the model are the same code, so a calibration
can look like it improved the system when it only moved the ruler.
With a bubble, three things are distinct and testable:
1. True system (inside, frozen gate, true routing, true frequency).
2. Observer reports (outside, noisy, REPORTED, non-intervening).
3. Assumed model (outside, calibrated from reports, evaluated as
   a shadow against the frozen gate on held-out probes).

## Why maximum outcomes means maximum honesty

A package that reports only its best seed, only its best tau, or
only its best frequency is not maximising scientific outcomes; it
is maximising a headline. This package therefore:
- sweeps the full grid, reports mean and range across seeds;
- optimises on train and reports on test, never the reverse;
- keeps negatives: injection net-negative at sigma 0.30, lesion
  breaking reflex, random probes refused, off-frequency probes
  rejected;
- refuses calibration when evidence is thin, noisy, or unsigned;
- withholds the headline by rule, because the data are synthetic.

## What calibration can and cannot do

Can: move assumed tau, assumed frequency, and assumed injection
commit closer to the true values, as measured by held-out shadow
accuracy, with a confidence bound.
Cannot: change the true gate, change true routing, change true
frequency sensitivity, rescue an off-frequency probe, or turn a
synthetic toy into evidence about a real nervous system.

## Files

- nervous.py, human.py, injection.py, LICENSE: vendored, unchanged
- bubble.py, observer.py, calibrator.py: the boundary and its two
  external roles
- sweep.py, optimizer.py, passport.py: grid, held-out optimisation,
  evidence seal
- demo.py, tests.py, PREREG.md, README.md, DESIGN.md: run, verify,
  preregister, explain, design
- Private work: excluded entirely, never imported.
