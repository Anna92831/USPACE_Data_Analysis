import pandas as pd
from datetime import datetime, timedelta

# 載入 CSV 檔案
file_path = "USPACE/國家企業中心.csv"  # 請填寫正確路徑
parking_df = pd.read_csv(file_path)

# 把資料轉成時間格式
parking_df['order_start_time'] = pd.to_datetime(parking_df['order_start_time'])
parking_df['order_end_time'] = pd.to_datetime(parking_df['order_end_time'])

# 制定不同區段的費率和當日上限
new_rates = {
    "night": 10,               # 夜間每小時費率 (00:00 - 07:59 和 22:00 - 23:59)
    "weekday_day": 50,         # 平日白天每小時費率 (08:00 - 21:59)
    "weekend_day": 60,         # 假日白天每小時費率 (08:00 - 21:59)
    "daily_limit": 280         # 新的每日上限
}

# 判斷是否是假日
def is_holiday(date):
    return date.weekday() >= 5  # 星期六 (5) 和星期日 (6)

# 計算每日收入
def calculate_daily_revenue(current_time, end_time, rates):
    total_revenue = 0
    daily_revenue = 0
    current_day = current_time.date()

    while current_time < end_time:
        hour = current_time.hour
        if 0 <= hour <= 7 or 22 <= hour <= 23:  # 夜間
            rate = rates["night"]
        elif 8 <= hour <= 21:  # 白天
            if is_holiday(current_time):  # 假日白天
                rate = rates["weekend_day"]
            else:  # 平日白天
                rate = rates["weekday_day"]
        else:
            rate = 0

        # 累計單日收入
        daily_revenue += rate

        # 如果跨日，結算當日收入
        next_hour = current_time + timedelta(hours=1)
        if next_hour.date() != current_day:
            # 單日收入不超過每日上限
            total_revenue += min(daily_revenue, rates["daily_limit"])
            daily_revenue = 0  # 重置單日收入
            current_day = next_hour.date()

        current_time = next_hour

    # 最後一天的收入
    total_revenue += min(daily_revenue, rates["daily_limit"])
    return total_revenue

# 計算新營收
def calculate_new_revenue(row):
    return calculate_daily_revenue(row['order_start_time'], row['order_end_time'], new_rates)

# 使用 CSV 中的 `payment_amount` 作為舊營收
parking_df['old_revenue'] = parking_df['payment_amount']
parking_df['new_revenue'] = parking_df.apply(calculate_new_revenue, axis=1)

# 總營收
old_total_revenue = parking_df['old_revenue'].sum()  # 使用 `payment_amount` 加總
new_total_revenue = parking_df['new_revenue'].sum()

# 營收變動
revenue_change = new_total_revenue - old_total_revenue
revenue_change_percentage = (revenue_change / old_total_revenue) * 100

# 顯示結果
print("舊營收總額 (每週):", old_total_revenue / 7)
print("新營收總額 (每週):", new_total_revenue / 7)
print("營收變動金額 (每週):", revenue_change / 7)
print("營收變動比例 (每週): {:.2f}%".format(revenue_change_percentage / 7))
