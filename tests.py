"""Tests for bubble-nervous-system v0.1.0.
Run: python3 -m unittest tests -v"""
import math
import unittest

from bubble import Bubble
from calibrator import Calibrator
from observer import Observer
from optimizer import optimise
from passport import headline_allowed
from sweep import full_sweep, run_cell


class TestBubble(unittest.TestCase):
    def setUp(self):
        self.b = Bubble(seed=42)

    def test_full_system_inside(self):
        self.assertEqual(self.b.system.geometry.n, 128)
        self.assertEqual(len(self.b.system.patterns), 4)
        self.assertEqual(self.b.system.RESPONSE_NAMES,
                         ("withdraw", "grasp", "balance", "cool-alert"))
        self.assertIsNotNone(self.b.true_tau)

    def test_routing_reflex_shorter_and_lesion_breaks(self):
        r = self.b.routing()
        self.assertLess(r["reflex"], r["central"])
        self.assertTrue(math.isinf(r["lesion_reflex"]))
        self.assertTrue(math.isfinite(r["central"]))

    def test_observer_does_not_mutate(self):
        tau0 = self.b.system.tau
        n0 = len(self.b.system.patterns)
        obs = Observer(self.b, sigma=0.05)
        obs.measure_routing()
        obs.measure_gate()
        obs.measure_frequency()
        self.assertEqual(self.b.system.tau, tau0)
        self.assertEqual(len(self.b.system.patterns), n0)

    def test_observer_reports_tagged(self):
        obs = Observer(self.b, sigma=0.05)
        rep = obs.measure_routing()
        self.assertEqual(rep.tag, "REPORTED")
        self.assertTrue(math.isinf(rep.value["lesion_reflex"]))

    def test_calibrator_refuses_without_signoff(self):
        obs = Observer(self.b, sigma=0.05)
        obs.measure_routing(); obs.measure_gate(); obs.measure_frequency(); obs.measure_injection()
        cal = Calibrator(self.b)
        out, fail = cal.calibrate(obs.reports)
        self.assertIsNone(out)
        self.assertEqual(fail.reason, "review_signoff_missing")

    def test_calibrator_refuses_too_few_reports(self):
        self.b.set_review_signoff(True)
        cal = Calibrator(self.b)
        out, fail = cal.calibrate([])
        self.assertIsNone(out)
        self.assertEqual(fail.reason, "too_few_reports")

    def test_calibrator_applies_to_assumed_only(self):
        obs = Observer(self.b, sigma=0.05)
        obs.measure_routing(); obs.measure_gate(); obs.measure_frequency(); obs.measure_injection()
        self.b.set_review_signoff(True)
        cal = Calibrator(self.b)
        out, fail = cal.calibrate(obs.reports)
        self.assertIsNone(fail)
        self.assertIn("tau", out)
        self.assertIn("freq_hz", out)
        tau_true = self.b.system.tau
        cal.apply(out)
        self.assertEqual(self.b.system.tau, tau_true)
        self.assertAlmostEqual(self.b.assumed_tau, out["tau"])

    def test_calibrator_frequency_is_7hz(self):
        obs = Observer(self.b, sigma=0.05)
        obs.measure_routing(); obs.measure_gate(); obs.measure_frequency(); obs.measure_injection()
        self.b.set_review_signoff(True)
        cal = Calibrator(self.b)
        out, fail = cal.calibrate(obs.reports)
        self.assertEqual(out["freq_hz"], 7.0)

    def test_injection_net_negative_kept(self):
        obs = Observer(self.b, sigma=0.05)
        rep = obs.measure_injection()
        self.assertLess(rep.value["net_mean"], 0)
        self.assertEqual(rep.value["stock"], 19)
        self.assertEqual(rep.value["injected"], 21)

    def test_sweep_cell_reproducible(self):
        c1 = run_cell(Bubble(seed=42), 0.15, 7.0, n=40, seed=99, injection=False)
        c2 = run_cell(Bubble(seed=42), 0.15, 7.0, n=40, seed=99, injection=False)
        self.assertEqual(c1["accepts"], c2["accepts"])
        self.assertGreaterEqual(c1["accepts"], 35)

    def test_optimizer_held_out_not_worse_than_chance(self):
        opt = optimise(Bubble(seed=42))
        if not opt["refused"]:
            self.assertGreaterEqual(opt["test"]["accuracy_on_accepted"], 0.25)
            self.assertLessEqual(opt["test"]["false_accept_rate"], 0.10)

    def test_headline_withheld(self):
        self.assertFalse(headline_allowed("synthetic", 1.0))
        self.assertFalse(headline_allowed("reported", 1.0))
        self.assertTrue(headline_allowed("measured", 0.5))


if __name__ == "__main__":
    unittest.main()
