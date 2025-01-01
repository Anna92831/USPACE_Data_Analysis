# 重置費率(下降)
import pandas as pd
import numpy as np
import csv
from datetime import datetime
#場站的基本資訊
building_name = "國家企業中心"
hour_price = 50
original_limit_price = 290
original_hour_limit = original_limit_price / hour_price
hour_3_price = 120
hour_8_price = 270
hour_10_price = 290
hour_12_price = 180
name = [
    f"3 小時重置 {hour_3_price} 元",
    f"8 小時重置 {hour_8_price} 元",
    f"10 小時重置 {hour_10_price} 元",
    f"12 小時重置 {hour_12_price} 元"
]
def calculate_parking_3_fee(duration_hours, reset_hours, reset_price):
    # 如果 original_hour_limit > reset_hours，我們需要修改計費邏輯
    if 0 <= duration_hours <= reset_hours:
        # 在重置時間內，按小時計費
        fee = duration_hours * hour_price
    elif reset_hours < duration_hours <= reset_hours * 2:
        # 超過第一個重置時間，使用重置價格
        fee = reset_price
    elif reset_hours * 2 < duration_hours <= reset_hours * 2+ original_hour_limit:
        # 超過第二個重置時間，使用兩倍重置價格
        fee = reset_price * 2 + (duration_hours-reset_hours * 2) * hour_price
    elif reset_hours * 2+ original_hour_limit < duration_hours <= reset_hours * 3:
        # 超過第三個重置時間，使用三倍重置價格
        fee = reset_price * 3
    elif reset_hours * 3 < duration_hours <=  reset_hours * 3+ original_hour_limit :
        # 超過第四個重置時間但在 24 小時內，使用四倍重置價格
        fee = reset_price * 3 + (duration_hours-reset_hours * 3) * hour_price
    else:
        # 超過 24 小時的情況
        days = duration_hours // 24
        remaining_hours = duration_hours % 24
        fee = days * (reset_price * 4) + calculate_parking_3_fee(remaining_hours, reset_hours, reset_price)
    return fee
def analyze_parking_data(file_path):
    # 所有重置費率
    reset_structures = [
        (3, hour_3_price),
        (8, hour_8_price),
        (10, hour_10_price),
        (12, hour_12_price)
    ]
    total_revenues = [0] * len(reset_structures)
    original_total_revenue = 0
    duration_3_counts = {f"0~{reset_hours}": 0, f"{reset_hours}~{original_hour_limit}": 0, 
                         f"{original_hour_limit}~{reset_hours + original_hour_limit}": 0, f"{reset_hours + original_hour_limit}~{reset_hours * 2 + original_hour_limit}": 0,
                         f"{reset_hours * 2 + original_hour_limit}~{reset_hours * 3 + original_hour_limit }": 0, f"{reset_hours * 3 + original_hour_limit}-{reset_hours * 4 + original_hour_limit}": 0,
                           f"{reset_hours * 4 + original_hour_limit}-{reset_hours * 5 + original_hour_limit}": 0,f"{reset_hours * 5 + original_hour_limit}-24": 0,
                           "24+": 0}

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['order_start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['order_end_time'], '%Y-%m-%d %H:%M:%S')
            duration_hours = (end_time - start_time).total_seconds() / 3600

            # 計算重置費率後的金額
            for i, (reset_hours, reset_price) in enumerate(reset_structures):
                fee = calculate_parking_8_fee(duration_hours, reset_hours, reset_price)
                total_revenues[i] += fee

            # 原本總營收
            original_fee = float(row['payment_amount'])
            original_total_revenue += original_fee

            
            if duration_hours <= original_hour_limit:
                duration_3_counts[f"0~{original_hour_limit}"] += 1
            elif original_hour_limit < duration_hours <= 8:
                duration_3_counts[f"{original_hour_limit}~8"] += 1
            elif 8 < duration_hours <= 8+original_hour_limit:
                duration_3_counts[f"8-{8+original_hour_limit}"] += 1
            elif 8+original_hour_limit < duration_hours <= 16:
                duration_3_counts[f"{8+original_hour_limit}-16"] += 1
            elif 16 < duration_hours <= 16+original_hour_limit:
                duration_3_counts[f"16-{16+original_hour_limit}"] += 1
            elif 16+original_hour_limit < duration_hours <= 24:
                duration_3_counts[f"{16+original_hour_limit}-24"] += 1
            else:
                duration_3_counts["24+"] += 1
def calculate_parking_8_fee(duration_hours, reset_hours, reset_price):
    if 0 <= duration_hours <= original_hour_limit:
        fee = duration_hours * hour_price
    elif original_hour_limit < duration_hours <= reset_hours:
        fee = reset_price
    elif reset_hours < duration_hours <= reset_hours + original_hour_limit:
        fee = reset_price + (duration_hours - reset_hours) * hour_price
    elif reset_hours + original_hour_limit < duration_hours <= reset_hours + original_hour_limit * 2:
        fee = reset_price * 2
    elif reset_hours + original_hour_limit * 2 < duration_hours <= reset_hours + original_hour_limit * 3:
        fee = reset_price * 2 + (duration_hours - reset_hours - original_hour_limit * 2) * hour_price
    elif reset_hours + original_hour_limit * 3 < duration_hours <= reset_hours + original_hour_limit * 4:
        fee = reset_price * 3
    else:
        days = duration_hours // 24
        remaining_hours = duration_hours % 24
        fee = days * (reset_price * 3) + calculate_parking_8_fee(remaining_hours, reset_hours, reset_price)
    return fee
def analyze_parking_data(file_path):

    reset_structures = [
        (3, hour_3_price),
        (8, hour_8_price),
        (10, hour_10_price),
        (12, hour_12_price)
    ]
    total_revenues = [0] * len(reset_structures)
    original_total_revenue = 0
    duration_8_counts = {f"0~{original_hour_limit}": 0, f"{original_hour_limit}~8": 0, f"8~{reset_hours + original_hour_limit}": 0, f"{reset_hours + original_hour_limit}~16": 0, f"16~{reset_hours + original_hour_limit * 3}": 0, f"{reset_hours + original_hour_limit * 3}-24": 0, "24+": 0}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['order_start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['order_end_time'], '%Y-%m-%d %H:%M:%S')
            duration_hours = (end_time - start_time).total_seconds() / 3600

           
            for i, (reset_hours, reset_price) in enumerate(reset_structures):
                fee = calculate_parking_8_fee(duration_hours, reset_hours, reset_price)
                total_revenues[i] += fee

          
            original_fee = float(row['payment_amount'])
            original_total_revenue += original_fee

           
            if duration_hours <= original_hour_limit:
                duration_8_counts[f"0~{original_hour_limit}"] += 1
            elif original_hour_limit < duration_hours <= 8:
                duration_8_counts[f"{original_hour_limit}~8"] += 1
            elif 8 < duration_hours <= 8+original_hour_limit:
                duration_8_counts[f"8-{8+original_hour_limit}"] += 1
            elif 8+original_hour_limit < duration_hours <= 16:
                duration_8_counts[f"{8+original_hour_limit}-16"] += 1
            elif 16 < duration_hours <= 16+original_hour_limit:
                duration_8_counts[f"16-{16+original_hour_limit}"] += 1
            elif 16+original_hour_limit < duration_hours <= 24:
                duration_8_counts[f"{16+original_hour_limit}-24"] += 1
            else:
                duration_8_counts["24+"] += 1
def calculate_parking_10_fee(duration_hours, reset_hours, reset_price):
    if 0 <= duration_hours <= original_hour_limit:
        fee = duration_hours * hour_price
    elif original_hour_limit < duration_hours <= reset_hours:
        fee = reset_price
    elif reset_hours < duration_hours <= reset_hours + original_hour_limit:
        fee = reset_price + (duration_hours - reset_hours) * hour_price
    elif reset_hours + original_hour_limit < duration_hours <= reset_hours * 2:
        fee = reset_price * 2
    elif reset_hours * 2 < duration_hours <= 24:
        fee = reset_price * 2 + (duration_hours - reset_hours * 2) * hour_price
    else:
        days = duration_hours // 24
        remaining_hours = duration_hours % 24
        fee = days * (reset_price * 3) + calculate_parking_10_fee(remaining_hours, reset_hours, reset_price)
    return fee
def analyze_parking_10_data(file_path):
    reset_structures = [(10, hour_10_price)]
    total_revenues = [0] * len(reset_structures)
    original_total_revenue = 0
    duration_10_counts = {f"0~{original_hour_limit}": 0, f"{original_hour_limit}~10": 0, f"10~{reset_hours + original_hour_limit}": 0, f"{reset_hours + original_hour_limit}~20": 0, "20-24": 0, "24+": 0}
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['order_start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['order_end_time'], '%Y-%m-%d %H:%M:%S')
            duration_hours = (end_time - start_time).total_seconds() / 3600

          
            for i, (reset_hours, reset_price) in enumerate(reset_structures):
                fee = calculate_parking_10_fee(duration_hours, reset_hours, reset_price)
                total_revenues[i] += fee

          
            original_fee = float(row['payment_amount'])
            original_total_revenue += original_fee

            
            if duration_hours <= original_hour_limit:
                duration_10_counts[f"0~{original_hour_limit}"] += 1
            elif original_hour_limit < duration_hours <= 10:
                duration_10_counts[f"{original_hour_limit}~10"] += 1
            elif 10 < duration_hours <= 10+original_hour_limit:
                duration_10_counts["10-10+original_hour_limit "] += 1  
            elif 10+original_hour_limit < duration_hours <= 20:
                duration_10_counts["10+original_hour_limit-20"] += 1
            elif 20 < duration_hours <= 24:
                duration_10_counts["20-24"] += 1
            else:
                duration_10_counts["24+"] += 1

def calculate_parking_12_fee(duration_hours, reset_hours, reset_price):
    if 0 <= duration_hours <= original_hour_limit:
        fee = duration_hours * hour_price
    elif original_hour_limit < duration_hours <= reset_hours:
        fee = reset_price
    elif reset_hours < duration_hours <= reset_hours + original_hour_limit:
        fee = reset_price + (duration_hours - reset_hours) * hour_price
    elif reset_hours + original_hour_limit < duration_hours <= 24:
        fee = reset_price * 2
    else:
        days = duration_hours // 24
        remaining_hours = duration_hours % 24
        fee = days * (reset_price * 2) + calculate_parking_12_fee(remaining_hours, reset_hours, reset_price)
    return fee

def analyze_parking_data(file_path):
    
    reset_structures = [
        (3, hour_3_price),
        (8, hour_8_price),
        (10, hour_10_price),
        (12, hour_12_price)
    ]
    total_revenues = [0] * len(reset_structures)
    original_total_revenue = 0
   
    duration_12_counts = {
        f"0~{original_hour_limit}": 0, 
        f"{original_hour_limit}~12": 0, 
        f"12~{12 + original_hour_limit}": 0, 
        f"{12 + original_hour_limit}~24": 0, 
        "24+": 0
    }

    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            start_time = datetime.strptime(row['order_start_time'], '%Y-%m-%d %H:%M:%S')
            end_time = datetime.strptime(row['order_end_time'], '%Y-%m-%d %H:%M:%S')
            duration_hours = (end_time - start_time).total_seconds() / 3600

            # 12 小時的重置架構
            for i, (reset_hours, reset_price) in enumerate(reset_structures):
                fee = calculate_parking_12_fee(duration_hours, reset_hours, reset_price)
                total_revenues[i] += fee

            # 原營收
            original_fee = float(row['payment_amount'])
            original_total_revenue += original_fee

            # 新重置方式的停車人數
            if duration_hours <= original_hour_limit:
                duration_12_counts[f"0~{original_hour_limit}"] += 1
            elif original_hour_limit < duration_hours <= 12:
                duration_12_counts[f"{original_hour_limit}~12"] += 1
            elif 12 < duration_hours <= 12+original_hour_limit:
                duration_12_counts[f"12~{reset_hours + original_hour_limit}"] += 1  
            elif 12+original_hour_limit < duration_hours <= 24:
                duration_12_counts[f"{reset_hours + original_hour_limit}~24"] += 1  
            else:
                duration_12_counts["24+"] += 1
     # 重置收費方式帶來多少營收
    # 重置後帶來的營收差異與比例變化
    revenue_differences = [0] * len(reset_structures)
    revenue_ratios = [0] * len(reset_structures)
    
    
  
    for i in range(len(reset_structures)):
        revenue_differences[i] = total_revenues[i] - original_total_revenue
        revenue_ratios[i] = (revenue_differences[i] / original_total_revenue) * 100

        # 判斷是增加還是減少收入
        if revenue_differences[i] > 0:
            (f"{name[i]} 增加收入: {revenue_differences[i]:.2f} 元")
        else:
            (f"{name[i]} 減少收入: {abs(revenue_differences[i]):.2f} 元")

        # 判斷是比例增加還是減少
        if revenue_ratios[i] > 0:
            (f"{name[i]} 比例增加: {revenue_differences[i]:.2f} %")
        else:
            (f"{name[i]} 比例減少: {abs(revenue_differences[i]):.2f} %")

    # 最終結果
    for i, (reset_hours, reset_price) in enumerate(reset_structures):
        print(f"{name[i]} 收費方式總收入: {total_revenues[i]:.2f} 元 變動營收:{revenue_differences[i]:.2f} 變動比例:{revenue_ratios[i]:.2f}")
    
    print(f"{building_name}原收費方式總收入: {original_total_revenue/7:.2f} 元")


if __name__ == "__main__":
    file_path = "USPACE/國家企業中心.csv"  # 請確認正確的文件路徑
    analyze_parking_data(file_path)
    
#計算不同時間的停車人數
file_path = "USPACE/國家企業中心.csv"  # 請確認正確的文件路徑
parking_df = pd.read_csv(file_path)

parking_df['order_start_time'] = pd.to_datetime(parking_df['order_start_time'])
parking_df['order_end_time'] = pd.to_datetime(parking_df['order_end_time'])

# 計算停放時數
parking_df['duration_minutes'] = (parking_df['order_end_time'] - parking_df['order_start_time']).dt.total_seconds() / 60

# 定義每一個停車區間時數
bins = [0, 15, 30, 60, 120, 180, 300, 480, 720, 960, 1440, np.inf]
labels = [
    '0-15 minutes',
    '15-30 minutes',
    '30-60 minutes',
    '1-2 hours',
    '2-3 hours',
    '3-5 hours',
    '5-8 hours',
    '8-12 hours',
    '12-16 hours',
    '16-24 hours',
    '24+ hours'
]

# 加上資料標籤
parking_df['duration_category'] = pd.cut(parking_df['duration_minutes'], bins=bins, labels=labels, right=False)

# 計算各停放區間的次數
duration_counts = parking_df['duration_category'].value_counts().reindex(labels)

# 用 Data Frame 的方式呈現出來
print("Parking Duration Distribution:")
print(duration_counts)
