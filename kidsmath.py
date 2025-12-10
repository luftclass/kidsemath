import streamlit as st
import random

# ---------------------------
# 페이지 설정
# ---------------------------
st.set_page_config(page_title="1학년 수학 퀴즈", page_icon="🎓", layout="centered")

# ---------------------------
# ✅ CSS (전체 센터 정렬 + 점수 확대 + 보기 완전 중앙 정렬)
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
    line-height: 1.4;
    text-align: center;
}

/* ✅ 보기 완전 중앙 정렬 */
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

/* 버튼 */
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
div.stButton > button:first-child:hover {
    background-color: #E64A19;
}

/* 점수 */
.score-display {
    font-size: 40px;
    font-weight: bold;
    color: #D32F2F;
    margin: 15px 0;
    text-align: center;
}

/* 성공 메시지 */
.success-msg {
    font-size: 28px;
    font-weight: bold;
    color: #2E7D32;
    margin: 20px 0;
    text-align: center;
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

# ---------------------------
# ✅ 문제 생성 (난이도별)
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

# ---------------------------
# ✅ GIF + 세레모니
# ---------------------------
GIFS = [
    "https://media.giphy.com/media/l0MYt5jPR6QX5pnqM/giphy.gif",
    "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif",
    "https://media.giphy.com/media/3oriO0OEd9QIDdllqo/giphy.gif"
]

def show_ceremony():
    st.balloons()
    st.markdown("<div class='success-msg'>🎉 정답이에요!</div>", unsafe_allow_html=True)
    st.image(random.choice(GIFS), width=250)

# ---------------------------
# ✅ 사이드바 스티커판
# ---------------------------
st.sidebar.title("📒 나의 칭찬 스티커판")
if len(st.session_state.stickers) == 0:
    st.sidebar.write("아직 스티커가 없어요!")
else:
    st.sidebar.write(" ".join(st.session_state.stickers))

# ---------------------------
# ✅ 메인 화면
# ---------------------------
st.title("🎓 1학년 수학 퀴즈")

st.markdown(f"**현재 단계 : {st.session_state.level}**")
st.markdown(f"<div class='score-display'>현재 점수 : {st.session_state.score}점</div>", unsafe_allow_html=True)

# ✅ 레벨업 게이지 (5문제 기준)
progress = (st.session_state.step % 5) / 5
st.progress(progress, text="🎯 다음 레벨까지")

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?"
st.markdown(f'<div class="big-font">❓ 문제<br>{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# ✅ 문제 보기
# ---------------------------
with st.form("quiz_form"):
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True,
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button("정답 확인하기")

    if submitted:
        st.session_state.is_checked = True

        if user_choice == st.session_state.answer:
            st.session_state.score += 10
            st.session_state.correct = True
            st.session_state.stickers.append("⭐")
        else:
            st.session_state.correct = False

# ---------------------------
# ✅ 결과 처리
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.correct:
        show_ceremony()

        if st.button("➡️ 다음 문제"):
            st.session_state.step += 1

            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.success(f"🎯 {st.session_state.level}단계로 올라갔어요!")

            st.session_state.problem_generated = False
            st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
