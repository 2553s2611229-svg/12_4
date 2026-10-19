import streamlit as st

st.set_page_config(
    page_title="수업 안내 | 학교생활 가이드",
    page_icon="📘",
    layout="centered",
)

st.title("수업 안내")
st.caption("새로운 학교생활, 차근차근 알아가요 ✨")

if "page" not in st.session_state:
    st.session_state.page = "home"

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("↻ 새로고침"):
    st.session_state.page = "home"
    st.session_state.history = []
    st.rerun()

if st.button("‹ 뒤로 가기"):
    if st.session_state.history:
        st.session_state.page = (
            st.session_state.history.pop()
        )
    else:
        st.session_state.page = "home"
    st.rerun()
