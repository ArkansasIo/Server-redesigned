from .inventory import Rack
from .interconnect import Interconnect
from .power import PowerThermalModel
from .scheduler import Scheduler
from .workloads import create_workload
class SimulationEngine:
    def __init__(self,cfg):
        self.config=cfg; self.rack=Rack(cfg); self.fabric=Interconnect(self.rack.interconnect_tbps); self.power=PowerThermalModel(cfg); self.scheduler=Scheduler(self.rack,self.fabric,cfg); self.time_seconds=0.; self.history=[]
    def submit(self,kind='matrix',operations_tflop=None,memory_gib=None,gpu_count=None,precision='fp16',workload_id='job-001'):
        job=create_workload(kind,operations_tflop,memory_gib,int(gpu_count or self.config['scheduler'].get('default_parallel_gpus',8)),precision,workload_id); return self.scheduler.submit(job)
    def tick(self,dt=1.):
        if dt<=0: raise ValueError('tick duration must be positive')
        self.scheduler.tick(dt); p=self.power.update(self.rack,dt); self.time_seconds+=dt
        m={'time_seconds':self.time_seconds,'gpu_count':len(self.rack.gpus),'gpu_utilization_avg':sum(g.utilization for g in self.rack.gpus)/len(self.rack.gpus),'gpus_active':sum(g.utilization>.1 for g in self.rack.gpus),'active_gpu_ids':[g.id for g in self.rack.gpus if g.utilization>.1],'queued_jobs':len(self.scheduler.queue),'active_jobs':len(self.scheduler.active),'completed_jobs':len(self.scheduler.completed),'interconnect':self.fabric.snapshot(),'power':p}; self.history.append(m); return m
    def run(self,seconds,tick_seconds=1.):
        if seconds<=0 or tick_seconds<=0: raise ValueError('seconds and tick_seconds must be positive')
        remaining=float(seconds); latest={}
        while remaining>1e-9: dt=min(float(tick_seconds),remaining); latest=self.tick(dt); remaining-=dt
        return {'inventory':self.rack.inventory(),'simulation_seconds':self.time_seconds,'metrics':latest,'jobs':{'queued':[j.to_dict() for j in self.scheduler.queue],'active':[j.to_dict() for j in self.scheduler.active],'completed':[j.to_dict() for j in self.scheduler.completed]},'history':self.history,'assumptions':['Logical software simulation only.','Performance and infrastructure figures are simplified estimates.']}
