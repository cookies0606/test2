import streamlit as st
import sqlite3
from datetime import datetime

# DB 연결
conn = sqlite3.connect("employee.db", check_same_thread=False)
cursor = conn.cursor()

# 현재 로그인한 직원 (간단 예시용)
EMPLOYEE_ID = 1

# 출퇴근 기록하기
st.header("🕒 출근 / 퇴근 기록")

now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
location = st.text_input("위치 (예: Busan 본사, 재택 등)")

if st.button("출근"):
    today = datetime.now().date().isoformat()
    cursor.execute("INSERT INTO attendance_logs (employee_id, date, clock_in, location) VALUES (?, ?, ?, ?)",
                   (EMPLOYEE_ID, today, now, location))
    conn.commit()
    st.success(f"출근 시간 기록됨: {now}")

if st.button("퇴근"):
    today = datetime.now().date().isoformat()
    cursor.execute("UPDATE attendance_logs SET clock_out=? WHERE employee_id=? AND date=?",
                   (now, EMPLOYEE_ID, today))
    conn.commit()
    st.success(f"퇴근 시간 기록됨: {now}")

# 휴가 기록
st.header("🏖️ 휴가 기록")

with st.form("vacation_form"):
    vacation_type = st.selectbox("휴가 유형", ["연차", "병가", "경조사", "기타"])
    start_date = st.date_input("시작일")
    end_date = st.date_input("종료일")
    reason = st.text_area("사유")
    submit = st.form_submit_button("휴가 신청")

    if submit:
        days = (end_date - start_date).days + 1
        cursor.execute("INSERT INTO vacations (employee_id, vacation_type, start_date, end_date, days, reason) VALUES (?, ?, ?, ?, ?, ?)",
                       (EMPLOYEE_ID, vacation_type, start_date.isoformat(), end_date.isoformat(), days, reason))
        conn.commit()
        st.success(f"{days}일 휴가 등록 완료")
