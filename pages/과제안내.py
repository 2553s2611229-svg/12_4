
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="우리 반 학교생활 안내",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
.block-container {
    padding-top: 0.8rem;
    padding-bottom: 0.6rem;
    max-width: 1500px;
}
h1 {
    font-size: 1.65rem !important;
    margin-bottom: 0.25rem !important;
}
h2, h3 {
    font-size: 1.1rem !important;
}
p, label, .stMarkdown {
    font-size: 0.9rem;
}
div[data-testid="stMetric"] {
    padding: 0.35rem 0.55rem;
    border: 1px solid rgba(128,128,128,0.25);
    border-radius: 10px;
}
div.stButton > button,
div.stFormSubmitButton > button {
    min-height: 2.1rem;
    padding: 0.25rem 0.65rem;
}
</style>
""", unsafe_allow_html=True)

today = date.today()

# 처음 실행할 때 표시되는 예시 과제
if "assignments" not in st.session_state:
    st.session_state.assignments = [
        {
            "id": 1,
            "title": "영어 자기소개문 작성",
            "subject": "영어",
            "due": today + timedelta(days=2),
            "details": "나를 소개하는 문장 8~10개 작성",
            "done": False
        },
        {
            "id": 2,
            "title": "과학 관찰 기록 제출",
            "subject": "과학",
            "due": today + timedelta(days=5),
            "details": "관찰 내용과 느낀 점 기록",
            "done": False
        },
        {
            "id": 3,
            "title": "수학 문제집 32~35쪽",
            "subject": "수학",
            "due": today - timedelta(days=1),
            "details": "틀린 문제 풀이 확인",
            "done": False
        }
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 4


def due_label(due, done):
    if done:
        return "✅ 제출 완료"

    days = (due - date.today()).days

    if days < 0:
        return f"🔴 기한 지남 {abs(days)}일"
    if days == 0:
        return "🟠 오늘 마감"
    if days == 1:
        return "🟡 내일 마감"

    return f"🟢 {days}일 남음"


def sorted_assignments(items):
    return sorted(
        items,
        key=lambda a: (
            a["done"],
            a["due"],
            a["title"].lower()
        )
    )


# 상단 제목과 가로 메뉴
st.title("📚 우리 반 학교생활 안내")
st.caption("과제 마감일과 수업 준비를 한 화면에서 확인하세요.")

page = st.radio(
    "메뉴",
    [
        "과제 한눈에 보기",
        "과제 추가하기",
        "학교생활 길잡이"
    ],
    horizontal=True,
    label_visibility="collapsed"
)

assignments = st.session_state.assignments


# 1. 과제 한눈에 보기
if page == "과제 한눈에 보기":

    pending = [
        a for a in assignments
        if not a["done"]
    ]

    overdue = [
        a for a in pending
        if a["due"] < today
    ]

    due_today = [
        a for a in pending
        if a["due"] == today
    ]

    m1, m2, m3, m4 = st.columns(4)

    m1.metric("전체 과제", len(assignments))
    m2.metric("남은 과제", len(pending))
    m3.metric("오늘 마감", len(due_today))
    m4.metric("기한 지남", len(overdue))

    st.markdown("#### 과제 목록")

    f1, f2 = st.columns(2)

    with f1:
        filter_option = st.selectbox(
            "상태",
            [
                "전체",
                "미제출만",
                "제출 완료만",
                "기한 지남",
                "오늘 마감",
                "앞으로 마감"
            ],
            label_visibility="collapsed"
        )

    with f2:
        subjects = ["모든 과목"] + sorted({
            a["subject"] for a in assignments
        })

        selected_subject = st.selectbox(
            "과목",
            subjects,
            label_visibility="collapsed"
        )

    filtered = assignments[:]

    if filter_option == "미제출만":
        filtered = [
            a for a in filtered
            if not a["done"]
        ]

    elif filter_option == "제출 완료만":
        filtered = [
            a for a in filtered
            if a["done"]
        ]

    elif filter_option == "기한 지남":
        filtered = [
            a for a in filtered
            if not a["done"] and a["due"] < today
        ]

    elif filter_option == "오늘 마감":
        filtered = [
            a for a in filtered
            if not a["done"] and a["due"] == today
        ]

    elif filter_option == "앞으로 마감":
        filtered = [
            a for a in filtered
            if not a["done"] and a["due"] > today
        ]

    if selected_subject != "모든 과목":
        filtered = [
            a for a in filtered
            if a["subject"] == selected_subject
        ]

    ordered = sorted_assignments(filtered)

    if not ordered:
        st.info(
            "표시할 과제가 없습니다. "
            "필터를 바꾸거나 과제를 추가해 보세요."
        )

    else:
        # 과제 카드를 두 열로 배치
        for start in range(0, len(ordered), 2):

            pair = ordered[start:start + 2]
            cols = st.columns(2)

            for col, item in zip(cols, pair):

                with col:
                    with st.container(border=True):

                        a, b = st.columns([3, 2])

                        with a:
                            st.markdown(
                                f"**{item['title']}**"
                            )
                            st.caption(
                                f"{item['subject']} · "
                                f"마감 {item['due'].strftime('%m/%d')}"
                            )

                        with b:
                            st.caption(
                                due_label(
                                    item["due"],
                                    item["done"]
                                )
                            )

                        if item["details"]:
                            st.caption(item["details"])

                        x, y = st.columns([3, 1])

                        with x:
                            checked = st.checkbox(
                                "제출 완료",
                                value=item["done"],
                                key=f"done_{item['id']}"
                            )

                            if checked != item["done"]:
                                item["done"] = checked
                                st.rerun()

                        with y:
                            if st.button(
                                "삭제",
                                key=f"delete_{item['id']}",
                                use_container_width=True
                            ):
                                st.session_state.assignments = [
                                    a for a in
                                    st.session_state.assignments
                                    if a["id"] != item["id"]
                                ]
                                st.rerun()

    st.caption(
        "※ 예시 과제는 실제 학교 공지에 맞게 수정하거나 삭제하세요."
    )


# 2. 과제 추가하기
elif page == "과제 추가하기":

    st.subheader("✍️ 새 과제 등록")

    with st.form(
        "add_assignment_form",
        clear_on_submit=True
    ):

        left, right = st.columns(2)

        with left:
            title = st.text_input(
                "과제 이름 *",
                placeholder="예: 국어 독서 감상문"
            )

            subject = st.selectbox(
                "과목",
                [
                    "국어", "영어", "수학", "사회",
                    "과학", "정보", "체육", "예체능", "기타"
                ]
            )

        with right:
            due = st.date_input(
                "제출 기한",
                value=today + timedelta(days=3)
            )

            details = st.text_input(
                "간단한 설명 (선택)",
                placeholder="분량, 제출 방법 등"
            )

        submitted = st.form_submit_button(
            "과제 추가",
            type="primary",
            use_container_width=True
        )

    if submitted:

        clean_title = title.strip()
        clean_details = details.strip()

        if not clean_title:
            st.error("과제 이름을 입력해 주세요.")

        elif len(clean_title) > 120:
            st.error("과제 이름은 120자 이하로 입력해 주세요.")

        elif len(clean_details) > 300:
            st.error("설명은 300자 이하로 입력해 주세요.")

        else:
            st.session_state.assignments.append({
                "id": st.session_state.next_id,
                "title": clean_title,
                "subject": subject,
                "due": due,
                "details": clean_details,
                "done": False
            })

            st.session_state.next_id += 1

            st.success("과제를 추가했습니다.")
            st.rerun()

    st.info(
        "등록한 과제는 ‘과제 한눈에 보기’에서 확인할 수 있어요."
    )


# 3. 학교생활 길잡이
else:

    st.subheader("🧭 새로운 학교생활 길잡이")

    left, right = st.columns(2)

    with left:
        with st.container(border=True):

            st.markdown("**📒 수업 준비**")

            st.checkbox(
                "시간표와 교실 위치 확인",
                key="guide_timetable"
            )

            st.checkbox(
                "교과서와 준비물 챙기기",
                key="guide_books"
            )

            st.checkbox(
                "수업 전에 자리에 앉아 준비",
                key="guide_ready"
            )

            st.checkbox(
                "모르는 내용은 질문하기",
                key="guide_question"
            )

    with right:
        with st.container(border=True):

            st.markdown("**📝 과제 제출 전 확인**")

            st.checkbox(
                "지시문과 분량 확인",
                key="guide_instructions"
            )

            st.checkbox(
                "파일 이름과 제출 형식 확인",
                key="guide_format"
            )

            st.checkbox(
                "마감일과 제출 위치 확인",
                key="guide_deadline"
            )

            st.checkbox(
                "제출 후 완료 여부 확인",
                key="guide_submit"
            )

    st.info(
        "학교와 선생님마다 규칙이 다를 수 있으니 "
        "공식 공지를 우선으로 확인하세요."
    )


st.divider()

st.caption(
    "간단한 과제 관리 앱 · 현재 세션에 임시 저장되며 "
    "영구 저장은 지원하지 않습니다."
)
