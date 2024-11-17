from services import *

from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.panel import Panel
from rich.theme import Theme
from rich.live import Live
from rich.progress import BarColumn, Progress, SpinnerColumn, TextColumn
from rich.spinner import Spinner
from rich.traceback import install
from rich import print,inspect
from rich import box
import keyboard
install()
console=Console()

stage_command=None # 主线程根据这个变量决定是否切换显示界面
keybd_command=None # 现在需要处理的键盘信号
locks:list[Locker]=[Locker(idx) for idx in config.keys("lockers")]
def on_key_press(event):
    global keybd_command 
    keybd_command=event.name
keyboard.on_press(on_key_press)

def get_name(task_id:int)->str:
    for task in config.get("count_tasks")():
        if task["id"]==task_id:
            return task["name"]
    for task in config.get("timer_tasks")():
        if task["id"]==task_id:
            return task["name"]
    return "Unknown"

def make_layout(title:str,instructs:str)->Layout:
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="body", ratio=1),
        Layout(name="footer", size=5),
    )
    header=Panel(Text(title,justify="center"),border_style="cyan")
    layout["header"].update(header)
    footer=Panel(Text(instructs,justify="center"),border_style="cyan")
    layout["footer"].update(footer)
    return layout

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
        table.add_row(lock["name"], str(lock["on"]), lock["punish"], lock["list_type"], str(list2str(lock["list"])), rule_str)
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
    
    global keybd_command,stage_command
    keybd_command,stage_command=None,None
    
    layout = make_layout("CONFIGURATIONS","q: menu")

    body=Table.grid()
    body.add_row(Panel(cfg_tasks()))
    body.add_row(Panel(cfg_locks()))
    body.add_row(Panel(cfg_presets()))
    layout["body"].update(body)
    
    with Live(layout, refresh_per_second=10,screen=True) as live:
        while keybd_command not in ["q"]:
            pass
    keybd_command,stage_command=None,"menu"

def show_insts():
    global keybd_command,stage_command
    keybd_command,stage_command=None,None
    
    layout = make_layout("INSTANCES","q: menu")
    
    body=Table.grid()
    body.add_row(Panel(active_timers()))
    body.add_row(Panel(active_lockers()))
    layout["body"].update(body)
    
    with Live(layout, refresh_per_second=10,screen=True) as live:
        while keybd_command not in ["q"]:
            pass
    keybd_command,stage_command=None,"menu"

def remove_task():
    global keybd_command,stage_command
    stage_command=None
    
    _=input("press enter to continue:")
    
    task_id=input("task id (input q to cancel) : ")
    
    if task_id.isdigit():
        task_id=int(task_id)
        counters:list=config.get("count_tasks")()
        for task in counters:
            if task["id"]==task_id:
                counters.remove(task)
                break
        timers:list=config.get("timer_tasks")()
        for task in timers:
            if task["id"]==task_id:
                timers.remove(task)
                break
        config.save()
    
    keybd_command,stage_command=None,"show_cfg"

def remove_locker():
    global keybd_command,stage_command
    stage_command=None
    
    _=input("press enter to continue:")
    
    idx=input("locker index (input q to cancel) (start from 0): ")
    
    if idx.isdigit():
        global locks
        idx=int(idx)
        lockers:list=config.get("lockers")()
        if idx<len(lockers):
            lockers.pop(idx)
            locks[idx].stop()
        config.save()
    keybd_command,stage_command=None,"show_cfg"

def add_locker():
    global keybd_command,stage_command
    stage_command=None
    
    _=input("press enter to continue:")
    
    name = input("locker name: ")
    
    on = input("turned on (y/n): ")
    on = True if on.lower() == "y" else False
    
    punish=input(
        '''
        punish mode:
        1.DEBUG
        2.MINIMIZE
        3.CLOSE
        '''
    )
    match punish:
        case "1":
            punish="DEBUG"
        case "2":
            punish="MINIMIZE"
        case "3":
            punish="CLOSE"
        case _:
            punish="DEBUG"
            
    list_type=input("blacklist or whitelist?(b/w): ")
    list_type="WHITELIST" if list_type.lower()=="w" else "BLACKLIST"

    list_content=input("list content (separate by comma): ")
    list_content=list_content.split(',')
    list_content=[x.strip() for x in list_content]
    
    time_rules=[]
    while True:
        start_time=input("start time (HH:MM:SS) (input q to stop): ")
        if start_time.lower()=="q":
            break
        end_time=input("end time (HH:MM:SS): ")
        days=input("active days (separate by comma):")
        days=days.split(',')
        days=[day.strip() for day in days]
        time_rules.append({
            "start_time":start_time,
            "end_time":end_time,
            "days":days
        })
    config.get("lockers")().append({
        "name":name,
        "on":on,
        "punish":punish,
        "list_type":list_type,
        "list":list_content,
        "time_rules":time_rules
    })
    config.save()
    
    keybd_command,stage_command=None,"show_cfg"
    
def add_task():
    global keybd_command,stage_command
    stage_command=None

    _=input("press enter to continue:")

    id=0
    for task in config.get("count_tasks")():
        if task["id"]>id:
            id=task["id"]
    for task in config.get("timer_tasks")():
        if task["id"]>id:
            id=task["id"]
    id+=1
    
    tp=input("timer or counter? (t/c): ")
    tp="timer"if tp.lower()=="t" else "count"
    
    name=input("name: ")
    note=input("description: ")
    activate=True
    
    if tp =="timer":
        timers=input("timer presets(in minutes,0 means countup,seperate by comma): ")
        timers=timers.split(',')
        timers=[int(x.strip()) for x in timers]
    
    unit= "times" if tp=="count" else "minutes"
    daily_aim=input(f"daily {unit} aim (n for no aim): ")
    daily_aim=None if daily_aim.lower()=="n" else int(daily_aim)
    
    weekly_aim=input(f"weekly {unit} aim (n for no aim): ")
    weekly_aim=None if weekly_aim.lower()=="n" else int(weekly_aim)

    monthly_aim=input(f"monthly {unit} aim (n for no aim): ")
    monthly_aim=None if monthly_aim.lower()=="n" else int(monthly_aim)
    
    deadline_aim=input(f"deadline {unit} aim (n for no aim)(fmt: YYYY-MM-DD , your aim): ")
    if deadline_aim.lower()=="n":
        deadline_aim=None
    else:
        deadline_aim=deadline_aim.split(',')
        deadline_aim=[x.strip() for x in deadline_aim]
        date=deadline_aim[0]
        aim=int(deadline_aim[1])
        deadline_aim={
            "date":date,
            "aim":aim
        }
    
    if tp=="count":
        config.get(tp+"_tasks")().append({
            "id":id,
            "name":name,
            "note":note,
            "activate":activate,
            "daily_aim":daily_aim,
            "weekly_aim":weekly_aim,
            "monthly_aim":monthly_aim,
            "deadline_aim":deadline_aim
        })
    else:
        config.get(tp+"_tasks")().append({
            "id":id,
            "name":name,
            "note":note,
            "activate":activate,
            "timers":timers,
            "daily_aim":daily_aim,
            "weekly_aim":weekly_aim,
            "monthly_aim":monthly_aim,
            "deadline_aim":deadline_aim,
        })
    config.save()
    
    keybd_command,stage_command=None,"show_cfg"

def start_timer():
    global keybd_command,stage_command
    stage_command=None
    
    _=input("press enter to continue:")

    id=int(input("task id: "))
    
    for task in config.get("count_tasks")():
        if task["id"]==id:
            note=input('any note? : ')
            TaskRecorder.add_record(TaskRecorder.counter_record(id,datetime.now(),note))
            name=task["name"]
            
            print(f"Count Task {name} recorded")
            sleep(1)
            
            keybd_command,stage_command=None,"menu"
            return
    for task in config.get("timer_tasks")():
        if task["id"]==id:
            timers=task['timers']
            print("timer presets:"+list2str(timers))
            time=input("choose length:")
            time=int(time.strip())
            time=None if time==0 else timedelta(minutes=time)
            TaskTimer(id,time)

            print("timer started")
            sleep(1)

            keybd_command,stage_command=None,"menu"
            return
        
    print("Unknown Task")
    sleep(1)
    
    keybd_command,stage_command=None,"menu"
    
def track_timers():
    global keybd_command,stage_command
    stage_command=None
    
    TaskTimer.run_thread()
    layout=make_layout("RUNNING TIMERS","q: main menu\tp:pause all\te:stop all\tr:resume all\t")
    
    with Live(layout,refresh_per_second=10,screen=True) as live:
        
        while keybd_command not in ["q"]:
            match keybd_command:
                case "p":
                    keybd_command=None
                    for timer in TaskTimer.instances:
                        timer.pause()
                    continue
                case "e":
                    keybd_command=None
                    for timer in TaskTimer.instances:
                        timer.stop()
                    continue
                case "r":
                    keybd_command=None
                    for timer in TaskTimer.instances:
                        timer.resume()
                    continue
            body=Table.grid()
            for timer in TaskTimer.instances:
                status:TimerStatus=timer.status
                name=get_name(status.task_id)
                # if status.end is not None:
                #     continue
                grid=Table.grid()
                if status.countdown is None:
                    used=TaskRecorder.floor_dur(status.used_time)
                    speed=1 if status.running else 0
                    running = Spinner("dots",speed=speed)
                    grid.add_row(
                        Text(name+' '),
                        running,
                        Text(' '+str(used)),
                        )
                else:
                    cd=status.countdown
                    used=TaskRecorder.floor_dur(status.used_time)
                    speed=1 if status.running else 0
                    running = Spinner("dots",speed=speed)
                    percentage=round(status.used_time/status.countdown*100,1)
                    grid.add_row(
                        Text(name+' '),
                        running,
                        Text(f" {used}/{cd} - {percentage}%"),
                    )
                
                body.add_row(Panel(grid,border_style="cyan"))
            layout["body"].update(body)
            
    TaskTimer.stop_thread()
    keybd_command,stage_command=None,"menu"



    

def menu():
    global keybd_command,stage_command
    keybd_command,stage_command=None,None
    
    layout=make_layout("MENU","q: quit")

    body=Panel(Text("""
                    1:track timers
                    2:show cfg
                    3:show instances
                    4:add task
                    5.remove task
                    6:add locker
                    7.remove locker
                    8.start timer"""
                    ,justify="left",style="bold"),border_style="cyan")
    layout["body"].update(body)
    with Live(layout, refresh_per_second=10,screen=True) as live:
        while True:
            match keybd_command:
                case "1":
                    keybd_command,stage_command=None,"track_timers"
                    return
                case "2":
                    keybd_command,stage_command=None,"show_cfg"
                    return
                case "3":
                    keybd_command,stage_command=None,"show_insts"
                    return
                case "4":
                    keybd_command,stage_command=None,"add_task"
                    return
                case "5":
                    keybd_command,stage_command=None,"remove_task"
                    return
                case "6":
                    keybd_command,stage_command=None,"add_locker"
                    return
                case "7":
                    keybd_command,stage_command=None,"remove_locker"
                    return
                case "8":
                    keybd_command,stage_command=None,"start_timer"
                    return
                case "q":
                    keybd_command,stage_command=None,"quit"
                    return

TaskTimer(3)
TaskTimer(4,timedelta(seconds=2))
TaskTimer(5,timedelta(seconds=5))
TaskTimer(6,timedelta(seconds=10))

stage_command="menu"

while stage_command!="quit":
    match stage_command:
        case "track_timers":
            track_timers()
        case "show_cfg":
            show_cfg()
        case "show_insts":
            show_insts()
        case "menu":
            menu()
        case "remove_task":
            remove_task()
        case "remove_locker":
            remove_locker()
        case "add_locker":
            add_locker()
        case "add_task":
            add_task()
        case "start_timer":
            start_timer()
        case None:
            continue
        case _:
            print(f"unknown command:{stage_command}")
    console.clear()