# 調價_單一費率有上限
import pandas as pd
import numpy as np

# 載入 CSV 檔案
file_path = 'USPACE/三寶大樓.csv'  # 寫入路徑
parking_df = pd.read_csv(file_path)

# 把資料轉成時間格式
parking_df['order_start_time'] = pd.to_datetime(parking_df['order_start_time'])
parking_df['order_end_time'] = pd.to_datetime(parking_df['order_end_time'])

# 制定不同區段的費率和當日上限
parking_name = '三寶大樓一'
new_rates = {
    'hourly_rate': 60,  # 針對平假日的單一費率
    'daily_cap': 320    # 新當日上限
}

# 計算營收的函數
def calculate_revenue(row, rates):
    start_time = row['order_start_time']
    end_time = row['order_end_time']
    duration_minutes = (end_time - start_time).total_seconds() / 60
    
    # 10 分鐘內免費
    if duration_minutes < 10:
        return 0
    
    
    duration_hours = duration_minutes // 60
    remaining_minutes = duration_minutes % 60
    
    # 不滿半小時算半小時、不滿一小時算一小時
    if 0 < remaining_minutes <= 30:
        duration_hours += 0.5
    elif remaining_minutes > 30:
        duration_hours += 1
    
    # 新的訂單營收，分為有碰到當日上限以及沒有的
    revenue = min(duration_hours * rates['hourly_rate'], rates['daily_cap'])
    return revenue

# 建立新的資料欄位 new_revenue 存放新的金額
parking_df['new_revenue'] = parking_df.apply(calculate_revenue, axis=1, rates=new_rates)

# 計算總營收
new_total_revenue = parking_df['new_revenue'].sum()
old_total_revenue = parking_df['payment_amount'].sum()  # 原本 csv 裡的訂單金額

# 計算變動金額和比例
revenue_change = new_total_revenue - old_total_revenue
revenue_change_percentage = (revenue_change / old_total_revenue) * 100

# 顯示結果
print(parking_name)
print("舊營收總額:", old_total_revenue/3)
print("新營收總額:", new_total_revenue/3)
print("營收變動金額:", revenue_change/3)
print("營收變動比例: {:.2f}%".format(revenue_change_percentage/3))
