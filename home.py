import streamlit as st
import pandas as pd
import datetime
import plotly.express as px

# 📅 날짜
today = datetime.date.today()

# -----------------------------
# 헤더 및 소개
# -----------------------------
st.set_page_config(page_title="🏭 ERP 홈 대시보드", layout="wide")
st.title("visionerp")
st.markdown("""
이 시스템은 소규모 제조기업을 위한 **경량 ERP 솔루션**입니다.

---

### 오늘의 주요 지표 요약
""")

# -----------------------------
# 더미 데이터
# -----------------------------
production_today = 4
stock_summary = {'원자재': 24, '완제품': 8}
monthly_sales = {'건수': 102, '매출': 9400000}
pending_io = {'입고': 2, '출고': 1}

production_log = pd.DataFrame({
    '날짜': pd.date_range(end=today, periods=7),
    '생산량': [80, 120, 90, 100, 130, 110, 150]
})

# -----------------------------
# KPI 지표
# -----------------------------
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric("👷 오늘의 생산계획", f"{production_today} 건")

with col2:
    st.metric("📦 원자재", f"{stock_summary['원자재']} 종")
    st.metric("📦 완제품", f"{stock_summary['완제품']} 종")

with col3:
    st.metric("💰 판매건수", f"{monthly_sales['건수']} 건")
    st.metric("💵 월 매출", f"₩{monthly_sales['매출']:,}")

with col4:
    st.metric("⏳ 입고 대기", f"{pending_io['입고']} 건")
    st.metric("📤 출고 대기", f"{pending_io['출고']} 건")

st.divider()

# -----------------------------
# 생산량 그래프
# -----------------------------
st.subheader("📈 최근 7일 생산량 추이")
fig = px.bar(production_log, x='날짜', y='생산량', title='최근 생산량', labels={'생산량': '단위: 개'})
st.plotly_chart(fig, use_container_width=True)

# -----------------------------
# 안내 및 TODO
# -----------------------------
st.info("📌 좌측 메뉴에서 다른 기능으로 이동하세요.")
