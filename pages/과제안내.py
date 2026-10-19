
import streamlit as st
from datetime import date, timedelta

st.set_page_config(
    page_title="우리 반 학교생활 안내",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown(
    """
    <style>
    .main-title {
        font-size: 2.25rem;
        font-weight: 800;
        margin-bottom: .2rem;
    }
    .sub-title {
        color: #64748b;
        margin-top: 0;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# 처음 실행할 때 표시할 예시 과제
if "assignments" not in st.session_state:
    st.session_state.assignments = [
        {
            "id": 1,
            "title": "영어 자기소개문 작성",
            "subject": "영어",
            "due": date.today() + timedelta(days=2),
            "details": "나를 소개하는 문장 8~10개를 작성해요.",
            "done": False,
        },
        {
            "id": 2,
            "title": "과학 관찰 기록 제출",
            "subject": "과학",
            "due": date.today() + timedelta(days=5),
            "details": "관찰한 내용과 느낀 점을 기록해요.",
            "done": False,
        },
        {
            "id": 3,
            "title": "수학 문제집 32~35쪽",
            "subject": "수학",
            "due": date.today() - timedelta(days=1),
            "details": "틀린 문제는 풀이 과정을 다시 확인해요.",
            "done": False,
        },
    ]

if "next_id" not in st.session_state:
    st.session_state.next_id = 4

today = date.today()
assignments = st.session_state.assignments


def due_label(due, done):
    """제출 상태와 마감일까지 남은 기간을 표시합니다."""
    if done:
        return "✅ 제출 완료"

    days_left = (due - today).days

    if days_left < 0:
        return f"🔴 기한 지남 · {abs(days_left)}일"
    if days_left == 0:
        return "🟠 오늘 마감"
    if days_left == 1:
        return "🟡 내일 마감"
    return f"🟢 {days_left}일 남음"


def sorted_assignments(items):
    """미제출 과제를 먼저, 마감일이 가까운 순으로 정렬합니다."""
    return sorted(
        items,
        key=lambda item: (
            item["done"],
            item["due"],
            item["title"].lower(),
        ),
    )


# 사이드바 메뉴
with st.sidebar:
    st.title("📚 우리 반 안내")

    page = st.radio(
        "메뉴",
        [
            "과제 한눈에 보기",
            "과제 추가하기",
            "학교생활 길잡이",
        ],
    )

    st.divider()
    st.caption(f"오늘 날짜: {today.strftime('%Y년 %m월 %d일')}")
    st.caption("과제는 현재 세션에 임시 저장됩니다.")


# 1. 과제 대시보드
if page == "과제 한눈에 보기":
    st.markdown(
        '<div class="main-title">'
        '이번 주, 놓치지 말아야 할 과제'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<p class="sub-title">'
        '마감일을 확인하고, 끝낸 과제는 제출 완료로 표시해 보세요.'
        '</p>',
        unsafe_allow_html=True,
    )

    pending = [a for a in assignments if not a["done"]]
    overdue = [a for a in pending if a["due"] < today]
    due_today = [a for a in pending if a["due"] == today]

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("전체 과제", len(assignments))
    c2.metric("남은 과제", len(pending))
    c3.metric("오늘 마감", len(due_today))
    c4.metric("기한 지남", len(overdue))

    st.divider()

    filter_option = st.selectbox(
        "과제 보기",
        [
            "전체",
            "미제출만",
            "제출 완료만",
            "기한 지남",
            "오늘 마감",
            "앞으로 마감",
        ],
    )

    subject_options = ["모든 과목"] + sorted(
        {a["subject"] for a in assignments}
    )
    selected_subject = st.selectbox("과목", subject_options)

    filtered = assignments[:]

    if filter_option == "미제출만":
        filtered = [a for a in filtered if not a["done"]]
    elif filter_option == "제출 완료만":
        filtered = [a for a in filtered if a["done"]]
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

    if not filtered:
        st.info(
            "조건에 맞는 과제가 없어요. "
            "필터를 바꾸거나 새 과제를 추가해 보세요."
        )

    for item in sorted_assignments(filtered):
        with st.container(border=True):
            left, right = st.columns([4, 1])

            with left:
                st.subheader(item["title"])
                st.caption(
                    f"📘 {item['subject']} · "
                    f"📅 제출 기한: "
                    f"{item['due'].strftime('%Y년 %m월 %d일')}"
                )
                st.write(
                    item["details"]
                    if item["details"]
                    else "추가 설명이 없습니다."
                )
                st.write(due_label(item["due"], item["done"]))

            with right:
                new_done = st.checkbox(
                    "제출 완료",
                    value=item["done"],
                    key=f"done_{item['id']}",
                )

                if new_done != item["done"]:
                    item["done"] = new_done
                    st.rerun()

                if st.button(
                    "삭제",
                    key=f"delete_{item['id']}",
                ):
                    st.session_state.assignments = [
                        a for a in st.session_state.assignments
                        if a["id"] != item["id"]
                    ]
                    st.rerun()

    st.divider()
    st.caption(
        "처음 실행하면 예시 과제가 표시됩니다. "
        "실제 과제에 맞게 사용하거나 삭제해 주세요."
    )


# 2. 과제 추가
elif page == "과제 추가하기":
    st.title("✍️ 새 과제 등록")
    st.write("과목과 제출 기한을 입력하면 과제 목록에 추가됩니다.")

    with st.form("add_assignment_form", clear_on_submit=True):
        title = st.text_input(
            "과제 이름 *",
            placeholder="예: 국어 독서 감상문",
        )

        subject = st.selectbox(
            "과목",
            [
                "국어", "영어", "수학", "사회", "과학",
                "정보", "체육", "예체능", "기타",
            ],
        )

        due = st.date_input(
            "제출 기한 *",
            value=today + timedelta(days=3),
            min_value=date(2000, 1, 1),
        )

        details = st.text_area(
            "과제 설명 (선택)",
            placeholder="분량, 제출 방법, 준비물 등을 적어 주세요.",
        )

        submitted = st.form_submit_button(
            "과제 추가",
            type="primary",
        )

    if submitted:
        clean_title = title.strip()
        clean_details = details.strip()

        if not clean_title:
            st.error("과제 이름을 입력해 주세요.")
        elif len(clean_title) > 120:
            st.error("과제 이름은 120자 이하로 입력해 주세요.")
        elif len(clean_details) > 1000:
            st.error("과제 설명은 1,000자 이하로 입력해 주세요.")
        else:
            st.session_state.assignments.append(
                {
                    "id": st.session_state.next_id,
                    "title": clean_title,
                    "subject": subject,
                    "due": due,
                    "details": clean_details,
                    "done": False,
                }
            )
            st.session_state.next_id += 1

            st.success(
                "과제를 추가했어요! "
                "‘과제 한눈에 보기’에서 확인할 수 있습니다."
            )
            st.rerun()

    st.info(
        "팁: 제출 위치나 파일 형식도 설명에 적어 두면 "
        "과제를 빠뜨릴 가능성이 줄어들어요."
    )


# 3. 학교생활 길잡이
else:
    st.title("🧭 새로운 학교생활 길잡이")
    st.write(
        "새로운 학교의 수업과 과제 방식에 적응할 때 "
        "참고할 수 있는 기본 안내예요."
    )

    with st.expander("📒 수업 준비 체크리스트", expanded=True):
        st.checkbox(
            "시간표와 교실 위치를 확인했어요.",
            key="guide_timetable",
        )
        st.checkbox(
            "과목별 교과서와 준비물을 챙겼어요.",
            key="guide_books",
        )
        st.checkbox(
            "수업 시작 전에 자리에 앉아 준비했어요.",
            key="guide_ready",
        )
        st.checkbox(
            "모르는 내용은 표시해 두었다가 질문했어요.",
            key="guide_question",
        )

    with st.expander("📝 과제 제출 전 확인"):
        st.checkbox(
            "과제 지시문과 분량을 확인했어요.",
            key="guide_instructions",
        )
        st.checkbox(
            "파일 이름과 제출 형식을 확인했어요.",
            key="guide_format",
        )
        st.checkbox(
            "마감일과 제출 위치를 확인했어요.",
            key="guide_deadline",
        )
        st.checkbox(
            "제출 후 완료 여부를 확인했어요.",
            key="guide_submit",
        )

    with st.expander("🤝 학교생활에 적응하는 작은 팁"):
        st.markdown(
            """
            - **일정은 한곳에 기록하기:** 과제와 시험 날짜를 적어요.
            - **모르면 빨리 물어보기:** 선생님이나 친구에게 규칙을 확인해요.
            - **과제를 나누어 하기:** 마감 전까지 할 일을 작게 나눠요.
            - **하루 마무리 3분:** 내일 시간표와 준비물을 확인해요.
            """
        )

    st.warning(
        "학교와 선생님마다 규칙이 다를 수 있어요. "
        "정확한 제출 방식은 선생님의 공지와 학교 안내를 "
        "우선으로 확인하세요."
    )


st.sidebar.divider()
st.sidebar.caption("우리 반 학교생활 안내 · 과제 관리 앱")
