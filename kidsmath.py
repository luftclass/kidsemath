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
# 2. CSS 스타일 (✅ 시스템 기본 폰트 + S25+ 최적화)
# ---------------------------
st.markdown("""
<style>

html, body {
    translate: no;
}

/* ✅ 시스템 기본 폰트 (최고속 로딩) */
.block-container {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    max-width: 430px;
    margin: 0 auto !important;
    padding-left: 10px !important;
    padding-right: 10px !important;
}

/* 서브 타이틀 */
h2.sub-title {
    text-align: center !important;
    color: #888;
    font-size: 0.9rem !important;
    margin-top: 10px;
    margin-bottom: 0;
}

/* 메인 타이틀 */
h1.main-title {
    text-align: center !important;
    color: #FF6F00;
    font-size: 1.9rem !important;
    margin-bottom: 10px;
}

/* 문제 박스 */
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

/* 보기 카드 */
div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 10px !important;
    width: 100% !important;
    flex-wrap: wrap !important;
}

div[class*="stRadio"] label {
    background-color: #FFF9C4 !important;
    border: 2px solid #FFF176 !important;
    padding: 12px 20px !important;
    border-radius: 14px !important;
    box-shadow: 0 3px 0 #FDD835 !important;
}

div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-size: 20px !important;
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
# 9. 문제 폼
# ---------------------------
with st.form("quiz_form"):
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True, 
        label_visibility="collapsed",
        disabled=st.session_state.solved
    )

    submitted = st.form_submit_button(
        "🚀 정답 확인하기", 
        use_container_width=True, 
        disabled=st.session_state.solved
    )

    if submitted:
        st.session_state.is_checked = True
        
        if user_choice == st.session_state.answer:
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
