"""_summary_
    任务计时器
"""
from utils.helper import *
from config import *
from openpyxl import Workbook,load_workbook

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


TaskRecord=namedtuple('TaskRecord',('task_id','start','end','valid_time','note'))
class TaskRecorder:
    @staticmethod
    def floor_dtm(time:datetime)->datetime: # 削去微秒
        return time.replace(microsecond=0)
    
    @staticmethod
    def floor_dur(time:timedelta)->timedelta: # 削去微秒
        return timedelta(seconds=time.total_seconds()//1)
    
    @staticmethod
    def timer_record(status:TimerStatus,note:str=None)->TaskRecord: # TimerStatus 2 TaskRecord
        assert status.running is False, 'Timer not paused'
        assert status.end is not None, 'Timer not ended'
        
        start=TaskRecorder.floor_dtm(status.start)
        end=TaskRecorder.floor_dtm(status.end)
        valid_time=TaskRecorder.floor_dur(status.used_time)
        return TaskRecord(status.task_id,start,end,valid_time,note)
    
    @staticmethod
    def counter_record(task_id:int,time:datetime,note:str=None)->TaskRecord:
        tm=TaskRecorder.floor_dtm(time)
        return TaskRecord(task_id,tm,tm,None,note)
    
    @staticmethod
    def rec_split(rec:TaskRecord)->list[TaskRecord]: # 如果TaskRecord跨天，则拆分成多个在同一天的记录
        if rec.valid_time is None: # 计次任务
            return [rec]
        if rec.start.date()==rec.end.date(): # 同一天
            return [rec]
        assert rec.start.date()<rec.end.date(), 'TaskRecord not cross day'
        # 跨天
        start:datetime=rec.start
        end:datetime=rec.end
        elapsed:timedelta = end - start
        
        left:datetime = start
        right:datetime = start.replace(hour=23,minute=59,second=59,microsecond=999999)
        ret=[]
        while True:
            # 添加元素
            weight:float = (right-left)/elapsed
            valid_time:timedelta = TaskRecorder.floor_dur(rec.valid_time*weight)
            record:TaskRecord = TaskRecord(rec.task_id,TaskRecorder.floor_dtm(left),TaskRecorder.floor_dtm(right),valid_time,rec.note)
            ret.append(record)
            # 更改 left right
            left:datetime = right.replace(hour=0,minute=0,second=0,microsecond=0) + timedelta(days=1)
            if left.date()>end.date():
                break
            if left.date()==end.date():
                right=end
            else:
                right=left.replace(hour=23,minute=59,second=59,microsecond=999999)
        return ret
    
    # TODO excel存入
    

if __name__ == '__main__':
    
    import random
    VARY = 1e6
    dur=timedelta(seconds=VARY*random.random())
    start=datetime.now()-0.7*dur
    end = datetime.now()+0.7*dur
    status=TimerStatus(1,2*dur,start,end,False,dur)
    record=TaskRecorder.timer_record(status)
    records=TaskRecorder.rec_split(record)
    print(records)

    breakpoint()