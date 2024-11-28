import tkinter as tk
from tkinter import ttk
from win32ctypes.pywin32.pywintypes import datetime
import gui_setting
import locker_manager
import threading
from file_watcher import FileWatcher
from services import config
from tkinter import messagebox
from timer_tasks_manager import TimerTasksManager
from services import TaskRecorder
from count_tasks_manager import CountTasksManager

import user_json_path

class ModernApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TODO")
        self.root.geometry("900x600")
        self.root.configure(bg="#1e1e1e")  # 背景色：深灰

        # 初始化 TimerTasksManager 并传递当前 ModernApp 实例
        self.timer_tasks_manager = TimerTasksManager(app=self)

        # 创建 CountTasksManager 的实例
        self.count_tasks_manager = CountTasksManager()
        # 启动文件监视器来监控用户配置文件
        self.file_watcher = FileWatcher(user_json_path.user_json_path, self.on_file_change)
        # 在后台线程中运行文件监视器
        threading.Thread(target=self.file_watcher.watch, daemon=True).start()

        # 配置样式
        self.style = ttk.Style()
        self.style.configure("Sidebar.TFrame", background="#252526")  # 按钮栏深灰色
        self.style.configure("Content.TFrame", background="#1e1e1e")  # 内容区深灰色
        self.style.configure(
            "AppTitle.TLabel",
            font=("Arial", 18, "bold"),
            foreground="#d4d4d4",  # 浅灰色文字
            background="#252526",
        )
        self.style.configure(
            "SidebarButton.TButton",
            font=("Arial", 12),
            padding=10,
            background="#b0b0b0",  # 按钮中灰色
            foreground="#000000",  # 黑色文字
            borderwidth=0,
        )
        self.style.map(
            "SidebarButton.TButton",
            background=[("active", "#c0c0c0")],  # 悬停时更浅灰色
            foreground=[("active", "#000000")],  # 悬停时黑色文字
        )

        # 主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # 左侧按钮栏
        self.sidebar = ttk.Frame(self.main_frame, style="Sidebar.TFrame", width=200)
        self.sidebar.pack(side=tk.LEFT, fill=tk.Y)

        # 右侧动态内容区
        self.content = ttk.Frame(self.main_frame, style="Content.TFrame")
        self.content.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 添加按钮栏
        self.add_sidebar()

        # 初始化并启动Locker
        locker_manager.create_and_start_lockers()
        self.show_locker()

        # 当窗口关闭时，调用self.on_closing
        root.protocol("WM_DELETE_WINDOW", self.on_closing)


    def on_file_change(self):
        # 文件变动时，重新加载config
        old_timer_tasks = config.get('timer_tasks')()
        old_count_tasks = config.get('count_tasks')()
        config.load(user_json_path.user_json_path)
        new_timer_tasks = config.get('timer_tasks')()
        new_count_tasks = config.get('count_tasks')()

        # 查找被删除的timer_tasks
        deleted_timer_tasks = [task for task in old_timer_tasks if task not in new_timer_tasks]

        # 对于每个被删除的timer_task，删除其记录
        for task in deleted_timer_tasks:
            excel_file_path = 'data/timer_tasks_record.xlsx'
            TaskRecorder.delete_task_records_from_excel(task['id'], excel_file_path)

        # 查找并处理被删除的 count_tasks
        deleted_count_tasks = [task for task in old_count_tasks if task not in new_count_tasks]
        for task in deleted_count_tasks:
            self.count_tasks_manager.delete_task_records(task['id'])

        # 更新Locker配置
        locker_manager.load_locks_from_config()
        self.show_locker()


    def add_sidebar(self):
        # App名称
        title_label = ttk.Label(self.sidebar, text="TODO", style="AppTitle.TLabel", anchor="center")
        title_label.pack(fill=tk.X, pady=20)

        # 按钮列表
        buttons = [
            ("🔒 Locker", self.show_locker),
            ("⏱️ Timer Tasks", self.show_timer_tasks),
            ("📊 Count Tasks", self.show_count_tasks),
            ("⚙️ Setting", self.show_setting),
        ]

        for text, command in buttons:
            button = ttk.Button(
                self.sidebar,
                text=text,
                command=command,
                style="SidebarButton.TButton",
            )
            button.pack(fill=tk.X, padx=15, pady=10)

    def clear_content(self):
        """清空内容区"""
        for widget in self.content.winfo_children():
            widget.destroy()

    def show_locker(self):
        self.clear_content()
        label = ttk.Label(
            self.content, text="🔒 Locker", font=("Arial", 16), foreground="#ffffff", background="#1e1e1e"
        )
        label.pack(pady=50)

        for locker in locker_manager.lockers:
            # 创建状态字符串和颜色
            status_str = "On" if locker.on else "Off"
            status_color = "#4caf50" if locker.on else "#f44336"  # 绿色/红色

            # 外框（卡片）
            card = tk.Frame(
                self.content,
                bg="#252526",
                padx=10,
                pady=10,
                highlightbackground="#3c3c3c",  # 卡片边框颜色
                highlightthickness=1,  # 卡片边框厚度
            )
            card.pack(fill="x", padx=20, pady=10)  # 填充x方向，并设置外边距

            # Locker 名称
            name_label = tk.Label(
                card,
                text=locker.name,
                font=("Arial", 14, "bold"),
                fg="#d4d4d4",  # 浅灰色文字
                bg="#252526",  # 与卡片背景色一致
            )
            name_label.pack(side="left", padx=10)

            # 状态标签
            status_label = tk.Label(
                card,
                text=status_str,
                font=("Arial", 12, "bold"),
                fg="#ffffff",  # 白色文字
                bg=status_color,  # 根据状态动态变化颜色
                padx=10,
                pady=5,
            )
            status_label.pack(side="right", padx=10)

    def show_timer_tasks(self):
        self.clear_content()
        label = ttk.Label(
            self.content, text="⏱️ Timer Tasks", font=("Arial", 16), foreground="#ffffff", background="#1e1e1e"
        )
        label.pack(pady=50)

        # 创建控制按钮框架
        self.control_frame = ttk.Frame(self.content)
        self.control_frame.pack(pady=20)

        # 在控制按钮框架中添加计时标签
        self.timer_label = ttk.Label(self.control_frame, text="Time: 00:00:00", font=("Arial", 14))
        self.timer_label.grid(row=7, column=0, padx=10, pady=10)

        # 创建下拉菜单来选择计时器任务
        self.timer_tasks_combobox = ttk.Combobox(self.content, values=self.get_timer_task_names())
        self.timer_tasks_combobox.pack(pady=20)

        # 创建一个按钮来加载选中的任务
        load_task_button = ttk.Button(self.content, text="Load Task", command=self.load_selected_timer_task)
        load_task_button.pack(pady=20)

        # 创建控制按钮框架
        self.control_frame = ttk.Frame(self.content)
        self.control_frame.pack(pady=20)

    def get_timer_task_names(self):
        """获取所有计时器任务的名字"""
        timer_tasks = config.get('timer_tasks')()
        return [task['name'] for task in timer_tasks]

    def load_selected_timer_task(self):
        """加载用户选择的计时器任务"""
        task_name = self.timer_tasks_combobox.get()
        timer_task = next((task for task in config.get('timer_tasks')() if task['name'] == task_name), None)
        if timer_task:
            if messagebox.askokcancel("Load Task", f"Do you want to load the task '{task_name}'?"):
                self.show_timer_task_info(timer_task)

    def show_timer_task_info(self, timer_task):
        """显示计时器任务的信息和控制按钮"""
        # 清除控制按钮框架中的内容
        for widget in self.control_frame.winfo_children():
            widget.destroy()

        # 显示任务信息
        task_id = timer_task['id']
        task_name = timer_task['name']
        task_note = timer_task['note']
        task_id_label = ttk.Label(self.control_frame, text=f"ID: {task_id}")
        task_id_label.grid(row=0, column=0, padx=10, pady=10)
        task_name_label = ttk.Label(self.control_frame, text=f"Name: {task_name}")
        task_name_label.grid(row=1, column=0, padx=10, pady=10)
        task_note_label = ttk.Label(self.control_frame, text=f"Note: {task_note}")
        task_note_label.grid(row=2, column=0, padx=10, pady=10)

        # 显示任务目标
        daily_aim_label = ttk.Label(self.control_frame, text=f"Daily Aim: {timer_task['daily_aim']}")
        daily_aim_label.grid(row=3, column=0, padx=10, pady=10)
        weekly_aim_label = ttk.Label(self.control_frame, text=f"Weekly Aim: {timer_task['weekly_aim']}")
        weekly_aim_label.grid(row=4, column=0, padx=10, pady=10)
        monthly_aim_label = ttk.Label(self.control_frame, text=f"Monthly Aim: {timer_task['monthly_aim']}")
        monthly_aim_label.grid(row=5, column=0, padx=10, pady=10)

        # 获取并显示已记录时间
        total_recorded_time = self.timer_tasks_manager.get_total_recorded_time(task_id)
        total_time_label = ttk.Label(self.control_frame, text=f"Total Recorded Time: {total_recorded_time}")
        total_time_label.grid(row=6, column=0, padx=10, pady=10)

        # 创建控制按钮
        start_button = ttk.Button(self.control_frame, text="Start",
                                  command=lambda: self.timer_tasks_manager.start_timer(task_id))
        start_button.grid(row=0, column=1, padx=10, pady=10)
        pause_button = ttk.Button(self.control_frame, text="Pause",
                                  command=lambda: self.timer_tasks_manager.pause_timer(task_id))
        pause_button.grid(row=1, column=1, padx=10, pady=10)
        stop_button = ttk.Button(self.control_frame, text="Stop",
                                 command=lambda: self.stop_timer_with_record(task_id))
        stop_button.grid(row=2, column=1, padx=10, pady=10)

        # 本次计时的 elapsed time 标签
        self.elapsed_time_var = tk.StringVar()
        self.elapsed_time_var.set("Elapsed Time: 00:00:00")
        elapsed_time_label = ttk.Label(self.control_frame, textvariable=self.elapsed_time_var)
        elapsed_time_label.grid(row=7, column=0, padx=10, pady=10)

        # 更新 elapsed time 标签的函数
        def update_elapsed_time():
            timer = self.timer_tasks_manager.get_timer(task_id)
            if timer and timer.running:
                elapsed_time = timer.used_time + (datetime.now() - timer.start)
                self.elapsed_time_var.set(f"Elapsed Time: {str(elapsed_time).split('.')[0]}")
                self.root.after(1000, update_elapsed_time)
            else:
                # 计时器已停止或暂停，显示已记录的总时间
                self.elapsed_time_var.set(f"Total Recorded Time: {total_recorded_time}")

        # 如果计时器已经在运行，开始更新 elapsed time 标签
        timer = self.timer_tasks_manager.get_timer(task_id)
        if timer and timer.running:
            update_elapsed_time()

    def stop_timer_with_record(self, task_id):
        """停止计时器任务并保存记录"""
        self.timer_tasks_manager.stop_timer(task_id, note="Task completed manually")
        self.show_timer_tasks()  # 刷新任务列表以清除任务信息

    def update_timer_label(self, task_id):
        """更新计时标签以显示经过的时间"""
        if task_id in self.timer_tasks_manager.timers and self.timer_tasks_manager.timers[task_id].running:
            elapsed_time = datetime.now() - self.timer_tasks_manager.timers[task_id].start
            self.timer_label.config(text=f"Time: {str(elapsed_time).split('.')[0]}")  # 显示小时、分钟和秒
            # 每秒更新一次
            self.root.after(1000, lambda: self.update_timer_label(task_id))
        else:
            # 计时器已停止，显示总有效时间
            total_time = self.timer_tasks_manager.get_total_recorded_time(task_id)
            self.timer_label.config(text=f"Total Time: {str(total_time).split('.')[0]}")

    def show_count_tasks(self):
        self.clear_content()
        label = ttk.Label(
            self.content, text="📊 Count Tasks", font=("Arial", 16), foreground="#ffffff", background="#1e1e1e"
        )
        label.pack(pady=50)
        # 创建 CountTasksManager 实例
        self.count_tasks_manager = CountTasksManager()

        # 创建任务按钮
        for task in self.count_tasks_manager.tasks:
            btn_text = f"ID: {task['id']} - {task['name']}\n计划: {task['weekly_aim']}次/周\n已完成: {task.get('completion_count', 0)}次\n备注: {task.get('note', '')}"
            task_button = ttk.Button(
                self.content,
                text=btn_text,
                command=lambda task_id=task['id']: self.on_task_button_click(task_id),
                width=50,  # 设置按钮宽度
                padding=(10, 5)  # 设置按钮内边距以增加大小
            )
            task_button.pack(pady=10)

    def on_task_button_click(self, task_id):
        # 处理任务按钮点击事件
        self.count_tasks_manager.increment_completion_count(task_id)
        self.show_count_tasks()  # 刷新界面以更新按钮文本

    def show_setting(self):
        gui_setting.setting()
        self.clear_content()
        label = ttk.Label(
            self.content, text="⚙️ Setting", font=("Arial", 16), foreground="#ffffff", background="#1e1e1e"
        )
        label.pack(pady=50)

    def on_closing(self):

        # 停止文件监视器
        self.file_watcher.stop()
        # 停止并等待所有Locker线程结束
        locker_manager.stop_and_join_lockers()
        # 销毁窗口
        self.root.quit()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = ModernApp(root)
    root.mainloop()