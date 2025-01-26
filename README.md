# USPACE-Data-Analysis 停車營收分析
旨在分析停車收費方案變更後的營收差異。透過處理停車訂單的 CSV 資料，根據靈活的時段費率設定計算新舊營收。

## 功能特點
- **動態費率設定**：支援平日與週末的早晨、日間及夜間不同費率。
- **每日上限**：可選擇啟用每日營收上限，分別針對平日與週末。
- **營收比較**：計算新舊營收，分析費率調整的財務影響。
- **日期範圍分析**：提供按月份或年份的營收報告。

## 需求
- Python 3.11.11
- pandas 套件

安裝依賴項：
```bash
pip install pandas
