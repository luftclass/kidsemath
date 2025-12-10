import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정 (넓은 화면 사용)
# ---------------------------
st.set_page_config(page_title="1학년 수학 퀴즈왕", page_icon="👑", layout="wide")

# ---------------------------
# 2. CSS 스타일 (중앙 정렬 + 꾸미기)
# ---------------------------
st.markdown("""
<style>
/* 폰트 적용 */
.block-container {
    font-family: 'Gamja Flower', sans-serif;
}

/* 제목 중앙 정렬 */
h1 { text-align: center !important; color: #FF6F00; }

/* 문제 텍스트 스타일 */
.big-font {
    font-size: 70px !important;
    font-weight: bold;
    color: #1565C0;
    text-align: center;
    margin: 20px 0;
    background-color: #E3F2FD;
    border-radius: 20px;
    padding: 30px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}

/* ✅✅✅ [핵심] 보기 버튼 완벽 중앙 정렬 ✅✅✅ */
div.row-widget.stRadio {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    width: 100% !important;
}

div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    gap: 30px !important; /* 보기 사이 간격 */
    width: 100% !important;
}

/* 보기 텍스트 크기 */
div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-size: 32px !important;
    font-weight: bold;
}

/* 정답 메시지 */
.success-msg {
    font-size: 35px;
    font-weight: bold;
    color: #2E7D32;
    text-align: center;
    margin-bottom: 20px;
    animation: bounce 1s infinite;
}

/* 스티커 박스 */
.sticker-box {
    font-size: 30px;
    text-align: center;
    border: 3px dashed #FFCA28;
    border-radius: 15px;
    padding: 15px;
    background-color: #FFF8E1;
    min-height: 100px;
}

/* 점수 표시 */
.score-display {
    font-size: 40px;
    font-weight: bold;
    color: #D32F2F;
    text-align: center;
    margin: 15px 0;
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
if 'solved' not in st.session_state: st.session_state.solved = False # 정답 맞춤 여부 (잠금용)

# ---------------------------
# 4. 효과음 설정 (제공해주신 링크)
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
# 5. 함수 정의
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
        if n1 < n2: n1, n2 = n2, n1
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
    st.session_state.solved = False # 문제 새로 내면 잠금 해제

def show_ceremony():
    # 움직이는 GIF 이미지들
    gifs = [
        "https://media.giphy.com/media/nNxT5qXR02FOM/giphy.gif",
        "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif",
        "https://media.giphy.com/media/l0HlFTxCJqK7s21pK/giphy.gif",
        "https://media.giphy.com/media/TdfyKrN7HGTIY/giphy.gif"
    ]
    messages = ["천재가 나타났다!", "우와! 대단해요!", "정답입니다! 최고!", "수학왕이 될 자격이 있어요!"]
    
    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(random.choice(gifs), width=300)

# ---------------------------
# 6. 화면 구성 (사이드바 + 메인)
# ---------------------------

# === 사이드바: 점수 & 스티커 판 ===
with st.sidebar:
    st.header(f"📒 점수: {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    
    # 레벨업 게이지
    progress = (st.session_state.step % 5) / 5
    if st.session_state.step % 5 == 0 and st.session_state.step != 0: progress = 1.0
    st.write("🚀 다음 레벨까지:")
    st.progress(progress)
    
    st.divider()
    st.subheader("🏆 나의 칭찬 스티커")
    
    # 스티커 모음판
    with st.container():
        stickers_html = "<div class='sticker-box'>" + " ".join(st.session_state.stickers) + "</div>"
        st.markdown(stickers_html, unsafe_allow_html=True)
        if not st.session_state.stickers:
            st.info("문제를 맞춰서 스티커를 모아보세요!")

# === 메인 화면 ===
st.title("🎓 1학년 수학 퀴즈왕")

if not st.session_state.problem_generated:
    generate_problem()

# 문제 출력
op_display = "×" if st.session_state.operator == '*' else st.session_state.operator
quiz_text = f"{st.session_state.num1} {op_display} {st.session_state.num2} = ❓"
st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

# -----------------------------------------------
# ✅ 문제 풀이 폼 (정답 맞추면 비활성화 기능 포함)
# -----------------------------------------------
with st.form("quiz_form"):
    # solved가 True면 선택 못하게 막음 (disabled)
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True,
        label_visibility="collapsed",
        disabled=st.session_state.solved 
    )

    st.write("") # 간격 띄우기

    # 정답 버튼도 비활성화
    submitted = st.form_submit_button(
        "🚀 정답 확인하기", 
        use_container_width=True,
        disabled=st.session_state.solved
    )

    if submitted:
        st.session_state.is_checked = True
        
        if user_choice == st.session_state.answer:
            # 정답 처리
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True # 잠금 걸기
                st.session_state.stickers.append(random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "⚽"]))
                st.audio(random.choice(CORRECT_SOUNDS), autoplay=True)
                st.rerun() # 즉시 화면 새로고침하여 잠금 적용
        else:
            # 오답 처리
            st.session_state.solved = False
            st.audio(random.choice(WRONG_SOUNDS), autoplay=True)

# ---------------------------
# 7. 결과 및 다음 문제 버튼
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()
        
        # 다음 문제 버튼 (초록색 강조)
        if st.button("➡️ 다음 문제 도전! (클릭)", type="primary", use_container_width=True):
            st.session_state.step += 1
            
            # 5문제마다 레벨업
            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.snow()
                st.toast(f"🎉 {st.session_state.level}단계로 레벨업!")
            
            st.session_state.problem_generated = False
            st.session_state.is_checked = False
            st.session_state.solved = False
            st.rerun()
    else:
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
        if st.button("💡 힌트 보기"):
             st.info(f"정답은 {st.session_state.answer} 근처에 있어요!")
