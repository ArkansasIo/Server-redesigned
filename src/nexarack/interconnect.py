from dataclasses import dataclass

@dataclass(slots=True)
class Interconnect:
    aggregate_tbps:float; bytes_transferred:float=0.0; transfer_count:int=0
    def transfer_seconds(self,byte_count,utilization=1.0):
        if byte_count<0: raise ValueError('byte_count cannot be negative')
        fraction=min(1.0,max(.01,float(utilization))); self.bytes_transferred+=byte_count; self.transfer_count+=1
        return byte_count/(self.aggregate_tbps*1e12*fraction)
    def snapshot(self): return {'aggregate_bandwidth_tbps':self.aggregate_tbps,'bytes_transferred':self.bytes_transferred,'transfer_count':self.transfer_count}
