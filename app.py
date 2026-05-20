import streamlit as st
import pandas as pd

st.set_page_config(page_title="스케줄 표", layout="centered")

st.title("📅 나의 스케줄 표")

# 기본 시간표 데이터
if "schedule" not in st.session_state:
    st.session_state.schedule = pd.DataFrame({
        "시간": [
            "09:00",
            "10:00",
            "11:00",
            "12:00",
            "13:00",
            "14:00",
            "15:00",
            "16:00",
            "17:00",
        ],
        "일정": [""] * 9
    })

st.subheader("스케줄 입력")

# 편집 가능한 테이블
edited_df = st.data_editor(
    st.session_state.schedule,
    num_rows="fixed",
    use_container_width=True
)

# 저장 버튼
if st.button("저장"):
    st.session_state.schedule = edited_df
    st.success("스케줄이 저장되었습니다!")

st.subheader("현재 스케줄")

# 저장된 데이터 출력
st.table(st.session_state.schedule)
