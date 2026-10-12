from .models import GPU, CPU

class Rack:
    def __init__(self,cfg):
        top,gc,cc=cfg['topology'],cfg['gpu'],cfg['cpu']; self.name=cfg['system']['name']; self.trays=int(top['trays']); self.gpus_per_tray=int(top['gpus_per_tray']); self.interconnect_tbps=float(top['interconnect_aggregate_tbps'])
        self.gpus=[GPU(i,i//self.gpus_per_tray,float(gc['memory_gib']),float(gc['memory_bandwidth_tbps']),float(gc['fp16_tflops']),float(gc['fp8_tflops']),float(gc['max_power_w']),float(gc.get('idle_power_w',0)),power_w=float(gc.get('idle_power_w',0))) for i in range(self.trays*self.gpus_per_tray)]
        self.cpus=[CPU(i,int(cc['cores_per_instance']),float(cc['memory_gib_per_instance']),float(cc['max_power_w']),float(cc.get('idle_power_w',0)),power_w=float(cc.get('idle_power_w',0))) for i in range(int(top['cpus']))]
    def inventory(self):
        mem=sum(g.memory_gib for g in self.gpus)
        return {'name':self.name,'trays':self.trays,'gpus_per_tray':self.gpus_per_tray,'gpu_count':len(self.gpus),'cpu_count':len(self.cpus),'gpu_memory_total_gib':mem,'gpu_memory_total_tib':mem/1024,'cpu_memory_total_gib':sum(c.memory_gib for c in self.cpus),'interconnect_aggregate_tbps':self.interconnect_tbps,'simulation_only':True}
