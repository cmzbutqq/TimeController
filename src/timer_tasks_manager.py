from services import TaskTimer, TaskRecorder, TimerStatus
from services import config
from typing import Dict, List, Optional
import json
from datetime import timedelta
import openpyxl
from openpyxl import Workbook
from openpyxl.utils import get_column_letter
import datetime


class TimerTasksManager:
    def __init__(self, app):
        self.timers: Dict[int, TimerStatus] = {}
        self.load_timers()
        self.app = app

    def load_timers(self):
        """从配置文件加载计时器任务实例"""
        timer_tasks = config.get("timer_tasks")()
        for task in timer_tasks:
            task_id = task["id"]
            countdown_time = (
                timedelta(seconds=task["timers"][1])
                if len(task["timers"]) > 1
                else None
            )
            # 初始化时任务未开始，所以start和end都为None
            self.timers[task_id] = TimerStatus(
                task_id,
                countdown_time,
                None,
                None,
                False,
                timedelta(0),
            )

    def get_timer(self, task_id: int) -> Optional[TimerStatus]:
        """根据任务ID获取计时器实例"""
        return self.timers.get(task_id)

    def create_timer(
        self, task_id: int, countdown_time: Optional[timedelta] = None
    ):
        """创建新的计时器实例"""
        if task_id in self.timers:
            raise ValueError(f"Task ID {task_id} already exists.")
        self.timers[task_id] = TimerStatus(
            task_id, countdown_time, None, None, False, timedelta(0)
        )

    def update_timer(
        self, task_id: int, countdown_time: Optional[timedelta] = None
    ):
        """更新现有计时器实例"""
        if task_id not in self.timers:
            raise ValueError(f"Task ID {task_id} does not exist.")
        self.timers[task_id] = TimerStatus(
            task_id, countdown_time, None, None, False, timedelta(0)
        )

    def delete_timer(self, task_id: int):
        """删除计时器实例"""
        if task_id not in self.timers:
            raise ValueError(f"Task ID {task_id} does not exist.")
        del self.timers[task_id]

    def start_timer(self, task_id: int):
        """开始计时器实例"""
        if task_id not in self.timers:
            # 如果任务 ID 不存在，创建一个新的计时器任务
            self.timers[task_id] = TimerStatus(
                task_id=task_id,
                countdown=None,
                start=None,
                end=None,
                running=False,
                used_time=timedelta(0),
            )
        timer = self.timers[task_id]
        if timer.running:
            # 如果计时器已经在运行，不需要重新启动
            return
        # 更新计时器状态为运行中，并设置开始时间
        self.timers[task_id] = timer._replace(
            start=datetime.datetime.now(), running=True
        )
        self.app.update_timer_label(task_id)

    def pause_timer(self, task_id: int):
        """暂停计时器实例"""
        if task_id not in self.timers:
            raise ValueError(f"Task ID {task_id} does not exist.")
        timer = self.timers[task_id]
        if not timer.running:
            raise RuntimeError(f"Timer ID {task_id} is not running.")
        # 计算已经使用的时间，并更新计时器状态为暂停
        self.timers[task_id] = timer._replace(
            running=False,
            used_time=timer.used_time
            + (datetime.datetime.now() - timer.start),
        )

    def get_elapsed_time(self, task_id: int) -> timedelta:
        """获取给定任务 ID 的当前计时时间"""
        if task_id not in self.timers:
            raise ValueError(f"Task ID {task_id} does not exist.")
        timer = self.timers[task_id]
        if timer.running:
            elapsed_time = timer.used_time + (
                datetime.datetime.now() - timer.start
            )
        else:
            elapsed_time = timer.used_time
        return elapsed_time

    def stop_timer(self, task_id: int, note: str = ""):
        """停止计时器实例并保存记录"""
        if task_id not in self.timers:
            raise ValueError(f"Task ID {task_id} does not exist.")
        timer = self.timers[task_id]
        if not timer.running:
            # 如果计时器未在运行，不需要停止
            return
        # 计算最终使用的时间，并更新计时器状态为停止
        used_time = self.get_elapsed_time(task_id)
        timer = timer._replace(
            end=datetime.datetime.now(),
            running=False,
            used_time=used_time,
        )
        # 使用 TaskRecorder 保存记录
        self.save_timer_record(timer, note)
        # 从计时器列表中移除
        del self.timers[task_id]

    def save_timer_record(
        self, timer_status: TimerStatus, note: str = ""
    ):
        """使用 TaskRecorder 保存计时器任务记录"""
        # 创建 TaskRecord 实例并保存
        task_record = TaskRecorder.timer_record(timer_status, note)
        TaskRecorder.add_records(TaskRecorder.rec_split(task_record))

    def get_total_recorded_time(self, task_id: int) -> timedelta:
        """获取给定任务 ID 的所有记录时间的总和"""
        total_time = timedelta(0)
        for record in TaskRecorder.get_all_records():
            if record.task_id == task_id:
                total_time += record.valid_time
        return total_time


# 示例使用
if __name__ == "__main__":
    manager = TimerTasksManager()
    # 假设任务ID为1的任务有一个30分钟的倒计时
    manager.create_timer(1, timedelta(minutes=30))
    # 开始任务
    manager.start_timer(1)
    # 暂停任务
    manager.pause_timer(1)
    # 停止任务并保存记录
    manager.stop_timer(1, note="Completed")
