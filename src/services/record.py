"""_summary_
    TODO 任务记录表交互
"""
import csv
from task_timer import *

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
            writer.writerow([input.task_id,input.start,input.end,input.used_time,note])

    @classmethod
    def add_counter_rec(cls,task_id:int,time:datetime=None,note:str=None)->None:
        if note is None:
            note = ''
        if time is None:
            time = datetime.now()
        with open(cls.file_path,'a',newline='')as f:
            writer = csv.writer(f)
            writer.writerow([task_id,time,time,None,note])
    
    @classmethod
    def query(cls,task_id:int=None,start_range:tuple[datetime]=None,end_range:tuple[datetime]=None)->list[TaskRecord]:
        with open(cls.file_path,'r',newline='')as f:
            reader = csv.reader(f)
            records = [TaskRecord(*row) for row in reader]
        if task_id is not None:
            records = [record for record in records if int(record.task_id)==int(task_id)]
        if start_range is not None:
            records= [record for record in records if datetime(record.start)>=start_range[0] and datetime(record.start)<=start_range[1]]
        if end_range is not None:
            records= [record for record in records if datetime(record.end)>=end_range[0] and datetime(record.end)<=end_range[1]]
        return records
    @classmethod
    def delete(cls,task_id:int,start:datetime,end:datetime)->Optional[TaskRecord]:
        pass
        

if __name__ == '__main__':
    TaskRecorder.add_timer_rec(TimerStatus(1,timedelta(10.24423),datetime.now(),datetime.now()+timedelta(10.872789),False,timedelta(seconds=10e5)),note='test')
    
    
    breakpoint()