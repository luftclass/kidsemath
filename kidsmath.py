import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정 (모바일 최적)
# ---------------------------
st.set_page_config(
    page_title="덧뺄셈 두자리",
    page_icon="🔢",
    layout="centered"
)

# ✅ 자동 번역 완전 차단
st.markdown(
    """
    <meta name="google" content="notranslate">
    <meta http-equiv="Content-Language" content="ko">
    """,
    unsafe_allow_html=True
)

# ---------------------------
# 2. CSS 스타일 (시스템 기본 폰트 + 노란 박스 유지)
# ---------------------------
st.markdown("""
<style>

html, body {
    translate: no;
}

/* ✅ 시스템 기본 폰트 */
.block-container {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    max-width: 430px;
    margin: 0 auto !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
}

/* 제목 */
h2.sub-title {
    text-align: center !important;
    color: #888;
    font-size: 0.9rem !important;
    margin-top: 10px;
    margin-bottom: 0;
}
h1.main-title {
    text-align: center !important;
    color: #FF6F00;
    font-size: 1.9rem !important;
    margin-bottom: 10px;
}

/* 문제 */
.big-font {
    font-size: 38px !important;
    font-weight: bold;
    color: #1565C0;
    text-align: center;
    background-color: #E3F2FD;
    border-radius: 15px;
    padding: 18px;
    margin-bottom: 15px;
}

/* ✅ 보기 기본 = 노란 박스 유지 */
.choice-card {
    background-color: #FFF9C4;
    border: 2px solid #FFF176;
    padding: 14px 10px;
    border-radius: 14px;
    box-shadow: 0 3px 0 #FDD835;
    text-align: center;
    font-size: 20px;
    font-weight: bold;
}

/* 버튼 */
div.stButton > button {
    width: 100% !important;
    font-size: 18px !important;
    padding: 12px 0 !important;
    border-radius: 14px !important;
    background-color: #FF5722 !important;
    color: white !important;
    border: none !important;
}

/* 정답 메시지 */
.success-msg {
    font-size: 22px;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
}

/* 스티커 박스 */
.sticker-box {
    font-size: 18px;
    text-align: center;
    border: 2px dashed #FFCA28;
    border-radius: 12px;
    padding: 8px;
    background-color: #FFF8E1;
    min-height: 60px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# 3. 세션 상태 초기화
# ---------------------------
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'step' not in st.session_state: st.session_state.step = 1
if 'is_checked' not in st.session_state: st.session_state.is_checked = False
if 'problem_generated' not in st.session_state: st.session_state.problem_generated = False
if 'stickers' not in st.session_state: st.session_state.stickers = []
if 'solved' not in st.session_state: st.session_state.solved = False
if 'selected' not in st.session_state: st.session_state.selected = None

# ---------------------------
# 4. 사운드
# ---------------------------
CORRECT_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-3.mp3",
    "https://www.soundjay.com/human/sounds/applause-01.mp3",
    "https://www.soundjay.com/misc/sounds/magic-chime-01.mp3"
]
WRONG_SOUND_FIXED = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

def play_sound(url):
    st.markdown(f"""
    <audio autoplay="true" style="display:none;">
        <source src="{url}" type="audio/mp3">
    </audio>
    """, unsafe_allow_html=True)

# ---------------------------
# 5. 문제 생성
# ---------------------------
def generate_problem():
    ops = ['+', '-']
    op = random.choice(ops)
    n1 = random.randint(10, 30)
    n2 = random.randint(1, 20)

    ans = n1 + n2 if op == '+' else n1 - n2

    choices = set([ans])
    while len(choices) < 4:
        wrong = ans + random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        if 0 <= wrong <= 50 and wrong != ans:
            choices.add(wrong)

    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.operator = op
    st.session_state.answer = ans
    st.session_state.choices = list(choices)
    random.shuffle(st.session_state.choices)

    st.session_state.problem_generated = True
    st.session_state.is_checked = False
    st.session_state.solved = False
    st.session_state.selected = None

# ---------------------------
# 6. 세레모니
# ---------------------------
def show_ceremony():
    st.balloons()
    st.markdown("<div class='success-msg'>🎉 정답입니다!</div>", unsafe_allow_html=True)

# ---------------------------
# 7. 사이드바
# ---------------------------
with st.sidebar:
    st.header(f"📒 점수: {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    st.progress((st.session_state.step % 5) / 5)
    st.subheader("🏆 나의 칭찬 스티커")
    st.markdown(
        "<div class='sticker-box'>" + " ".join(st.session_state.stickers) + "</div>",
        unsafe_allow_html=True
    )

# ---------------------------
# 8. 메인 화면
# ---------------------------
st.markdown("<h2 class='sub-title'>바보똥꾸돼지야 아빠가 만든</h2>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>덧뺄셈 두자리수</h1>", unsafe_allow_html=True)

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ❓"
st.markdown(f"<div class='big-font'>{quiz_text}</div>", unsafe_allow_html=True)

# ---------------------------
# 9. ✅ 보기 2×2 배열 (노란 박스 유지)
# ---------------------------
with st.form("quiz_form"):
    row1 = st.columns(2)
    row2 = st.columns(2)

    choices = st.session_state.choices

    if row1[0].button(choices[0], use_container_width=True, disabled=st.session_state.solved):
        st.session_state.selected = choices[0]
    if row1[1].button(choices[1], use_container_width=True, disabled=st.session_state.solved):
        st.session_state.selected = choices[1]
    if row2[0].button(choices[2], use_container_width=True, disabled=st.session_state.solved):
        st.session_state.selected = choices[2]
    if row2[1].button(choices[3], use_container_width=True, disabled=st.session_state.solved):
        st.session_state.selected = choices[3]

    submitted = st.form_submit_button(
        "🚀 정답 확인하기",
        use_container_width=True,
        disabled=st.session_state.solved
    )

    if submitted and st.session_state.selected is not None:
        st.session_state.is_checked = True

        if st.session_state.selected == st.session_state.answer:
            st.session_state.score += 10
            st.session_state.solved = True
            st.session_state.stickers.append(random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "⚽"]))
            play_sound(random.choice(CORRECT_SOUNDS))
            st.rerun()
        else:
            play_sound(WRONG_SOUND_FIXED)

# ---------------------------
# 10. 결과 화면
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()

        if st.button("➡️ 다음 문제 도전!", use_container_width=True):
            st.session_state.step += 1
            st.session_state.problem_generated = False
            st.session_state.is_checked = False
            st.session_state.solved = False
            st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
