import pandas as pd
import csv
from datetime import datetime, timedelta

# 場站的基本資訊
building_name = "國家企業中心"
hour_price_daytime = 50  # 平日白天每小時費率
hour_price_night = 10  # 夜間每小時費率
hour_price_holiday = 60  # 假日白天每小時費率
holiday_night_price = 10  # 假日夜間每小時費率
daytime_reset_hours = 9
daytime_reset_price = 280  # 白天時段 9 小時重置費率
holiday_daily_limit = 280  # 假日每日上限
day_start_hour = 8
day_end_hour = 21

# 定義假日判斷
def is_holiday(date):
    """
    判斷是否是假日。假日定義為星期六 (5) 和星期日 (6)。
    """
    return date.weekday() in [5, 6]  # 星期六和星期日為假日

# 定義白天費率的計算
def calculate_daytime_fee(start_time, end_time, is_holiday_flag):
    """
    計算白天時段的停車費用，白天定義為 08:00-21:59。
    如果是平日則使用白天費率，假日則使用假日費率。
    """
    current_time = start_time
    total_daytime_hours = 0

    while current_time < end_time:
        if day_start_hour <= current_time.hour <= day_end_hour:
            total_daytime_hours += 1
        current_time += timedelta(hours=1)

    if total_daytime_hours == 0:
        return 0  # 沒有白天時段
    elif is_holiday_flag:  # 假日費率計算
        return min(total_daytime_hours * hour_price_holiday, holiday_daily_limit)
    elif total_daytime_hours <= daytime_reset_hours:  # 平日白天費率計算
        return total_daytime_hours * hour_price_daytime
    else:
        return daytime_reset_price

# 定義全天費率的計算（包含白天和夜間費率）
def calculate_parking_fee(start_time, end_time):
    """
    計算整個停車的費用，包括白天費率、夜間費率和假日費率。
    """
    duration_minutes = (end_time - start_time).total_seconds() / 60
    if duration_minutes < 10:  # 10 分鐘內免費
        return 0

    total_fee = 0
    current_time = start_time
    is_holiday_flag = is_holiday(start_time)

    while current_time < end_time:
        if day_start_hour <= current_time.hour <= day_end_hour:  # 白天時段
            fee = calculate_daytime_fee(current_time, end_time, is_holiday_flag)
            total_fee += fee
            break  # 白天費率處理完成後跳出
        else:  # 夜間時段
            if is_holiday_flag:  # 假日夜間費率
                total_fee += holiday_night_price
            else:  # 平日夜間費率
                total_fee += hour_price_night
        current_time += timedelta(hours=1)

    # 如果是假日，確保總收費不超過假日每日上限
    if is_holiday_flag:
        total_fee = min(total_fee, holiday_daily_limit)

    return total_fee

# 分析停車數據
def analyze_parking_data(file_path):
    total_revenue = 0
    original_revenue = 0

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['order_start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['order_end_time'], '%Y-%m-%d %H:%M:%S')

            # 計算新費率下的收入
            new_fee = calculate_parking_fee(start_time, end_time)
            total_revenue += new_fee

            # 計算原始收入
            original_fee = float(row['payment_amount'])
            original_revenue += original_fee

    # 顯示結果
    print(f"{building_name} 原收費方式總收入: {original_revenue/7:.2f} 元")
    print(f"{building_name} 新收費方式總收入: {total_revenue/7:.2f} 元")
    print(f"收入變動: {(total_revenue - original_revenue)/7:.2f} 元")
    print(f"收入變動比例: {((total_revenue - original_revenue) / original_revenue) * 100/7:.2f}%")

if __name__ == "__main__":
    file_path = "USPACE/國家企業中心.csv"  # 請確認正確的文件路徑
    analyze_parking_data(file_path)
