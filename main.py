import streamlit as st
import sys
import os
import pandas as pd

# 1. 強制修正路徑
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

try:
    import cloud_db
    import processor
except Exception as e:
    st.error(f"❌ 模組載入失敗: {e}")
    st.stop()

# --- 頁面配置 ---
st.set_page_config(page_title="Yetimall 簽售監測與門檻分析", layout="wide")

def main():
    st.title("📊 Yetimall 簽售即時監測與門檻分析")
    st.caption("即時追蹤用戶下單行為，分析前 10 名累計購買量與各國分佈")

    # --- 頂部核心指標 ---
    col1, col2, col3 = st.columns(3)
    # 這裡從 processor 獲取總結數據
    summary = processor.get_dashboard_summary() 
    with col1:
        st.metric("當前總銷量", f"{summary['total_sold']} 張")
    with col2:
        st.metric("監測到總人數", f"{summary['user_count']} 人")
    with col3:
        st.metric("安全門檻推估 (前10平均)", f"{summary['top10_avg']} 張")

    st.divider()

    # --- 核心佈局：左側排行榜，右側地理/強度分析 ---
    left_col, right_col = st.columns([2, 1])

    with left_col:
        st.subheader("🏆 累計購買量排行榜 (前 10 名)")
        st.info("💡 這個數值對預測中簽門檻最具參考意義")
        # 獲取前 10 名用戶數據 (UserID, 累計數量)
        leaderboard = processor.get_top_buyers(10)
        st.table(leaderboard)

    with right_col:
        st.subheader("🗺️ 下單地區分佈")
        # 顯示你要求的國家/地區判斷功能
        country_dist = processor.get_country_distribution()
        st.bar_chart(country_dist)
        
        st.subheader("📈 銷售強度增量")
        st.write("過去 1 小時增長:", f"+{summary['hourly_increase']} 張")

    # --- 原始日誌明細 (包含 API 攔截到的交易時間) ---
    st.subheader("📋 即時交易日誌 (API Data)")
    raw_logs = cloud_db.get_recent_transactions(limit=50)
    st.dataframe(raw_logs, use_container_width=True)

    # --- AI 分析報告 ---
    st.divider()
    if st.button("生成 Gemini AI 量化分析報告"):
        report = processor.generate_ai_report(leaderboard)
        st.markdown(f"### 🤖 AI 分析建議\n{report}")

if __name__ == "__main__":
    main()
