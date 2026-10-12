import unittest
from nexarack.config import load_config
from nexarack.engine import SimulationEngine
class EngineTests(unittest.TestCase):
 def setUp(self): self.e=SimulationEngine(load_config())
 def test_inventory(self):
  i=self.e.rack.inventory(); self.assertEqual(i['gpu_count'],72); self.assertEqual(i['cpu_count'],36); self.assertAlmostEqual(i['gpu_memory_total_tib'],13.5)
 def test_completion_and_release(self):
  j=self.e.submit('matrix',operations_tflop=1,memory_gib=10,gpu_count=1); self.e.run(5); self.assertEqual(j.status,'completed'); self.assertAlmostEqual(self.e.rack.gpus[j.assigned_gpu_ids[0]].memory_used_gib,0)
 def test_gpu_limit(self):
  with self.assertRaises(ValueError): self.e.submit('matrix',gpu_count=73)
 def test_memory_limit(self):
  with self.assertRaises(ValueError): self.e.submit('matrix',memory_gib=193,gpu_count=1)
 def test_invalid_tick(self):
  with self.assertRaises(ValueError): self.e.tick(0)
if __name__=='__main__': unittest.main()
