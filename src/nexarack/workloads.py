from .models import Workload
PRESETS={'matrix':(1000.,8.,.02),'llm-inference':(250.,48.,.10),'distributed-training':(5000.,64.,.25),'memory-bandwidth':(100.,100.,.02)}
def create_workload(kind,operations_tflop=None,memory_gib=None,gpu_count=8,precision='fp16',workload_id='job-001'):
    if kind not in PRESETS: raise ValueError(f'Unknown workload {kind!r}; options: {", ".join(PRESETS)}')
    ops,mem,comm=PRESETS[kind]; ops=float(ops if operations_tflop is None else operations_tflop); mem=float(mem if memory_gib is None else memory_gib)
    if ops<=0 or mem<0 or int(gpu_count)<1: raise ValueError('operations_tflop and gpu_count must be positive; memory_gib cannot be negative')
    if precision not in ('fp8','fp16'): raise ValueError('precision must be fp8 or fp16')
    return Workload(workload_id,kind,ops,mem,int(gpu_count),precision,comm)
def estimate_runtime(job,gpus,fabric,efficiency=.35,memory_efficiency=.7,calibration=1.0,contention=1.0,dispatch_ms=.2):
    if not gpus: raise ValueError('At least one GPU is required')
    if job.kind=='memory-bandwidth': duration=job.memory_gib/max(sum(g.memory_bandwidth_tbps*1e12/(1024**3) for g in gpus)*memory_efficiency,1e-9)
    else:
        peak=sum(g.fp8_tflops if job.precision=='fp8' else g.fp16_tflops for g in gpus)
        compute=job.operations_tflop/max(peak*efficiency,1e-9); memory=job.memory_gib/max(sum(g.memory_bandwidth_tbps*1e12/(1024**3) for g in gpus)*memory_efficiency,1e-9); duration=max(compute,memory)
    comm=fabric.transfer_seconds(job.memory_gib*1024**3*job.communication_fraction,contention)
    return max(.001,(duration+comm+dispatch_ms/1000)*calibration)
