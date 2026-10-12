import unittest
from nexarack.benchmarks import BenchmarkRecord,create_benchmark_report
class BenchmarkTests(unittest.TestCase):
 def test_error(self):
  r=BenchmarkRecord('matrix','fp16',8,100,8,12,10); self.assertAlmostEqual(r.prediction_error_percent,20); report=create_benchmark_report([r]); self.assertAlmostEqual(report['mean_absolute_error_percent'],20)
if __name__=='__main__': unittest.main()
