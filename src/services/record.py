"""_summary_
    TODO 任务记录表交互
"""
import csv
from task_timer import *

def dur_reg(duration:timedelta)->timedelta: # 去除天数和微秒数
    return timedelta(seconds=duration.seconds)
def dtm_reg(dt:datetime)->datetime:
    return dt.replace(microsecond=0)
dt_fmt = "%Y-%m-%d %H:%M:%S"
TaskRecord=namedtuple('TaskRecord',('task_id','start','end','valid_time','note'))
class TaskRecorder:
    file_path = 'data/task_rec.csv'
    
    @classmethod
    def add_timer_rec(cls,input:TimerStatus,note:str=None)->None:
        if note is None:
            note = ''
        if input.end is None or input.running:
            raise ValueError('Timer not ended yet')
        with open(cls.file_path,'a',newline='')as f:
            writer = csv.writer(f)
            writer.writerow([input.task_id,dtm_reg(input.start),dtm_reg(input.end),dur_reg(input.used_time),note])

    @classmethod
    def add_counter_rec(cls,task_id:int,time:datetime=None,note:str=None)->None:
        if note is None:
            note = ''
        if time is None:
            time = datetime.now()
        with open(cls.file_path,'a',newline='')as f:
            writer = csv.writer(f)
            writer.writerow([task_id,dtm_reg(time),dtm_reg(time),None,note])
    
    @classmethod
    def query(cls,task_id:int=None,start_range:tuple[datetime]=None,end_range:tuple[datetime]=None)->list[TaskRecord]:
        with open(cls.file_path,'r',newline='')as f:
            reader = csv.reader(f)
            records = [TaskRecord(*row) for row in reader]
        if task_id is not None:
            records = [record for record in records if int(record.task_id)==int(task_id)]
        if start_range is not None:
            records= [record for record in records if datetime.strptime(record.start,dt_fmt)>=start_range[0] and datetime.strptime(record.start,dt_fmt)<=start_range[1]]
        if end_range is not None:
            records= [record for record in records if datetime.strptime(record.end,dt_fmt)>=end_range[0] and datetime.strptime(record.end,dt_fmt)<=end_range[1]]
        return records
    @classmethod
    def delete(cls,task_id:int,start:datetime,end:datetime)->Optional[TaskRecord]:
        pass # TODO
        

if __name__ == '__main__':
    # import random
    # VARY = 1e5
    # while True:
    #     TaskRecorder.add_timer_rec(TimerStatus(1,timedelta(VARY*random.random()),datetime.now()-timedelta(VARY*random.random()),datetime.now()+timedelta(VARY*random.random()),False,timedelta(seconds=VARY*random.random())),note='test')
    #     TaskRecorder.add_counter_rec(10,datetime.now()+timedelta(random.uniform(-VARY,+VARY)))
    
    breakpoint()
    # TaskRecorder.query(task_id=1,start_range=(datetime.now()-timedelta(RNG),datetime.now()+timedelta(RNG)),end_range=(datetime.now()-timedelta(RNG),datetime.now()+timedelta(RNG)))