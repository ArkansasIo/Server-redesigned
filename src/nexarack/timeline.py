from datetime import datetime,timezone
class WorkloadTimeline:
    def __init__(self): self.events=[]
    def record(self,event,job=None,at_seconds=0.,details=None):
        e={'sequence':len(self.events)+1,'timestamp_utc':datetime.now(timezone.utc).isoformat(),'simulation_seconds':float(at_seconds),'event':event,'job_id':getattr(job,'id',None),'workload':getattr(job,'kind',None),'status':getattr(job,'status',None),'gpu_ids':list(getattr(job,'assigned_gpu_ids',[])),'details':details or {}}; self.events.append(e); return e
    def snapshot(self): return list(self.events)
