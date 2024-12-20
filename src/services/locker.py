"""_summary_
    锁机器
"""

from .config import config
from .utils.helper import Callable, weakref, time, datetime, Optional
from .utils.sysutils import user32, fore_window_info, sleep
from threading import (
    Thread,
    Event,
)  # 每个Locker一个线程 这个py文件相对主文件可以新开一个进程

__all__ = ("Locker", "peroid", "Thread", "Event")

peroid = tuple[time, time]
SW_MINIMIZE = 6
WM_CLOSE = 16


class Locker:
    _presets: Callable = config.get("presets")
    _active_int: Callable = config.get(
        "settings", "advanced", "lock_active_interval_sec"
    )
    _idle_int: Callable = config.get(
        "settings", "advanced", "lock_idle_interval_sec"
    )
    _off_int: Callable = config.get(
        "settings", "advanced", "lock_off_interval_sec"
    )

    instances: weakref.WeakSet = weakref.WeakSet()

    def __init__(
        self, index: int, stop_event: Optional[Event] = None
    ):
        self._lock: Callable = config.get("lockers", index)
        self.exit: Event = (
            Event() if stop_event is None else stop_event
        )  # 主线程通过此变量通知子线程退出
        self.thread: Thread = Thread(target=self._run)  # 子线程
        self.status: str = (  # 子线程记录自己的状态
            f"{self.lock['name']}: [bold red]THREAD NOT STARTED[/]"
        )
        Locker.instances.add(self)

    @property
    def lock(self) -> dict:
        return self._lock()

    @classmethod
    def presets_decode(cls, lst: list):  # generator
        presets: dict = cls._presets()
        for item in lst:
            if item in presets:
                for it in presets[item]:
                    yield it
            else:
                yield item

    @property
    def weekly_durs(
        self,
    ) -> (
        tuple
    ):  # 返回长为7的元组 idx为周几（周一0周日6） 每个元素为时间段列表
        tfmt1 = "%H:%M"
        tfmt2 = "%H:%M:%S"

        def str2tm(str: str) -> time:
            try:
                return datetime.strptime(str, tfmt2).time()
            except ValueError:
                return datetime.strptime(str, tfmt1).time()

        rules = self.lock["time_rules"]
        ret: tuple = ([], [], [], [], [], [], [])
        for rule in rules:
            days = Locker.presets_decode(rule["days"])  # generator
            start, end = str2tm(rule["start_time"]), str2tm(
                rule["end_time"]
            )
            overnight = start > end
            for day in days:  # day: 周一1周日7
                if overnight:  # 跨天则开始在当日 结束在下一天
                    ret[(day - 1) % 7].append(
                        (start, str2tm("23:59:59"))
                    )
                    ret[day % 7].append((str2tm("00:00:00"), end))
                else:
                    ret[(day - 1) % 7].append((start, end))
        return ret

    @property
    def proc_list(self) -> list:
        plist: list = self.lock["list"]
        return list(Locker.presets_decode(plist))

    @property
    def on(self) -> bool:
        return self.lock["on"]

    @property
    def name(self) -> str:
        return self.lock["name"]

    @property
    def list_type(self) -> str:
        return self.lock["list_type"]

    def punish(self, hwnd) -> None:
        if hwnd is None:
            return
        # 当别的Locker已经结束了违法的进程时，当前Locker的punish函数不应该再执行
        # (不是原子操作 会不会还有竞争？ hwnd指向的窗口已关闭时会出问题吗？)
        fname: str = self.lock["punish"]
        match fname:
            case "MINIMIZE":
                user32.ShowWindow(hwnd, SW_MINIMIZE)
            case "CLOSE":
                user32.PostMessageW(hwnd, WM_CLOSE, 0, 0)
            case "DEBUG":
                print(f"[yellow]{fore_window_info()}[/yellow]")
            case "LAG":
                pass  # TODO
            case _:
                raise ValueError(f"punish function {fname} not found")

    @property
    def _violate(
        self,
    ) -> Optional[int]:  # 当前进程是否违规 是则返回hwnd 否则None
        (hwnd, _, _, pname) = fore_window_info()
        # print (pname)
        match self.list_type:
            case "WHITELIST":
                return None if pname in self.proc_list else hwnd
            case "BLACKLIST":
                return hwnd if pname in self.proc_list else None
            case _:
                raise ValueError(
                    f"list_type {self.list_type} illegal"
                )

    @property
    def _active(self) -> bool:  # 当前时间是否在激活时间段 TODO testit
        weekday = datetime.now().weekday()  # 周一0周日6
        now = datetime.now().time()
        durs = self.weekly_durs[weekday]
        for start, end in durs:
            if now >= start and now <= end:
                return True
        return False

    def _run(self) -> None:  # 子线程使用这个方法
        while True:
            if self.exit.is_set():
                self.status = (
                    f"{self.lock['name']}: [bold red]EXIT[/bold red]"
                )
                return
            if self.on is False:
                self.status = f"{self.lock['name']}: [b]off[/b]"
                sleep(Locker._off_int())
                continue
            if self._active is False:
                self.status = (
                    f"{self.lock['name']}: [green]idle[/green]"
                )
                sleep(Locker._idle_int())
                continue
            if self._violate is None:
                self.status = (
                    f"{self.lock['name']}: [cyan]active[/cyan]"
                )
                sleep(Locker._active_int())
                continue
            self.punish(
                self._violate
            )  # 这里再传一次violate是因为别的Lockers可能已经punish了，为了避免竞争
            self.status = (
                f"{self.lock['name']}: [magenta]violate[/magenta]"
            )
            sleep(Locker._active_int())

    def start(self):  # 主线程使用这个方法
        self.thread.start()

    def stop(self):  # 主线程使用这个方法
        self.exit.set()
        if self.thread.is_alive():
            self.thread.join()
        self.exit.clear()  # 重置exit
        self.thread: Thread = Thread(target=self._run)  # 重置thread
        print("[reverse]thread joined[/]")  # 之后还能再次start


if __name__ == "__main__":
    locks: list[Locker] = [
        Locker(idx) for idx in config.keys("lockers")
    ]
    # exit=Event()
    # threads=[Thread(target=lock.run,args=(exit,)) for lock in locks]
    # [thread.start() for thread in threads]
    # sleep(10)
    # exit.set()
    # [thread.join() for thread in threads]
