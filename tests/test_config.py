import unittest
from nexarack.config import load_config
class ConfigTests(unittest.TestCase):
 def test_profile_topology(self):
  c=load_config(); self.assertEqual(c['topology']['trays']*c['topology']['gpus_per_tray'],72)
if __name__=='__main__': unittest.main()
