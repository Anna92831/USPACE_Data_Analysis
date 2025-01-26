import pandas as pd

# 載入 CSV 檔案（範例路徑，請自行修改）
file_path = "USPACE/CSV/敦化車梯.csv"
parking_df = pd.read_csv(file_path)

# 把資料轉成時間格式
parking_df['order_start_time'] = pd.to_datetime(parking_df['order_start_time'])
parking_df['order_end_time'] = pd.to_datetime(parking_df['order_end_time'])

# 假日定義（星期六、星期日）
def is_holiday(date):
    return date.weekday() == 5 or date.weekday() == 6  # 僅星期六和星期日為假日 
    #return date.weekday() in [4, 5, 6]  #假日定義若是五、六、日請打開註解
    
# 費率設定（範例，根據需求調整）
rates = {
    "weekday_day_rate": 50, # 08:00-19:59 費率
    "weekend_day_rate": 60, # 08:00-19:59 費率
    "early_morning_rate": 10,  # 00:00-07:59 費率
    "night_rate": 8,           # 20:00-23:59 費率
    "weekday_day_limit": 280,  
    "weekend_day_limit": 290,
    "has_daily_limit": True  # 有每日上限
    #"has_daily_limit": False # 無上限場站，請打開註解
}

# 判斷時段類型
def get_rate_type(current_time):
    hour = current_time.hour
    if 0 <= hour < 8:
        return "early_morning_rate"
    elif 20 <= hour <= 23:
        return "night_rate"
    else:
        return "day_rate"

# 計算營收的函數
def calculate_revenue(row, rates):
    start_time = row['order_start_time']
    end_time = row['order_end_time']
    duration_minutes = (end_time - start_time).total_seconds() / 60

    # 免費停車規則（10 分鐘內免費）
    if duration_minutes <= 10:
        return 0

    # 計算停車時長（以小時計算）
    duration_hours = duration_minutes // 60
    remaining_minutes = duration_minutes % 60

    # 不滿半小時算半小時，不滿一小時算一小時
    if 0 < remaining_minutes <= 30:
        duration_hours += 0.5
    elif remaining_minutes > 30:
        duration_hours += 1

    # 確定費率與每日上限
    rate_type = get_rate_type(start_time)
    key = f"weekday_{rate_type}"

    # Check if the key exists in rates
    if key not in rates:
        print(f"Warning: '{key}' not found in rates. Available keys: {rates.keys()}")
        hourly_rate = 0  # Set a default value or handle the error as needed
    else:
        hourly_rate = rates[key]

    if is_holiday(start_time):
        daily_limit = rates['weekend_day_limit'] if rates['has_daily_limit'] else float('inf')
    else:
        daily_limit = rates['weekday_day_limit'] if rates['has_daily_limit'] else float('inf')

    # 計算總金額，應用每日上限
    revenue = min(duration_hours * hourly_rate, daily_limit)
    return revenue

# 計算新舊營收
parking_df['new_revenue'] = parking_df.apply(calculate_revenue, axis=1, rates=rates)
parking_df['old_revenue'] = parking_df['payment_amount']

# 總營收計算
new_total_revenue = parking_df['new_revenue'].sum()
old_total_revenue = parking_df['old_revenue'].sum()

# 計算資料時間範圍的月份數
time_range_months = max(parking_df['order_start_time'].dt.to_period('M').nunique(), 1)

# 若資料範圍超過 12 個月，計算為年份數
if time_range_months > 12:
    time_range_years = time_range_months // 12
    print("資料涵蓋年份數:", time_range_years)
    average_old_revenue = old_total_revenue / time_range_years
    average_new_revenue = new_total_revenue / time_range_years
    print("每年平均舊營收:", average_old_revenue)
    print("每年平均新營收:", average_new_revenue)
else:
    print("資料涵蓋月份數:", time_range_months)
    average_old_revenue = old_total_revenue / time_range_months
    average_new_revenue = new_total_revenue / time_range_months
    print("每月平均舊營收:", average_old_revenue)
    print("每月平均新營收:", average_new_revenue)

# 營收變動
revenue_change = new_total_revenue - old_total_revenue
revenue_change_percentage = (revenue_change / old_total_revenue) * 100

# 顯示結果
print("舊營收總額:", old_total_revenue)
print("新營收總額:", new_total_revenue)
print("營收變動金額:", revenue_change)
print("營收變動比例: {:.2f}%".format(revenue_change_percentage))
