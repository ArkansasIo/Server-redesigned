from pathlib import Path
from fastapi import FastAPI,HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel,Field
from .config import load_config
from .engine import SimulationEngine
from .timeline import WorkloadTimeline
app=FastAPI(title='NexaRack API',version='0.4.0'); engine=SimulationEngine(load_config()); timeline=WorkloadTimeline()
class WorkloadRequest(BaseModel):
 kind:str='matrix'; operations_tflop:float|None=Field(default=None,gt=0); memory_gib:float|None=Field(default=None,ge=0); gpu_count:int=Field(default=8,ge=1,le=72); precision:str='fp16'
@app.get('/')
def dashboard():
 p=Path(__file__).resolve().parents[2]/'dashboard'/'index.html'
 if not p.exists(): return HTMLResponse('<h1>NexaRack dashboard not found</h1>',status_code=500)
 return HTMLResponse(p.read_text(encoding='utf-8'))
@app.get('/health')
def health(): return {'status':'ok','simulation_only':True,'version':'0.4.0'}
@app.get('/inventory')
def inventory(): return engine.rack.inventory()
@app.get('/metrics')
def metrics(): return engine.history[-1] if engine.history else {'time_seconds':0,'gpu_count':len(engine.rack.gpus),'gpu_utilization_avg':0,'gpus_active':0,'active_gpu_ids':[],'queued_jobs':0,'active_jobs':0,'completed_jobs':0,'power':{'rack_power_w':sum(g.power_w for g in engine.rack.gpus)+sum(c.power_w for c in engine.rack.cpus),'rack_power_limit_w':engine.config['rack']['power_limit_w'],'rack_temperature_c':engine.config['rack'].get('ambient_c',22),'energy_kwh':0}}
@app.get('/workloads')
def workloads(): return {'jobs':[j.to_dict() for j in engine.scheduler.queue+engine.scheduler.active+engine.scheduler.completed]}
@app.get('/timeline')
def events(): return {'events':timeline.snapshot()}
@app.get('/history')
def history(limit:int=100):
 if not 1<=limit<=5000: raise HTTPException(status_code=400,detail='limit must be between 1 and 5000')
 return {'history':engine.history[-limit:]}
@app.post('/workloads')
def submit(req:WorkloadRequest):
 try:
  job=engine.submit(req.kind,req.operations_tflop,req.memory_gib,req.gpu_count,req.precision); timeline.record('queued',job,engine.time_seconds); return job.to_dict()
 except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
@app.post('/tick')
def tick(seconds:float=1.):
 if not 0<seconds<=3600: raise HTTPException(status_code=400,detail='seconds must be > 0 and <= 3600')
 try:
  m=engine.tick(seconds)
  for job in engine.scheduler.active+engine.scheduler.completed: timeline.record(job.status,job,engine.time_seconds)
  return m
 except ValueError as exc: raise HTTPException(status_code=400,detail=str(exc)) from exc
@app.post('/reset')
def reset():
 global engine,timeline; engine=SimulationEngine(load_config()); timeline=WorkloadTimeline(); return {'status':'reset'}
