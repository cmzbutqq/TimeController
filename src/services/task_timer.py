"""_summary_
    任务计时器
"""
from datetime import datetime,timedelta
from collections import namedtuple
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

if __name__ == '__main__':
    t=TaskTimer(1)
    cdt=TaskTimer(2,countdown_time=timedelta(seconds=5))
    breakpoint()