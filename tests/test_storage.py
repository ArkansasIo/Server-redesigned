import tempfile
import unittest
from pathlib import Path

from nexarack.storage import SimulationStore


class StorageTests(unittest.TestCase):
    def test_snapshot_round_trip(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SimulationStore(Path(directory) / "state.sqlite3")
            snapshot = {"simulation_seconds": 3.5, "metrics": {"gpu_count": 8}, "jobs": []}
            key = store.save_snapshot(snapshot)
            self.assertEqual(key, 1)
            rows = store.list_snapshots()
            self.assertEqual(rows[0]["snapshot"], snapshot)
            self.assertEqual(rows[0]["simulation_seconds"], 3.5)

    def test_job_upsert(self):
        with tempfile.TemporaryDirectory() as directory:
            store = SimulationStore(Path(directory) / "state.sqlite3")
            store.save_job({"id": "job-1", "status": "queued"})
            store.save_job({"id": "job-1", "status": "completed", "result": {"ok": True}})
            rows = store.list_jobs()
            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["status"], "completed")

    def test_limit_validation(self):
        store = SimulationStore(":memory:")
        with self.assertRaises(ValueError):
            store.list_jobs(0)


if __name__ == "__main__":
    unittest.main()
