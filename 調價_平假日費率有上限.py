import pandas as pd
import numpy as np

# 載入 CSV 檔案
file_path = 'USPACE/行政院.csv'
parking_df = pd.read_csv(file_path)

# 把資料轉成時間格式
parking_df['order_start_time'] = pd.to_datetime(parking_df['order_start_time'])
parking_df['order_end_time'] = pd.to_datetime(parking_df['order_end_time'])

# 以分計算停放時間
parking_df['duration_minutes'] = (parking_df['order_end_time'] - parking_df['order_start_time']).dt.total_seconds() / 60

# 假日定義（星期五、星期六、星期日）
parking_df['is_weekend'] = parking_df['order_start_time'].dt.dayofweek.isin([5, 6])

# 制定平日和假日的費率與當日上限
parking_name = '行政院鄰近車位'
new_rates = {
    'weekday_hourly_rate': 50,  # 平日每小時費率
    'weekend_hourly_rate': 50,  # 假日每小時費率
    'old_weekday_limit': 280,   # 舊平日每日上限
    'new_weekday_limit': 300,   # 新平日每日上限
    'old_weekend_limit': 280,   # 舊假日每日上限
    'new_weekend_limit': 300    # 新假日每日上限
}

# 計算營收的函數
def calculate_revenue(row, rates, limit_key):
    start_time = row['order_start_time']
    end_time = row['order_end_time']
    duration_minutes = (end_time - start_time).total_seconds() / 60

    # 10 分鐘內免費
    if duration_minutes < 10:
        return 0

    # 計算停車時間（以小時計算）
    duration_hours = duration_minutes // 60
    remaining_minutes = duration_minutes % 60

    # 不滿半小時算半小時、不滿一小時算一小時
    if 0 < remaining_minutes <= 30:
        duration_hours += 0.5
    elif remaining_minutes > 30:
        duration_hours += 1

    # 確定費率和每日上限
    if row['is_weekend']:
        hourly_rate = rates['weekend_hourly_rate']
        daily_limit = rates[limit_key.replace('daily_limit', 'weekend_limit')]
    else:
        hourly_rate = rates['weekday_hourly_rate']
        daily_limit = rates[limit_key.replace('daily_limit', 'weekday_limit')]

    # 計算總金額，應用每日上限
    revenue = min(duration_hours * hourly_rate, daily_limit)
    return revenue

# 計算新舊營收
parking_df['new_revenue'] = parking_df.apply(calculate_revenue, axis=1, rates=new_rates, limit_key='new_daily_limit')
parking_df['old_revenue'] = parking_df.apply(calculate_revenue, axis=1, rates=new_rates, limit_key='old_daily_limit')

# 總營收計算
new_total_revenue = parking_df['new_revenue'].sum()
old_total_revenue = parking_df['payment_amount'].sum()  # 原本 CSV 的訂單金額

# 營收變動
revenue_change = new_total_revenue - old_total_revenue
revenue_change_percentage = (revenue_change / old_total_revenue) * 100

# 平均每月營收
months = 1  # 假設 9 個月的數據
old_avg_revenue = old_total_revenue / months
new_avg_revenue = new_total_revenue / months
avg_revenue_change = revenue_change / months

# 顯示結果
print(parking_name)
print("舊營收平均每月總額:", old_avg_revenue)
print("新營收平均每月總額:", new_avg_revenue)
print("營收變動金額平均每月:", avg_revenue_change)
print("營收變動比例: {:.2f}%".format(revenue_change_percentage))
