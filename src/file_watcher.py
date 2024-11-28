"""
这个文件用来监视user.json文件的变化，如果变化，就会重新加载config
"""

import time
import os
import threading


class FileWatcher:
    def __init__(self, filepath, callback, stop_event=None):
        self.filepath = filepath
        self.callback = callback
        self.last_modified = os.path.getmtime(filepath)
        self.stop_event = stop_event or threading.Event()

    def watch(self):
        while (
            not self.stop_event.is_set()
        ):  # 检查 stop_event 是否设置
            try:
                current_modified = os.path.getmtime(self.filepath)
                if current_modified != self.last_modified:
                    self.last_modified = current_modified
                    self.callback()  # 文件发生变化时触发回调
            except FileNotFoundError:
                pass  # 如果文件不存在，忽略
            time.sleep(1)

    def stop(self):
        """设置事件停止线程"""
        self.stop_event.set()
