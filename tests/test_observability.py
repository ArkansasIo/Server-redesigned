import unittest
from nexarack.benchmarks import BenchmarkRecord,create_benchmark_report
from nexarack.timeline import WorkloadTimeline
from nexarack.workloads import create_workload
class ObservabilityTests(unittest.TestCase):
 def test_timeline_records_job(self):
  timeline=WorkloadTimeline(); job=create_workload('matrix',gpu_count=1); timeline.record('queued',job,0); self.assertEqual(timeline.snapshot()[0]['event'],'queued'); self.assertEqual(timeline.snapshot()[0]['job_id'],job.id)
 def test_benchmark_error(self):
  record=BenchmarkRecord('matrix','fp16',8,100,8,12,10); self.assertAlmostEqual(record.prediction_error_percent,20); report=create_benchmark_report([record]); self.assertEqual(report['record_count'],1); self.assertAlmostEqual(report['mean_absolute_error_percent'],20)
if __name__=='__main__': unittest.main()
