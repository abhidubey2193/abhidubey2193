import unittest
from control_tower import assess, report

class TestAssessment(unittest.TestCase):
    def test_safe_job(self):
        self.assertEqual(assess({"id": "1", "tasks": []})["risk"], "LOW")
    def test_scheduled_blocks_promotion(self):
        r = assess({"scheduled": True})
        self.assertIn("scheduled", r["blockers"])
        self.assertFalse(r["promotion_permitted"])
    def test_summary(self):
        r = report({"jobs": [{"legacy_mounts": True, "init_scripts": ["x"]}, {}]})
        self.assertEqual(r["summary"]["high_risk"], 1)
        self.assertEqual(r["summary"]["total_jobs"], 2)
if __name__ == "__main__": unittest.main()
