import streamlit as st
import sys
import os

st.title("極簡啟動測試")
st.write("執行環境路徑:", os.getcwd())
st.write("Python 版本:", sys.version)

try:
    st.write("準備嘗試載入資料庫模組...")
    import cloud_db
    st.write("✅ cloud_db.py 引入成功")
except Exception as e:
    st.error(f"❌ 模組載入失敗: {e}")
    st.write("請檢查資料庫連線代碼是否有錯。")

st.success("🎉 如果看到這行，代表主程式已成功運行！")
