from services import *

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.panel import Panel
from rich.theme import Theme
from rich.live import Live
from rich.progress import track
from rich.traceback import install
from rich import print,inspect
from rich import box
install()
console=Console()

def list2str(lst:list)->str:
    return ', '.join(map(str,lst))

def cfg_tasks()->Table:
    table = Table(title="Task List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["id", "name", "note", "avail", "daily", "weekly", "monthly", "deadline","type"]:
        table.add_column(col,overflow="fold")
    for task in config.get("count_tasks")():
        ddl=task["deadline_aim"]
        ddl=f"{ddl['aim']} times until: {ddl['date']}" if ddl is not None else "None"
        table.add_row(str(task["id"]), task["name"], task["note"], str(task["activate"]), str(task["daily_aim"]), str(task["weekly_aim"]), str(task["monthly_aim"]),ddl,'counter')
    for task in config.get("timer_tasks")():
        ddl=task["deadline_aim"]
        ddl=f"{ddl['aim']} mins until: {ddl['date']}" if ddl is not None else "None"
        table.add_row(str(task["id"]), task["name"], task["note"], str(task["activate"]), str(task["daily_aim"]), str(task["weekly_aim"]), str(task["monthly_aim"]),ddl,'timer')
    return table

def cfg_locks()->Table:
    table = Table(title="Lock List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["name", "on", "punish", "list_type", "list", "time_rules"]:
        table.add_column(col)
    for lock in config.get("lockers")():
        rule_str = ''
        for rule in lock["time_rules"]:
            rule_str += f"{rule['start_time']} - {rule['end_time']} | { list2str(rule['days'])}\n"
        table.add_row(lock["name"], str(lock["on"]), lock["punish"], lock["list_type"], str(*lock["list"]), rule_str)
    return table

def cfg_presets()->Table:
    table = Table(title="Preset List",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["key", "value"]:
        table.add_column(col)
    for k in config.keys("presets"):
        table.add_row(k, list2str(config.get("presets",k)()))
    return table

def active_timers()->Table:
    table = Table(title="Timer Instances",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    
    for col in ["task id","countdown", "start", "end", "running", "used time"]:
        table.add_column(col)
    for timer in TaskTimer.instances:
        status:TimerStatus = timer.status
        cd:str= 'count up' if status.countdown is None else str(status.countdown)
        table.add_row(str(status.task_id), cd, str(status.start), str(status.end), str(status.running), str(status.used_time))
    return table

def active_lockers()->Table:
    table= Table(title="Locker Instances",expand=True,box=box.SIMPLE,border_style = "bright_yellow")
    for col in ["status","thread"]:
        table.add_column(col)
    for lockers in Locker.instances:
        table.add_row(lockers.status, str(lockers.thread))
    return table

def show_cfg():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("CONFIGURATIONS",justify="center"),border_style="cyan")
    body=Table.grid()
    body.add_row(Panel(cfg_tasks()))
    body.add_row(Panel(cfg_locks()))
    body.add_row(Panel(cfg_presets()))
    layout["header"].update(header)
    layout["body"].update(body)
    print(layout)

def show_insts():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("INSTANCES",justify="center"),border_style="cyan")
    body=Table.grid()
    body.add_row(Panel(active_timers()))
    body.add_row(Panel(active_lockers()))
    layout["header"].update(header)
    layout["body"].update(body)
    print(layout)

def demo_timer():
    TaskTimer(0)
    TaskTimer(1,timedelta(seconds=2))
    TaskTimer(2,timedelta(seconds=5))
    
    print(active_timers())
    TaskTimer.run_thread()
    for _ in range(5):
        sleep(2)
        print(active_timers())
    TaskTimer.stop_thread()
    print(active_timers())
    
    TaskTimer.run_thread()
    for _ in range(2):
        sleep(1)
        print(active_timers())
    TaskTimer.stop_thread()
    print(active_timers())

locks:list[Locker]=[Locker(idx) for idx in config.keys("lockers")] 

def demo_locker():
    print(active_lockers())
    for lock in locks:lock.start()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.start()
    sleep(1)
    print(active_lockers())
    for lock in locks:lock.stop() # 不要用 del 因为 del 能用不大可能
    sleep(1)
    print(active_lockers())

def track_timers():
    TaskTimer.run_thread()

TaskTimer(1)

def track_timers():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
    )
    header=Panel(Text("RUNNING TIMERS",justify="center"),border_style="cyan")
    layout["header"].update(header)
    
    body=Table.grid()
    body.add_row(Panel(active_timers()))
    body.add_row(Panel(active_lockers()))
    layout["body"].update(body)
    print(layout)



show_cfg()
show_insts()








