"""Tests for Model Cascade Confidence Router."""
import unittest
from model_cascade_confidence_router.core import ModelCascadeRouter


class TestModelCascadeRouter(unittest.TestCase):
    def test_accepts_high_confidence_valid_draft(self):
        r = ModelCascadeRouter(confidence_threshold=0.8)
        res = r.evaluate_draft('{"status": "ok"}', confidence=0.91, valid_schema=True)
        self.assertFalse(res["escalated"])
        self.assertEqual(res["selected_tier"], "fast")

    def test_escalates_hedging_or_invalid_schema(self):
        r = ModelCascadeRouter(confidence_threshold=0.8)
        res_hedge = r.evaluate_draft("I am not sure about that.", confidence=0.95, valid_schema=True)
        res_schema = r.evaluate_draft("broken", confidence=0.95, valid_schema=False)
        self.assertTrue(res_hedge["escalated"])
        self.assertEqual(res_hedge["reason"], "hedging_detected")
        self.assertEqual(res_schema["reason"], "invalid_output_schema")
        self.assertEqual(r.stats()["escalation_rate"], 1.0)
