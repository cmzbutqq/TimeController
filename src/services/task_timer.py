"""_summary_
    TODO 任务计时器
"""
import datetime as tm
from config import *



@singleton
class TaskTimer:
    __slot__ = ('task_id','countdown_time','start_time','valid_time')
    def __init__(self, task_id:int, countdown_time:Optional[int]):
        self.task_id:int                    = task_id
        self.countdown_time:Optional[int]   = countdown_time
        self.start_time:tm.datetime         = tm.datetime.now()
        self.valid_time:tm.timedelta        = tm.timedelta()
        
        
if __name__ == '__main__':
    breakpoint()