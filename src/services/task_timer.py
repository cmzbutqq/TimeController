"""_summary_
    任务计时器
"""
from utils.helper import *
from config import *

TimerStatus = namedtuple('TimerStatus',('task_id','countdown','start','end','running','used_time')) # used_time指有效时间 暂停时不算

class TaskTimer:
    def __init__(self,task_id:int,countdown_time:Optional[timedelta]=None):
        self.task_id = task_id # 任务id
        self.countdown = countdown_time  # 倒计时设定时间,None表示正计时
        self.start = datetime.now() # 任务开始时间
        self.run = True   # 任务是暂停还是运行
        self.end = None  # 任务结束时间,None表示未结束
        self._last = [datetime.now(),timedelta(0)] # 上次暂停/恢复时的 时间和已用时间
    
    def resume(self)->None:
        if self.end is not None:
            return
        if self.run:
            return
        self.run = True
        self._last[0] = datetime.now()
    
    def pause(self)->None:
        if self.end is not None:
            return
        if not self.run:
            return
        self.run = False
        self._last[1] += datetime.now() - self._last[0]
        self._last[0] = datetime.now()
    
    def stop(self)->None:
        if self.end is not None:
            return
        self.pause()
        self.end = datetime.now()
        
    @property
    def _used(self)->timedelta: # 理论已用时间，不会改变计时器状态
        return self._last[1] + datetime.now() - self._last[0] if self.run else self._last[1]
    
    @property
    def status(self)->TimerStatus: # 更新并获取状态
        if (self.end is None) and (self.countdown is not None) and (self._used > self.countdown): # 未结束+倒计时+超时
            self.stop() # 自动结束
        return TimerStatus(self.task_id,self.countdown,self.start,self.end,self.run,self._used)
    
    def __repr__(self)->str:
        status=self.status # 注意这里会update
        return f'任务id:{status.task_id} 倒计时:{status.countdown}\n开始时间:{status.start} 结束时间:{status.end}\n是否运行:{status.running} 已用时间:{status.used_time}'

# if __name__ == '__main__':
#     t=TaskTimer(1)
#     cdt=TaskTimer(2,countdown_time=timedelta(seconds=5))
#     breakpoint()
    
    
    
"""_summary_
    TODO 重写任务记录表交互
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