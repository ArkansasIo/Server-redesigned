import argparse,json
from pathlib import Path
from .config import load_config
from .engine import SimulationEngine
from .reporting import write_json
from .benchmarks import BenchmarkRecord,create_benchmark_report,write_benchmark_report
def main():
 p=argparse.ArgumentParser(prog='nexarack'); sub=p.add_subparsers(dest='cmd',required=True); i=sub.add_parser('info'); i.add_argument('--config'); r=sub.add_parser('run'); r.add_argument('--config'); r.add_argument('--seconds',type=float,default=10); r.add_argument('--tick',type=float,default=1); r.add_argument('--workload',choices=['matrix','llm-inference','distributed-training','memory-bandwidth'],default='matrix'); r.add_argument('--operations-tflop',type=float); r.add_argument('--memory-gib',type=float); r.add_argument('--gpus',type=int,default=8); r.add_argument('--precision',choices=['fp8','fp16'],default='fp16'); r.add_argument('--output'); b=sub.add_parser('benchmark-report'); b.add_argument('--input',required=True); b.add_argument('--output',default='outputs/benchmark-report.json'); b.add_argument('--profile',default='NexaRack'); a=p.parse_args(); e=SimulationEngine(load_config(getattr(a,'config',None)))
 if a.cmd=='info': print(json.dumps(e.rack.inventory(),indent=2))
 elif a.cmd=='run':
  e.submit(a.workload,a.operations_tflop,a.memory_gib,a.gpus,a.precision); result=e.run(a.seconds,a.tick); print(f'Report saved: {write_json(result,a.output)}' if a.output else json.dumps(result,indent=2))
 else:
  records=[BenchmarkRecord(**x) for x in json.loads(Path(a.input).read_text(encoding='utf-8'))]; report=create_benchmark_report(records,a.profile); print(f'Report saved: {write_benchmark_report(report,a.output)}')
if __name__=='__main__': main()
