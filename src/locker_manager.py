from threading import Thread, Event
from services import Locker  # 假设 Locker 类在 lockers.py 文件中
from services import config  # 导入配置单例


# 全局变量，用于存储所有锁的实例
lockers = []

"""
def load_locks_from_config():
    global lockers
    lockers=[]
    lockers = [Locker(idx) for idx in config.keys("lockers")]
    for locker in lockers:
        if locker.on:
            locker.start()
"""


def load_locks_from_config():
    """
    停止所有正在运行的 Locker 实例，清理线程资源，
    然后重新从配置文件加载 Locker 实例并启动。
    """
    global lockers

    # 停止所有正在运行的 Locker 实例
    if lockers:
        for locker in lockers:
            locker.stop()
        for locker in lockers:
            if locker.thread.is_alive():
                locker.thread.join()
        print(
            "[green]All existing lockers stopped and joined.[/green]"
        )

    # 清空全局变量
    lockers = []

    # 重新加载 Locker 实例并启动
    lockers = [Locker(idx) for idx in config.keys("lockers")]
    for locker in lockers:
        if locker.on:
            locker.start()
            print(
                f"[blue]Locker {locker.name} started successfully.[/blue]"
            )


def create_and_start_lockers():
    global lockers
    lockers = [Locker(idx) for idx in config.keys("lockers")]
    for locker in lockers:
        if locker.on:
            locker.start()


def stop_and_join_lockers():
    global lockers
    for locker in lockers:
        locker.stop()
    for locker in lockers:
        if locker.thread.is_alive():
            locker.thread.join()


if __name__ == "__main__":
    create_and_start_lockers()
