class PowerThermalModel:
    def __init__(self,cfg): self.cfg=cfg['rack']; self.energy_j=0.; self.peak_w=0.; self.temperature_c=float(self.cfg.get('ambient_c',22))
    def update(self,rack,dt):
        if dt<0: raise ValueError('dt cannot be negative')
        gp=sum(setattr(g,'power_w',g.idle_power_w+(g.max_power_w-g.idle_power_w)*g.utilization) or g.power_w for g in rack.gpus)
        cp=sum(setattr(c,'power_w',c.idle_power_w+(c.max_power_w-c.idle_power_w)*c.utilization) or c.power_w for c in rack.cpus)
        total=gp+cp; self.energy_j+=total*dt; self.peak_w=max(self.peak_w,total); target=float(self.cfg.get('ambient_c',22))+total/1000*float(self.cfg.get('thermal_resistance_c_per_kw',.12)); self.temperature_c+=(target-self.temperature_c)*min(1,dt/30)
        return {'gpu_power_w':gp,'cpu_power_w':cp,'rack_power_w':total,'rack_power_limit_w':float(self.cfg['power_limit_w']),'power_limit_exceeded':total>float(self.cfg['power_limit_w']),'cooling_capacity_w':float(self.cfg['cooling_capacity_w']),'cooling_capacity_exceeded':total>float(self.cfg['cooling_capacity_w']),'rack_temperature_c':self.temperature_c,'energy_kwh':self.energy_j/3600000,'peak_power_w':self.peak_w}
