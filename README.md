Windows 上的时间管理软件。目前有命令行交互界面，GUI 正在锐意制作中

# 如何运行:

环境: vscode , Python 3.11.4

1. 安装依赖
   - 命令行输入：pip install -r requirements.txt
2. 运行 cli.py 即可
   - 命令行输入：python src/cli.py

# 界面组成：

- header：当前界面名字
- body：当前界面内容
- footer：当前界面操作提示

## menu：主界面

- 键盘按下对应的数字以转到对应界面

1. track timers 追踪当前活跃的计时器
2. show cfg 显示配置信息
3. show instances 显示当前活跃的计时器和锁机器的实例
4. add task 添加任务/习惯/待办
5. remove task 根据 id 删除任务/习惯/待办
6. add locker 添加锁机规则
7. remove locker 根据索引删除锁机规则
8. start timer 通过输入的习惯 id 启动计时器

## track_timers：追踪当前活跃的计时器的界面

- 标题："RUNNING TIMERS"
- 键盘按下对应的按键以进行相应操作
  - q: main menu 停止所有计时器返回主界面
  - p: pause all 暂停所有计时器
  - e: stop all 停止所有计时器，这会将倒计时的内容记录到 data/record.xlsx 中并删除计时器
  - r: resume all 恢复所有计时器

## show_cfg：显示配置信息的界面

- 标题："CONFIGURATION"
- 键盘按下 q 返回主界面
- 显示配置文件中的内容
  - 所有任务/习惯/待办的相关信息
  - 所有锁机规则的相关信息

## show_insts：显示计时器和锁机器的实例的界面

- 标题："INSTANCES"
- 键盘按下 q 返回主界面

## add_task：添加任务/习惯/待办的界面

- 根据指示在命令行输入相关信息

## add_locker：添加锁机规则的界面

- 根据指示在命令行输入相关信息

## remove_task：删除任务/习惯/待办的界面

- 根据指示在命令行输入相关信息 通过 task_id 删除

## remove_locker：删除锁机规则的界面

- 根据指示在命令行输入相关信息 通过 index 删除

## start_timer：启动计时器的界面

- 根据指示在命令行输入相关信息 通过 task_id 启动
- 需要设置计时时间（0 为正计时，其他值为以分钟为单位的倒计时）

# 文件目录解释

- src
  - services 这个文件夹下是所有服务的实现，外部可以将他作为包导入 (import services)
    - utils
      - helper.py
      - sysutils.py
    - config.py 实现 json 配置文件的读写，通过 config 全局对象访问与修改用户配置
    - task.py 任务计时器与记录器的实现，通过 TaskTimer.run_thread()开始追踪计时器
    - locker.py 锁机规则与锁机器的实现，通过 self.start()开始锁机
  - cli.py 命令行交互界面
- data
  - record.xlsx 记录所有计时记录的 xlsx 文件，记录在 taskRecords 工作表中
- config
  - user.json 用户配置文件，通过 config.py 实现读写

# user.json 解释

- lockers：锁机规则列表
  - name: 规则名称
  - on: 规则是否启用（false 为禁用）
  - punish: 触发规则（违反进程表的规定）后的惩罚措施
  - list_type: 进程表是白名单还是黑名单
  - list: 进程表
  - timerules：启动锁机器的时间规则
    - 有 start_time,end_time,days 三个属性，分别表示开始时间，结束时间，以及每周哪些天启动
- count_tasks: 计次任务列表
  - id : 程序分配的任务 id
  - name: 任务名称
  - note: 任务备注
  - activate: 任务是否显示（false 为隐藏
  - daily_aim: 每日目标
  - weekly_aim: 每周目标
  - monthly_aim: 每月目标
  - deadline_aim: ddl 目标 含 date（截止日期）aim（目标）两个属性
- timer_tasks: 计时任务列表
  - 与 count_task 相比，多了 timers 属性，用于预设计时器长度（0 为正计时，其他值为以分钟为单位的倒计时）
- presets: 预设列表
  - 用户可以添加列表时填入预设，处理时会自动将预设展开
- settings: 用户设置
