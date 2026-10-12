from nexarack.config import load_config
from nexarack.engine import SimulationEngine
e=SimulationEngine(load_config()); job=e.submit('matrix',operations_tflop=500,memory_gib=24,gpu_count=8); report=e.run(10); print(job.to_dict()); print(report['metrics'])
