from .workloads import estimate_runtime
class Scheduler:
    def __init__(self,rack,fabric,cfg):
        self.rack,self.fabric=rack,fabric; self.cfg=cfg; self.queue=[]; self.active=[]; self.completed=[]; self.counter=1
    def submit(self,job):
        if job.gpu_count>len(self.rack.gpus): raise ValueError('Requested GPU count exceeds rack inventory')
        if job.memory_gib>job.gpu_count*self.rack.gpus[0].memory_gib: raise ValueError('Requested workload memory exceeds assigned GPU capacity')
        if any(x.id==job.id for x in self.queue+self.active+self.completed): job.id=f'job-{self.counter:05d}'
        self.counter+=1; self.queue.append(job); return job
    def dispatch(self):
        while self.queue:
            job=self.queue[0]; used={gid for x in self.active for gid in x.assigned_gpu_ids}; free=[g for g in self.rack.gpus if g.id not in used]
            if len(free)<job.gpu_count: break
            selected=free[:job.gpu_count]; per=job.memory_gib/len(selected)
            if any(g.memory_free_gib+1e-9<per for g in selected): job.status='blocked-memory'; break
            self.queue.pop(0); job.assigned_gpu_ids=[g.id for g in selected]
            for g in selected: g.memory_used_gib+=per; g.utilization=.85
            job.status='running'; active_count=max(1,len(self.active)+1); bench=self.cfg.get('benchmark',{})
            job.estimated_total_seconds=estimate_runtime(job,selected,self.fabric,float(self.cfg['scheduler'].get('compute_efficiency',.35)),float(self.cfg['scheduler'].get('memory_efficiency',.7)),float(bench.get('calibration_factor_'+job.precision,1)),max(float(self.cfg['scheduler'].get('interconnect_contention_floor',.15)),1/active_count),float(self.cfg['scheduler'].get('dispatch_overhead_ms',.2)))
            self.active.append(job)
    def tick(self,dt):
        self.dispatch()
        for job in list(self.active):
            job.elapsed_seconds+=dt; job.progress=min(1.,job.elapsed_seconds/max(job.estimated_total_seconds or .001,.001))
            if job.progress>=1:
                job.status='completed'; job.result={'elapsed_seconds':job.elapsed_seconds,'estimated_total_seconds':job.estimated_total_seconds,'operations_tflop':job.operations_tflop,'effective_tflops':job.operations_tflop/max(job.elapsed_seconds,1e-9)}
                for gid in job.assigned_gpu_ids: g=self.rack.gpus[gid]; g.memory_used_gib=max(0,g.memory_used_gib-job.memory_gib/len(job.assigned_gpu_ids)); g.utilization=.05
                self.active.remove(job); self.completed.append(job)
        self.dispatch()
