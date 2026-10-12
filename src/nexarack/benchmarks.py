from dataclasses import dataclass,asdict
from datetime import datetime,timezone
import json
from pathlib import Path
@dataclass(slots=True)
class BenchmarkRecord:
    workload:str; precision:str; gpu_count:int; operations_tflop:float; memory_gib:float; predicted_seconds:float; measured_seconds:float|None=None; notes:str=''
    @property
    def prediction_error_percent(self): return None if self.measured_seconds is None or self.measured_seconds<=0 else (self.predicted_seconds-self.measured_seconds)/self.measured_seconds*100
    def to_dict(self): d=asdict(self); d['prediction_error_percent']=self.prediction_error_percent; return d
def create_benchmark_report(records,profile='NexaRack'):
    errors=[r.prediction_error_percent for r in records if r.prediction_error_percent is not None]
    return {'schema_version':1,'created_at':datetime.now(timezone.utc).isoformat(),'profile':profile,'record_count':len(records),'calibrated_record_count':len(errors),'mean_absolute_error_percent':sum(abs(x) for x in errors)/len(errors) if errors else None,'records':[r.to_dict() for r in records],'warning':'Analytical estimates only; measured values must come from target hardware.'}
def write_benchmark_report(report,path):
    p=Path(path); p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(report,indent=2),encoding='utf-8'); return p
