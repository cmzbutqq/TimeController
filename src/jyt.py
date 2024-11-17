import openpyxl
import matplotlib.pyplot as plt
from datetime import datetime

# 读取Excel数据
def read_excel(file_path):
    # 加载工作簿
    wb = openpyxl.load_workbook(file_path)
    sheet = wb['taskRecords']  # 获取第一个工作表

    # 提取数据：假设从第二行开始，每行包括任务ID、日期、起始时间、结束时间
    tasks = []
    for row in sheet.iter_rows(min_row=2, values_only=True):
        task_id, date, start_time, end_time = row[0],row[1], row[2], row[3]
        tasks.append({
            "task_id": task_id,
            "date": datetime.strptime(str(date), '%Y-%m-%d').date(),
            "start_time": datetime.strptime(str(start_time), '%H:%M').time(),
            "end_time": datetime.strptime(str(end_time), '%H:%M').time(),
        })
    return tasks

# 转换时间为小时数
def time_to_hours(time):
    return time.hour + time.minute / 60.0

# 可视化任务进度
def plot_task_progress(tasks):
    fig, ax = plt.subplots(figsize=(10, 6))

    # 设置每个任务的进度条
    for task in tasks:
        start_datetime = datetime.combine(task['date'], task['start_time'])
        end_datetime = datetime.combine(task['date'], task['end_time'])
        # 计算开始和结束的小时数
        start_hour = time_to_hours(task['start_time'])
        end_hour = time_to_hours(task['end_time'])

        # 绘制每个任务的时间段
        ax.barh(task['task_id'], end_hour - start_hour, left=start_hour, color='skyblue')

    # 设置图表的格式
    ax.set_xlabel('时间（小时）')
    ax.set_ylabel('任务ID')
    ax.set_title('任务进度可视化')
    ax.set_xlim(0, 24)  # 假设任务的时间段从0到24小时
    plt.xticks(range(25))  # 显示每小时的刻度
    plt.tight_layout()
    plt.show()

# 主函数
def main():
    file_path = 'data/record_demo.xlsx'  # 请将文件路径替换为实际路径
    tasks = read_excel(file_path)
    plot_task_progress(tasks)

if __name__ == "__main__":
    main()