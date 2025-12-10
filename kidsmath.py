import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정
# ---------------------------
st.set_page_config(page_title="덧뺄셈 두자리", page_icon="🔢", layout="centered")

# ✅ 자동 번역 차단
st.markdown("""
<meta name="google" content="notranslate">
<meta http-equiv="Content-Language" content="ko">
<style>
* { translate: no !important; }
html, body, div, span, p, h1, h2, h3, button { translate: no !important; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 2. CSS (모바일 고정 2x2)
# ---------------------------
st.markdown("""
<style>
.block-container {
    font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Arial, sans-serif;
    max-width: 430px;
    margin: 0 auto !important;
    padding: 0 10px !important;
}

h1.main-title {
    text-align: center !important;
    color: #FF6F00;
    font-size: 1.9rem !important;
    margin-bottom: 10px;
}
h2.sub-title {
    text-align: center !important;
    color: #888;
    font-size: 0.9rem !important;
    margin-top: 10px;
    margin-bottom: 0;
}

/* 문제 영역 */
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

/* 2x2 버튼 그리드 */
.choice-grid {
    display: grid !important;
    grid-template-columns: 1fr 1fr !important;
    gap: 12px !important;
}

/* 버튼 공통 */
.choice-btn {
    width: 100% !important;
    padding: 14px 10px !important;
    border-radius: 14px !important;
    font-size: 24px !important;
    font-weight: bold !important;
    border: none !important;
    box-shadow: 0 3px 0 rgba(0,0,0,0.1);
}

/* 보기별 색상 */
.choice-btn:nth-child(1) { background-color: #FFF9C4; box-shadow: 0 3px 0 #FDD835; }
.choice-btn:nth-child(2) { background-color: #FFE0F0; box-shadow: 0 3px 0 #FF80BF; }
.choice-btn:nth-child(3) { background-color: #D4F1F4; box-shadow: 0 3px 0 #75E6DA; }
.choice-btn:nth-child(4) { background-color: #E6E6FA; box-shadow: 0 3px 0 #9D9DFF; }

.success-msg {
    font-size: 22px;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
}
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
defaults = {
    'level': 1,
    'score': 0,
    'step': 1,
    'stickers': [],
    'problem_generated': False,
    'show_result': False,
    'solved': False,
    'selected': None
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ---------------------------
# 4. 난이도별 문제 생성
# ---------------------------
def get_range_by_level(level):
    base = 10 + (level - 1) * 10
    return base, base + 20

def generate_problem():
    n1_min, n1_max = get_range_by_level(st.session_state.level)
    op = random.choice(['+', '-'])
    n1 = random.randint(n1_min, n1_max)
    n2 = random.randint(1, 20)
    ans = n1 + n2 if op == '+' else n1 - n2
    choices = {ans}
    while len(choices) < 4:
        wrong = ans + random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
        if 0 <= wrong <= 100:
            choices.add(wrong)
    st.session_state.update({
        'num1': n1, 'num2': n2, 'operator': op,
        'answer': ans, 'choices': list(choices),
        'problem_generated': True, 'show_result': False,
        'solved': False, 'selected': None
    })

# ---------------------------
# 5. 보기 클릭 처리
# ---------------------------
def handle_click(selected):
    st.session_state.selected = selected
    st.session_state.show_result = True
    if selected == st.session_state.answer:
        st.session_state.solved = True
        st.session_state.score += 10
        st.session_state.stickers.append(random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "⚽"]))
        if st.session_state.score % 50 == 0:
            st.session_state.level += 1
    st.rerun()

# ---------------------------
# 6. 사이드바
# ---------------------------
with st.sidebar:
    st.header(f"📒 점수: {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    st.progress((st.session_state.step % 5) / 5)
    st.subheader("🏆 나의 칭찬 스티커")
    st.markdown(
        f"<div class='sticker-box'>{' '.join(st.session_state.stickers)}</div>",
        unsafe_allow_html=True
    )

# ---------------------------
# 7. 메인 화면
# ---------------------------
st.markdown("<h2 class='sub-title'>바보똥꾸돼지야 아빠가 만든</h2>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>덧뺄셈 두자리수</h1>", unsafe_allow_html=True)

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ❓"
st.markdown(f"<div class='big-font'>{quiz_text}</div>", unsafe_allow_html=True)

# ---------------------------
# 8. 보기 2x2 고정
# ---------------------------
if not st.session_state.show_result:
    st.markdown("<div class='choice-grid'>", unsafe_allow_html=True)
    for choice in st.session_state.choices:
        if st.button(str(choice), key=f"btn_{choice}", use_container_width=True):
            handle_click(choice)
    st.markdown("</div>", unsafe_allow_html=True)

# ---------------------------
# 9. 결과 처리
# ---------------------------
if st.session_state.show_result:
    if st.session_state.solved:
        st.balloons()
        st.markdown("<div class='success-msg'>🎉 정답입니다!</div>", unsafe_allow_html=True)
        if st.button("➡️ 다음 문제 도전!", use_container_width=True):
            st.session_state.step += 1
            st.session_state.problem_generated = False
            st.session_state.show_result = False
            st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
        if st.button("🔄 다시 풀어보기", use_container_width=True):
            st.session_state.show_result = False
            st.session_state.selected = None
            st.rerun()
