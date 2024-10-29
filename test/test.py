from datetime import date
import holidays
import pandas as pd

# 创建中国的节假日对象
cn_holidays = holidays.China()

# 选择一个年份
year = 2023

# 获取该年份的所有中国法定节假日
for dt, name in sorted(cn_holidays.items()):
    print(dt, name)

# # 添加周末休息日
# from pandas.tseries.offsets import CustomBusinessDay

# # 定义一个工作日规则，排除周六和周日
# weekend = CustomBusinessDay(weekmask='Mon Tue Wed Thu Fri')

# # 从年初到年末的日期范围
# start_date = date(year, 1, 1)
# end_date = date(year, 12, 31)

# # 生成日期范围
# all_days = pd.date_range(start=start_date, end=end_date, freq=weekend)

# # 筛选出不是工作日的日期（即周末）
# weekend_days = [d for d in pd.date_range(start=start_date, end=end_date) if d not in all_days]

# # 打印周末休息日
# for day in weekend_days:
#     if day not in cn_holidays:
#         print(day, "周末休息日")
