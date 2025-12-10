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

/* 전체 페이지 중앙 정렬 */
.block-container {
    display: flex;
    flex-direction: column;
    align-items: center;
    text-align: center;
}

/* 제목 중앙 */
h1 {
    text-align: center !important;
}

/* 문제 텍스트 */
.big-font {
    font-size: 60px !important;
    font-weight: bold;
    color: #1E88E5;
    margin: 30px 0;
    line-height: 1.4;
    text-align: center;
}

/* ✅✅✅ 라디오 전체 줄을 "화면 기준" 중앙으로 */
div[data-testid="stRadio"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}

/* ✅✅✅ 라디오 버튼 그룹 자체 중앙 */
div[data-testid="stRadio"] > div {
    justify-content: center !important;
}

/* ✅✅✅ 보기 버튼 가로 배열 */
div.row-widget.stRadio > div {
    flex-direction: row !important;
    justify-content: center !important;
    gap: 30px !important;
}

/* 보기 숫자 폰트 확대 */
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
    font-size: 30px !important;
    text-align: center;
}

/* 라디오 동그라미 크기 확대 */
div[class*="stRadio"] div[role="radiogroup"] > label > div:first-child {
    transform: scale(2.0);
}

/* 보기 버튼 스타일 */
div[class*="stRadio"] label {
    background: #f5f7ff;
    padding: 10px 20px;
    border-radius: 12px;
}

/* 버튼 중앙 정렬 */
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

/* 성공 메시지 */
.success-msg {
    font-size: 28px;
    font-weight: bold;
    color: #2E7D32;
    margin: 20px 0;
    text-align: center;
}

/* ✅ 점수 크게 표시 */
.score-display {
    font-size: 40px;
    font-weight: bold;
    color: #D32F2F;
    margin: 15px 0;
    text-align: center;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# 세션 상태 초기화
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


# ---------------------------
# 문제 생성 함수 (난이도별)
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
# 정답 효과
# ---------------------------
def show_ceremony():
    animals = ["🐶", "🐱", "🐰", "🐼", "🐨", "🐯", "🦁", "🐧", "🦄"]
    messages = ["대단해요!", "참 잘했어요!", "멋져요!", "천재예요!", "정답입니다!", "최고예요!"]

    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    st.markdown(
        f"<div style='font-size:120px;line-height:1.2;text-align:center'>{random.choice(animals)}</div>",
        unsafe_allow_html=True
    )


# ---------------------------
# 메인 화면
# ---------------------------
st.title("🎓 1학년 수학 퀴즈")

st.markdown(f"**현재 단계 : {st.session_state.level}**")
st.markdown(f"<div class='score-display'>현재 점수 : {st.session_state.score}점</div>", unsafe_allow_html=True)

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?"
st.markdown(f'<div class="big-font">❓ 문제<br>{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# 문제 보기
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
        else:
            st.session_state.correct = False


# ---------------------------
# 결과 표시
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.correct:
        show_ceremony()

        st.markdown(f"<div class='score-display'>현재 점수 : {st.session_state.score}점</div>", unsafe_allow_html=True)

        if st.button("➡️ 다음 문제"):
            st.session_state.step += 1

            # ✅ 5문제마다 레벨 업
            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.success(f"🎯 {st.session_state.level}단계로 올라갔어요!")

            st.session_state.problem_generated = False
            st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
