from dataclasses import dataclass, asdict, field

@dataclass(slots=True)
class GPU:
    id:int; tray_id:int; memory_gib:float; memory_bandwidth_tbps:float; fp16_tflops:float; fp8_tflops:float; max_power_w:float; idle_power_w:float
    utilization:float=0.0; memory_used_gib:float=0.0; power_w:float=0.0
    @property
    def memory_free_gib(self): return max(0.0, self.memory_gib-self.memory_used_gib)

@dataclass(slots=True)
class CPU:
    id:int; cores:int; memory_gib:float; max_power_w:float; idle_power_w:float; utilization:float=0.0; power_w:float=0.0

@dataclass(slots=True)
class Workload:
    id:str; kind:str; operations_tflop:float; memory_gib:float; gpu_count:int; precision:str="fp16"; communication_fraction:float=.05; status:str="queued"; progress:float=0.0; elapsed_seconds:float=0.0; assigned_gpu_ids:list[int]=field(default_factory=list); estimated_total_seconds:float|None=None; result:dict=field(default_factory=dict)
    def to_dict(self): return asdict(self)
