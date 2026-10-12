from nexarack.config import load_config
from nexarack.engine import SimulationEngine
e=SimulationEngine(load_config()); job=e.submit('llm-inference',memory_gib=120,gpu_count=4,precision='fp8'); report=e.run(30); print(job.to_dict()); print(report['metrics']['power'])
