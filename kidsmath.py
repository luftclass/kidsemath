import streamlit as st
import random

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="1학년 수학 퀴즈", page_icon="🎓", layout="centered")

# ---------------------------
# ✅ CSS
# ---------------------------
st.markdown("""
<style>
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}
h1 { text-align: center !important; }

.big-font {
    font-size: 60px !important;
    font-weight: bold;
    color: #1E88E5;
    margin: 30px 0;
}

div[data-testid="stRadio"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}
div[data-testid="stRadio"] > div {
    justify-content: center !important;
}
div.row-widget.stRadio > div {
    flex-direction: row !important;
    justify-content: center !important;
    gap: 30px !important;
}
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 30px !important;
}
div[class*="stRadio"] div[role="radiogroup"] > label > div:first-child {
    transform: scale(2.0);
}
div[class*="stRadio"] label {
    background: #f5f7ff;
    padding: 10px 20px;
    border-radius: 12px;
}

div.stButton {
    display: flex;
    justify-content: center;
    margin-top: 20px;
}
div.stButton > button:first-child {
    font-size: 24px;
    padding: 12px 40px;
    border-radius: 15px;
    background-color: #FF5722;
    color: white;
    border: none;
}

.score-display {
    font-size: 40px;
    font-weight: bold;
    color: #D32F2F;
    margin: 15px 0;
}

.success-msg {
    font-size: 28px;
    font-weight: bold;
    color: #2E7D32;
    margin: 20px 0;
}

.center-box {
    display: flex;
    flex-direction: column;
    align-items: center;
    margin-top: 20px;
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# ✅ 세션 상태 초기화
# ---------------------------
if 'level' not in st.session_state:
    st.session_state.level = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'step' not in st.session_state:
    st.session_state.step = 1
if 'is_checked' not in st.session_state:
    st.session_state.is_checked = False
if 'problem_generated' not in st.session_state:
    st.session_state.problem_generated = False
if 'stickers' not in st.session_state:
    st.session_state.stickers = []
if 'correct' not in st.session_state:
    st.session_state.correct = False

# ---------------------------
# ✅ 사운드 목록
# ---------------------------
CORRECT_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-4.mp3",
    "https://www.soundjay.com/buttons/sounds/button-10.mp3",
    "https://www.soundjay.com/buttons/sounds/button-16.mp3"
]

WRONG_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-3.mp3",
    "https://www.soundjay.com/buttons/sounds/button-09.mp3",
    "https://www.soundjay.com/buttons/sounds/fail-button-2.mp3"
]

# ---------------------------
# ✅ 문제 생성
# ---------------------------
def generate_problem():
    level = st.session_state.level

    if level == 1:
        n1, n2 = random.randint(1, 9), random.randint(1, 9)
        ops = ['+', '-']
    elif level == 2:
        n1, n2 = random.randint(5, 20), random.randint(1, 15)
        ops = ['+', '-']
    else:
        n1, n2 = random.randint(10, 30), random.randint(1, 20)
        ops = ['+', '-', '*']

    op = random.choice(ops)

    if op == '-':
        if n1 < n2:
            n1, n2 = n2, n1
        ans = n1 - n2
    elif op == '+':
        ans = n1 + n2
    else:
        ans = n1 * n2

    choices = set([ans])
    while len(choices) < 3:
        wrong = ans + random.choice([-5, -3, -2, 2, 3, 5])
        if wrong >= 0 and wrong != ans:
            choices.add(wrong)

    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.operator = op
    st.session_state.answer = ans
    st.session_state.choices = list(choices)
    random.shuffle(st.session_state.choices)

    st.session_state.problem_generated = True
    st.session_state.is_checked = False
    st.session_state.correct = False

# ---------------------------
# ✅ 메인 화면
# ---------------------------
st.title("🎓 1학년 수학 퀴즈")

st.markdown(f"**현재 단계 : {st.session_state.level}**")
st.markdown(f"<div class='score-display'>현재 점수 : {st.session_state.score}점</div>", unsafe_allow_html=True)

progress = (st.session_state.step % 5) / 5
st.progress(progress, text="🎯 다음 레벨까지")

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?"
st.markdown(f'<div class="big-font">❓ 문제<br>{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# ✅ 문제 보기 + 버튼 (비활성화 적용)
# ---------------------------
with st.form("quiz_form"):
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True,
        label_visibility="collapsed",
        disabled=st.session_state.correct
    )

    submitted = st.form_submit_button(
        "정답 확인하기",
        disabled=st.session_state.correct
    )

    if submitted:
        st.session_state.is_checked = True

        if user_choice == st.session_state.answer:
            st.session_state.score += 10
            st.session_state.correct = True
            st.session_state.stickers.append("⭐")
            st.audio(random.choice(CORRECT_SOUNDS), autoplay=True)
        else:
            st.session_state.correct = False
            st.audio(random.choice(WRONG_SOUNDS), autoplay=True)

# ---------------------------
# ✅ 결과 처리
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.correct:
        st.markdown('<div class="center-box">', unsafe_allow_html=True)
        st.success("🎉 정답이에요!")
        st.markdown("</div>", unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)
        with col2:
            if st.button("➡️ 다음 문제"):
                st.session_state.step += 1

                if st.session_state.step % 5 == 0:
                    st.session_state.level = min(3, st.session_state.level + 1)
                    st.success(f"🎯 {st.session_state.level}단계로 올라갔어요!")

                st.session_state.problem_generated = False
                st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
