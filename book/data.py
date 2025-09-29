import numpy as np
import pandas as pd


def _adj_or_not():
    df = pd.read_csv(r"C:\Users\liuchufan\Documents\601012.csv")
    df = df.sort_values('trade_date').reset_index(drop=True)
    # 计算理论涨跌幅（基于pre_close和close）
    df['pct_compute'] = (df['close'] - df['pre_close']) / df['pre_close'] * 100
    # 计算涨跌幅偏差（实际pct_chg与理论涨跌幅的差异）
    df['pct_diff'] = np.abs(df['pct_chg'] - df['pct_compute'])
    # 检测除权缺口：偏差>0.5%且close≠pre_close（排除正常波动）
    df['is_adjustment_needed'] = (df['pct_diff'] > 0.5) & (df['close'] != df['pre_close'])
    adjustment_dates = df[df['is_adjustment_needed']]['trade_date'].tolist()
    if len(adjustment_dates) > 0:
        print(f"检测到{len(adjustment_dates)}个潜在除权除息日：")
        for date in adjustment_dates[:5]:  # 显示前5个
            print(f"  - {date.strftime('%Y-%m-%d')}（偏差值：{df.loc[df['date'] == date, 'pct_diff'].values:.2f}%）")
        return True
    else:
        print("未检测到需要复权的价格缺口，数据可能已复权或无除权事件")
        return False


if __name__ == "__main__":
    # df = pd.read_csv(r"C:\Users\liuchufan\Documents\601012.csv")
    # df = df.sort_values('trade_date').reset_index(drop=True)
    # df.dropna(inplace=True)
    # df.reset_index(inplace=True)
    # df.drop(columns=['index'], inplace=True)
    # print(df)
    df = pd.read_csv(r"C:\Users\liuchufan\Documents\601012_all.csv")
    print(df)
    # print(df.loc['2021-01-01': '2025-09-11'])
