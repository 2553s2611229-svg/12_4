
import streamlit as st

# -----------------------------
# 기본 설정
# -----------------------------
st.set_page_config(
    page_title="우리학교 알리미",
    page_icon="🏫",
    layout="centered",
    initial_sidebar_state="expanded",
)

# -----------------------------
# 디자인
# -----------------------------
st.markdown(
    """
    <style>
    .stApp {
        background-color: #F7FAF8;
    }

    .main-title {
        color: #246B4B;
        font-size: 36px;
        font-weight: 800;
        text-align: center;
        margin-bottom: 8px;
    }

    .sub-title {
        color: #64748B;
        text-align: center;
        font-size: 16px;
        margin-bottom: 28px;
    }

    .welcome-box {
        background-color: #E7F4EC;
        border-radius: 16px;
        padding: 24px;
        text-align: center;
        margin-bottom: 22px;
        border: 1px solid #D3E8DA;
    }

    .welcome-box h2 {
        color: #246B4B;
        margin-top: 0;
    }

    .welcome-box p {
        color: #3D6650;
        margin-bottom: 0;
    }

    div.stButton > button {
        width: 100%;
        min-height: 58px;
        border-radius: 12px;
        border: 1px solid #D5E4DA;
        background-color: white;
        color: #246B4B;
        font-weight: 600;
    }

    div.stButton > button:hover {
        background-color: #E7F4EC;
        border-color: #78B58F;
        color: #185638;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# -----------------------------
# 페이지 데이터
# -----------------------------
PAGES = {
    "home": "🏠 메인 페이지",
    "class": "📚 수업 안내",
    "assignment": "📝 과제 안내",
    "life": "🏫 학교생활 안내",
    "checklist": "✅ 적응 체크리스트",
}

if "page" not in st.session_state:
    st.session_state.page = "home"

if "checked_items" not in st.session_state:
    st.session_state.checked_items = {}

# -----------------------------
# 페이지 이동 함수
# -----------------------------
def go_to(page):
    if page in PAGES:
        st.session_state.page = page
    else:
        st.session_state.page = "home"


# -----------------------------
# 왼쪽 메뉴
# -----------------------------
with st.sidebar:
    st.markdown("## 🏫 우리학교 알리미")
    st.caption("새로운 학교생활을 위한 안내서")
    st.divider()

    for key, label in PAGES.items():
        if st.button(label, key=f"nav_{key}"):
            go_to(key)
            st.rerun()

    st.divider()
    st.caption("학교별 세부 규칙은 담임 선생님과 학교 공지를 확인하세요.")

# -----------------------------
# 공통 페이지 제목
# -----------------------------
st.markdown(
    '<div class="main-title">우리학교 알리미 🏫</div>',
    unsafe_allow_html=True,
)

st.markdown(
    '<div class="sub-title">새로운 학교생활, 어렵지 않게 시작하기!</div>',
    unsafe_allow_html=True,
)

# -----------------------------
# 메인 페이지
# -----------------------------
if st.session_state.page == "home":
    st.markdown(
        """
        <div class="welcome-box">
            <h2>우리학교 생활이 처음이라면?</h2>
            <p>
                수업부터 과제까지, 학교생활에 필요한 정보를<br>
                쉽고 빠르게 확인해 보세요.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("📌 무엇이 궁금한가요?")
    st.write("아래 버튼을 눌러 원하는 안내를 확인하세요.")

    col1, col2 = st.columns(2)

    with col1:
        if st.button("📚 수업 안내\n수업 방식과 준비물", key="home_class"):
            go_to("class")
            st.rerun()

        if st.button("🏫 학교생활 안내\n일과와 기본 규칙", key="home_life"):
            go_to("life")
            st.rerun()

    with col2:
        if st.button("📝 과제 안내\n작성과 제출 방법", key="home_assignment"):
            go_to("assignment")
            st.rerun()

        if st.button("✅ 적응 체크리스트\n준비할 일 확인", key="home_checklist"):
            go_to("checklist")
            st.rerun()

    st.divider()
    st.info(
        "💡 처음에는 모든 것이 낯설 수 있어요. "
        "궁금한 점은 선생님께 질문하고 하나씩 익혀 봐요!"
    )

# -----------------------------
# 수업 안내
# -----------------------------
elif st.session_state.page == "class":
    st.header("📚 수업 안내")
    st.write("수업을 원활하게 듣기 위해 다음 내용을 확인하세요.")

    with st.container(border=True):
        st.subheader("수업 전 준비")
        st.markdown(
            """
            - 시간표를 확인하고 교과서를 준비해요.
            - 필기구와 필요한 학습 자료를 챙겨요.
            - 수업 시작 전에 자리에 앉아 준비해요.
            """
        )

    with st.container(border=True):
        st.subheader("수업 중 지켜야 할 점")
        st.markdown(
            """
            - 선생님의 설명을 집중해서 들어요.
            - 모르는 내용은 질문해요.
            - 발표와 모둠 활동에 적극적으로 참여해요.
            - 수행평가 기준과 제출 일정을 확인해요.
            """
        )

    with st.container(border=True):
        st.subheader("수업 후 확인")
        st.markdown(
            """
            - 배운 내용을 간단하게 복습해요.
            - 다음 수업 준비물을 확인해요.
            - 학교에서 안내한 학습 자료를 확인해요.
            """
        )

# -----------------------------
# 과제 안내
# -----------------------------
elif st.session_state.page == "assignment":
    st.header("📝 과제 안내")
    st.write("과제를 빠뜨리지 않고 제출하는 방법을 알아봐요.")

    st.subheader("과제 제출 5단계")

    steps = [
        "과제 내용과 평가 기준 확인하기",
        "제출 기한과 제출 장소 확인하기",
        "안내된 형식에 맞춰 과제 작성하기",
        "이름, 학번 등 필요한 정보 확인하기",
        "제출 후 정상적으로 제출되었는지 확인하기",
    ]

    for i, step in enumerate(steps, start=1):
        st.markdown(f"**{i}.** {step}")

    st.divider()
    st.subheader("📌 꼭 기억하세요!")
    st.warning(
        "과목마다 제출 방식이 다를 수 있어요. "
        "온라인 제출, 인쇄물 제출 등 선생님의 안내를 먼저 확인하세요."
    )

    st.subheader("과제 제출 전 체크")
    assignment_checks = [
        "과제 내용을 모두 작성했어요.",
        "맞춤법과 자료 출처를 확인했어요.",
        "파일이나 제출물을 준비했어요.",
        "제출 기한을 확인했어요.",
    ]

    for i, item in enumerate(assignment_checks):
        st.checkbox(item, key=f"assignment_check_{i}")

# -----------------------------
# 학교생활 안내
# -----------------------------
elif st.session_state.page == "life":
    st.header("🏫 학교생활 안내")
    st.write("학교에서의 하루를 미리 알아봐요.")

    with st.expander("🕒 학교 일과", expanded=True):
        st.markdown(
            """
            1. 등교 후 시간표와 공지 확인
            2. 정해진 시간에 맞춰 수업 참여
            3. 쉬는 시간에 다음 수업 준비
            4. 점심시간 및 학교 활동 참여
            5. 하교 전 과제와 준비물 확인
            """
        )
        st.caption(
            "※ 실제 등교 시간과 수업 시간은 학교 시간표를 확인하세요."
        )

    with st.expander("🤝 친구 및 선생님과 지내기"):
        st.markdown(
            """
            - 먼저 인사하고 서로 존중해요.
            - 친구의 의견을 잘 듣고 배려해요.
            - 어려운 일이 있으면 선생님께 도움을 요청해요.
            - 다른 사람의 물건과 개인정보를 존중해요.
            """
        )

    with st.expander("📢 공지 확인하기"):
        st.markdown(
            """
            - 학교 게시판과 공식 알림을 확인해요.
            - 수행평가 일정과 준비물을 기록해요.
            - 변경된 일정이 있는지 확인해요.
            - 정확하지 않은 정보는 선생님께 물어봐요.
            """
        )

# -----------------------------
# 적응 체크리스트
# -----------------------------
elif st.session_state.page == "checklist":
    st.header("✅ 학교 적응 체크리스트")
    st.write("완료한 항목을 체크하면서 하나씩 적응해 봐요!")

    checklist_items = [
        "학교 시간표를 확인했어요.",
        "교실과 주요 시설의 위치를 알아봤어요.",
        "교과서와 준비물을 확인했어요.",
        "학교 공지 확인 방법을 알아봤어요.",
        "과제 제출 방법을 확인했어요.",
        "수행평가 일정을 기록했어요.",
        "궁금한 점을 질문할 선생님을 알아봤어요.",
    ]

    for i, item in enumerate(checklist_items):
        st.checkbox(
            item,
            key=f"adapt_{i}",
            value=st.session_state.checked_items.get(item, False),
            on_change=lambda item=item, i=i: st.session_state.checked_items.update(
                {item: st.session_state.get(f"adapt_{i}", False)}
            ),
        )

    completed = sum(
        bool(st.session_state.checked_items.get(item, False))
        for item in checklist_items
    )
    total = len(checklist_items)

    st.divider()
    st.subheader(f"진행 상황: {completed} / {total}")
    st.progress(completed / total if total else 0)

    if completed == total:
        st.success("모든 항목을 확인했어요! 새로운 학교생활을 응원해요 🎉")
    else:
        st.info("천천히 확인해도 괜찮아요. 하나씩 완료해 봐요.")

    if st.button("체크리스트 초기화", key="reset_checklist"):
        for i in range(total):
            st.session_state.checked_items[checklist_items[i]] = False
            st.session_state[f"adapt_{i}"] = False
        st.rerun()

# -----------------------------
# 잘못된 페이지 값 방어
# -----------------------------
else:
    st.session_state.page = "home"
    st.rerun()

# -----------------------------
# 하단 공통 메뉴
# -----------------------------
st.divider()

if st.session_state.page != "home":
    if st.button("🏠 메인 페이지로 돌아가기", key="back_home"):
        go_to("home")
        st.rerun()

st.caption("우리학교 알리미 | 더 편리한 학교생활을 위한 안내")
