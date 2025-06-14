import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# DB 연결
conn = sqlite3.connect("employee.db", check_same_thread=False)
cursor = conn.cursor()

# 테이블 생성
cursor.execute("""
    CREATE TABLE IF NOT EXISTS employees (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        position TEXT,
        department TEXT,
        join_date TEXT,
        email TEXT
    )
""")
# 출퇴근 테이블
cursor.execute("""
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        date TEXT,
        clock_in TEXT,
        clock_out TEXT,
        location TEXT
    )
""")

# 휴가 테이블
cursor.execute("""
    CREATE TABLE IF NOT EXISTS vacations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        vacation_type TEXT,
        start_date TEXT,
        end_date TEXT,
        days INTEGER,
        reason TEXT
    )
""")
conn.commit()

# Streamlit UI
st.set_page_config(page_title="인사 관리 시스템", layout="wide")
st.title("🧑‍💼 인사 관리 시스템 ")

menu = st.sidebar.radio("인사 관리 시스템", ["직원 등록", "직원 목록", "직원 수정", "직원 삭제", "출근/퇴근 기록", "휴가 기록"])

# 직원 등록
if menu == "직원 등록":
    st.subheader("직원 등록")

    with st.form("register_form"):
        name = st.text_input("이름")
        position = st.selectbox("직급", ["사원", "대리", "과장", "차장", "부장", "임원"])
        department = st.selectbox("부서", ["경영", "회계", "인사", "영업", "전산", "마케팅"])
        join_date = st.date_input("입사일", value=datetime.today())
        email = st.text_input("이메일")
        submitted = st.form_submit_button("등록")

        if submitted:
            cursor.execute(
                "INSERT INTO employees (name, position, department, join_date, email) VALUES (?, ?, ?, ?, ?)",
                (name, position, department, join_date.isoformat(), email)
            )
            conn.commit()
            st.success("직원이 등록되었습니다!")

# 직원 목록
elif menu == "직원 목록":
    st.subheader("📋 직원 목록")
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    st.dataframe(df, use_container_width=True)

# 직원 수정
elif menu == "직원 수정":
    st.subheader("🛠️ 직원 정보 수정")

    df = pd.read_sql_query("SELECT * FROM employees", conn)
    selected_id = st.selectbox("직원 선택 (ID)", df["id"])

    if selected_id:
        employee = df[df["id"] == selected_id].iloc[0]
        with st.form("edit_form"):
            name = st.text_input("이름", value=employee["name"])
            position = st.selectbox("직급", ["사원", "대리", "과장", "차장", "부장", "임원"], index=["사원", "대리", "과장", "차장", "부장", "임원"].index(employee["position"]))
            department = st.selectbox("부서", ["경영", "회계", "인사", "영업", "전산", "마케팅"], index=["경영", "회계", "인사", "영업", "전산", "마케팅"].index(employee["department"]))
            join_date = st.date_input("입사일", value=datetime.fromisoformat(employee["join_date"]))
            email = st.text_input("이메일", value=employee["email"])
            updated = st.form_submit_button("수정 완료")

            if updated:
                cursor.execute("""
                    UPDATE employees
                    SET name=?, position=?, department=?, join_date=?, email=?
                    WHERE id=?
                """, (name, position, department, join_date.isoformat(), email, selected_id))
                conn.commit()
                st.success("직원 정보가 수정되었습니다!")

# 직원 삭제
elif menu == "직원 삭제":
    st.subheader("🗑️ 직원 삭제")

    df = pd.read_sql_query("SELECT * FROM employees", conn)
    selected_id = st.selectbox("삭제할 직원 선택 (ID)", df["id"])

    if st.button("삭제"):
        cursor.execute("DELETE FROM employees WHERE id=?", (selected_id,))
        conn.commit()
        st.warning("직원 정보가 삭제되었습니다.")


elif menu == "출근/퇴근 기록":
    st.subheader("🕒 출근 / 퇴근 기록")
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    location = st.selectbox("위치", ["본사", "재택"])
    df = pd.read_sql_query("SELECT * FROM employees", conn)
    EMPLOYEE_ID = int(st.selectbox("직원 선택 (ID)", df["id"].tolist()))

    col1, col2 = st.columns([1,1])

    with col1:
        if st.button("출근"):
            today = datetime.now().date().isoformat()
            cursor.execute("INSERT INTO attendance_logs (employee_id, date, clock_in, location) VALUES (?, ?, ?, ?)",
                           (EMPLOYEE_ID, today, now, location))
            conn.commit()
            st.session_state.attendance = now
            st.success(f"출근 시간 기록됨: {now}")
    with col2:
        if st.button("퇴근"):
            today = datetime.now().date().isoformat()
            cursor.execute("UPDATE attendance_logs SET clock_out=? WHERE employee_id=? AND date=?",
                           (now, EMPLOYEE_ID, today))
            conn.commit()
            st.session_state.leave = now
            st.success(f"퇴근 시간 기록됨: {now}")
    st.subheader("근무 시간 확인")
    if st.button("확인"):
        if "attendance" in st.session_state and "leave" in st.session_state:
            work_time = st.session_state.leave - st.session_state.attendance
            st.success(f"근무 시간: {work_time}")
        else:
            st.warning("출근 및 퇴근 시간을 먼저 기록하세요.")
