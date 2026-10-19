
import streamlit as st
from datetime import date, timedelta

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="우리 반 학교생활 안내",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown("""
<style>
.stApp {
    background-color: #F5F8FC;
}
h1, h2, h3 {
    color: #24466A;
}
div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #DCE7F4;
    padding: 16px;
    border-radius: 14px;
}
div.stButton > button {
    border-radius: 10px;
    border: 1px solid #D5E3F3;
}
.guide-card {
    background: white;
    border: 1px solid #DCE7F4;
    border-radius: 14px;
    padding: 18px;
    margin-bottom: 12px;
}
.small-note {
    color: #61758B;
    font-size: 0.9rem;
}
</style>
""", unsafe_allow_html=True)

# -----------------------------
# 기본 예시 데이터
# -----------------------------
DAYS = ["월요일", "화요일", "수요일", "목요일", "금요일"]
PERIODS = ["1교시", "2교시", "3교시", "4교시", "5교시", "6교시"]

DEFAULT_TIMETABLE = {
    "교시": PERIODS,
    "월요일": ["국어", "수학", "영어", "통합과학", "체육", "사회"],
    "화요일": ["수학", "영어", "국어", "정보", "사회", "미술"],
    "수요일": ["영어", "통합과학", "수학", "국어", "체육", "창체"],
    "목요일": ["사회", "국어", "영어", "수학", "정보", "통합과학"],
    "금요일": ["수학", "체육", "사회", "영어", "국어", "창체"],
}

def make_default_assignments():
    today = date.today()
    return [
        {
            "완료": False,
            "과목": "국어",
            "과제": "독서 활동 기록 작성",
            "마감일": (today + timedelta(days=2)).isoformat(),
            "준비물/메모": "읽은 책, 필기도구",
        },
        {
            "완료": False,
            "과목": "통합과학",
            "과제": "탐구 주제 조사",
            "마감일": (today + timedelta(days=4)).isoformat(),
            "준비물/메모": "탐구 자료",
        },
    ]

# -----------------------------
# 세션 상태 초기화
# -----------------------------
if "timetable" not in st.session_state:
    st.session_state.timetable = DEFAULT_TIMETABLE.copy()
    st.session_state.timetable = {
        key: value.copy()
        for key, value in DEFAULT_TIMETABLE.items()
    }

if "assignments" not in st.session_state:
    st.session_state.assignments = make_default_assignments()

if "current_page" not in st.session_state:
    st.session_state.current_page = "홈"

if "page_history" not in st.session_state:
    st.session_state.page_history = []

if "reset_notice" not in st.session_state:
    st.session_state.reset_notice = False

# -----------------------------
# 페이지 이동
# -----------------------------
PAGES = ["홈", "이번 주 시간표", "과제·준비물", "학교생활 가이드"]

def go_to(page):
    current = st.session_state.current_page
    if page != current:
        st.session_state.page_history.append(current)
        st.session_state.page_history = st.session_state.page_history[-20:]
    st.session_state.current_page = page

def go_back():
    history = st.session_state.page_history
    if history:
        st.session_state.current_page = history.pop()
    else:
        st.session_state.current_page = "홈"

def reset_demo():
    st.session_state.timetable = {
        key: value.copy()
        for key, value in DEFAULT_TIMETABLE.items()
    }
    st.session_state.assignments = make_default_assignments()
    st.session_state.current_page = "홈"
    st.session_state.page_history = []
    st.session_state.reset_notice = True

# -----------------------------
# 사이드바
# -----------------------------
with st.sidebar:
    st.markdown("# 📚 우리 반 안내")
    st.caption("새로운 학교생활, 차근차근!")

    st.markdown("---")
    st.markdown("### 메뉴")

    for page in PAGES:
        icon = {
            "홈": "🏠",
            "이번 주 시간표": "🗓️",
            "과제·준비물": "📝",
            "학교생활 가이드": "🎒",
        }[page]

        if st.button(
            f"{icon}  {page}",
            key=f"nav_{page}",
            use_container_width=True,
            type=(
                "primary"
                if st.session_state.current_page == page
                else "secondary"
            ),
        ):
            go_to(page)
            st.rerun()

    st.markdown("---")

    col_back, col_refresh = st.columns(2)

    with col_back:
        if st.button("⬅️ 이전", use_container_width=True):
            go_back()
            st.rerun()

    with col_refresh:
        if st.button("🔄 새로고침", use_container_width=True):
            st.rerun()

    st.caption(
        "새로고침은 화면을 다시 실행합니다. "
        "입력 내용 초기화는 아래 버튼을 이용하세요."
    )

    if st.button(
        "↩️ 예시 데이터로 초기화",
        use_container_width=True,
    ):
        reset_demo()
        st.rerun()

# -----------------------------
# 상단 제목
# -----------------------------
st.title("📚 우리 반 학교생활 안내")
st.markdown(
    '<p class="small-note">'
    '수업 시간표부터 과제, 학교생활 팁까지 한곳에서 확인해요.'
    '</p>',
    unsafe_allow_html=True,
)

if st.session_state.reset_notice:
    st.success("예시 데이터로 초기화했어요.")
    st.session_state.reset_notice = False

st.markdown("---")

# -----------------------------
# 홈
# -----------------------------
if st.session_state.current_page == "홈":
    today = date.today()
    weekday = today.weekday()

    st.markdown("## 안녕! 오늘도 즐거운 학교생활 🌱")
    st.write(
        "처음이라 낯설어도 괜찮아. "
        "오늘의 수업과 해야 할 일을 하나씩 확인해 보자."
    )

    total = len(st.session_state.assignments)
    completed = sum(
        1 for item in st.session_state.assignments
        if item.get("완료", False)
    )
    remaining = total - completed

    c1, c2, c3 = st.columns(3)
    c1.metric("📅 오늘", today.strftime("%m월 %d일"))
    c2.metric("📝 등록된 과제", total)
    c3.metric("⏳ 남은 과제", remaining)

    st.markdown("## 🗓️ 오늘의 수업")

    if weekday < 5:
        day_name = DAYS[weekday]
        subjects = st.session_state.timetable.get(day_name, [])
        st.info(
            f"**{day_name}** 수업을 확인해 보세요. "
            "시간표는 '이번 주 시간표' 메뉴에서 수정할 수 있어요."
        )

        cols = st.columns(3)
        for i, subject in enumerate(subjects):
            if i < len(PERIODS):
                with cols[i % 3]:
                    st.markdown(
                        f'<div class="guide-card">'
                        f'<b>{PERIODS[i]}</b><br>'
                        f'📘 {subject if subject else "미입력"}'
                        f'</div>',
                        unsafe_allow_html=True,
                    )
    else:
        st.info("오늘은 주말이에요. 다음 주 준비물을 확인해 보세요!")

    st.markdown("## 🚀 바로가기")
    c1, c2, c3 = st.columns(3)

    with c1:
        if st.button("🗓️ 시간표 확인", use_container_width=True):
            go_to("이번 주 시간표")
            st.rerun()

    with c2:
        if st.button("📝 과제 확인", use_container_width=True):
            go_to("과제·준비물")
            st.rerun()

    with c3:
        if st.button("🎒 학교생활 팁", use_container_width=True):
            go_to("학교생활 가이드")
            st.rerun()

    st.markdown("---")
    st.markdown("### 💡 오늘의 한마디")
    st.success(
        "모르는 것이 있다면 혼자 고민하지 말고 "
        "친구나 선생님에게 질문해도 괜찮아요!"
    )

# -----------------------------
# 이번 주 시간표
# -----------------------------
elif st.session_state.current_page == "이번 주 시간표":
    st.markdown("## 🗓️ 우리 반 이번 주 시간표")
    st.write(
        "표 안의 과목명을 클릭해 수정할 수 있어요. "
        "변경 내용은 현재 브라우저 세션에 저장됩니다."
    )

    try:
        import pandas as pd

        timetable_df = pd.DataFrame(st.session_state.timetable)
        edited_df = st.data_editor(
            timetable_df,
            key="timetable_editor",
            use_container_width=True,
            hide_index=True,
            num_rows="fixed",
            disabled=["교시"],
            column_config={
                "교시": st.column_config.TextColumn("교시"),
            },
        )

        if st.button("💾 시간표 변경 적용", type="primary"):
            new_data = {}
            for column in ["교시"] + DAYS:
                if column in edited_df.columns:
                    new_data[column] = (
                        edited_df[column].fillna("").astype(str).tolist()
                    )

            if all(day in new_data for day in DAYS):
                new_data["교시"] = PERIODS.copy()
                st.session_state.timetable = new_data
                st.success("시간표를 적용했어요!")
                st.rerun()
            else:
                st.error("시간표 형식을 확인하고 다시 시도해 주세요.")

    except Exception as e:
        st.error("시간표를 표시하지 못했어요. 다시 시도해 주세요.")
        st.caption(f"오류 정보: {type(e).__name__}")

    st.caption(
        "※ 실제 학교 시간표를 확인한 뒤 과목명을 수정해 주세요. "
        "이 앱의 기본 시간표는 예시입니다."
    )

# -----------------------------
# 과제 및 준비물
# -----------------------------
elif st.session_state.current_page == "과제·준비물":
    st.markdown("## 📝 과제 및 준비물")
    st.write("과제를 추가하고 완료 여부를 체크해 보세요.")

    assignments = st.session_state.assignments

    if assignments:
        try:
            import pandas as pd

            assignment_df = pd.DataFrame(assignments)
            edited_assignments = st.data_editor(
                assignment_df,
                key="assignment_editor",
                use_container_width=True,
                hide_index=True,
                num_rows="fixed",
                column_config={
                    "완료": st.column_config.CheckboxColumn("완료"),
                    "과목": st.column_config.TextColumn("과목"),
                    "과제": st.column_config.TextColumn("과제"),
                    "마감일": st.column_config.TextColumn(
                        "마감일", help="YYYY-MM-DD 형식"
                    ),
                    "준비물/메모": st.column_config.TextColumn("준비물/메모"),
                },
            )

            if st.button("💾 과제 변경 적용", type="primary"):
                st.session_state.assignments = (
                    edited_assignments.fillna("").to_dict("records")
                )
                st.success("과제 변경 내용을 적용했어요!")
                st.rerun()

        except Exception as e:
            st.error("과제 목록을 표시하지 못했어요.")
            st.caption(f"오류 정보: {type(e).__name__}")
    else:
        st.info("아직 등록된 과제가 없어요. 아래에서 추가해 보세요.")

    st.markdown("---")
    st.markdown("### ➕ 새 과제 추가")

    with st.form("add_assignment_form", clear_on_submit=True):
        subject = st.selectbox(
            "과목",
            ["국어", "수학", "영어", "통합과학", "사회", "정보", "기타"],
        )
        task = st.text_input("과제명", placeholder="예: 탐구 보고서 작성")
        due_date = st.date_input(
            "마감일",
            value=date.today() + timedelta(days=3),
        )
        memo = st.text_input(
            "준비물 또는 메모",
            placeholder="예: 교과서, 필기도구",
        )

        submitted = st.form_submit_button("과제 등록")

        if submitted:
            if not task.strip():
                st.warning("과제명을 입력해 주세요.")
            else:
                st.session_state.assignments.append({
                    "완료": False,
                    "과목": subject,
                    "과제": task.strip(),
                    "마감일": due_date.isoformat(),
                    "준비물/메모": memo.strip(),
                })
                st.success("과제를 등록했어요!")
                st.rerun()

    st.markdown("---")
    st.markdown("### 🗑️ 과제 삭제")

    if st.session_state.assignments:
        task_options = [
            f"{i + 1}. {item.get('과목', '')} - "
            f"{item.get('과제', '')}"
            for i, item in enumerate(st.session_state.assignments)
        ]
        selected_task = st.selectbox(
            "삭제할 과제를 선택하세요.",
            options=list(range(len(task_options))),
            format_func=lambda i: task_options[i],
        )

        if st.button("선택한 과제 삭제"):
            st.session_state.assignments.pop(selected_task)
            st.success("과제를 삭제했어요.")
            st.rerun()

# -----------------------------
# 학교생활 가이드
# -----------------------------
elif st.session_state.current_page == "학교생활 가이드":
    st.markdown("## 🎒 새로운 학교에 적응하는 방법")
    st.write(
        "학교마다 규칙과 수업 방식이 다를 수 있어요. "
        "아래 내용을 참고하고, 정확한 규칙은 담당 선생님께 확인하세요."
    )

    guides = [
        (
            "📖 수업 준비",
            "시간표를 미리 확인하고 교과서, 필기도구, "
            "과목별 준비물을 챙겨요. 수업 시작 전에 자리에 앉아 준비해요.",
        ),
        (
            "📝 과제 제출",
            "과제의 제출 기한과 제출 방법을 확인해요. "
            "온라인 제출인지 종이 제출인지 헷갈리면 선생님께 물어봐요.",
        ),
        (
            "🔬 수행평가와 탐구",
            "평가 기준과 제출 날짜를 먼저 확인하고, "
            "큰 과제는 여러 단계로 나누어 진행해요.",
        ),
        (
            "🤝 친구와 선생님에게 질문하기",
            "모르는 내용은 구체적으로 질문해도 괜찮아요. "
            "친구에게 수업 방식이나 학교생활 팁을 물어보는 것도 좋아요.",
        ),
        (
            "📌 학교 공지 확인",
            "학교 알림장, 학급 공지, 공식 학습 플랫폼을 "
            "정기적으로 확인해 중요한 일정을 놓치지 않도록 해요.",
        ),
    ]

    for title, description in guides:
        with st.expander(title, expanded=False):
            st.write(description)

    st.markdown("---")
    st.success(
        "적응에는 시간이 필요해요. 작은 것부터 하나씩 익혀 나가면 돼요!"
    )

# -----------------------------
# 하단 안내
# -----------------------------
st.markdown("---")
st.caption(
    "📚 우리 반 학교생활 안내 | 예시 자료를 실제 학교 정보에 맞게 수정하세요."
)
