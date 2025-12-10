import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정
# ---------------------------
st.set_page_config(page_title="초1 수학 퀴즈왕", page_icon="👑", layout="wide")

# ---------------------------
# 2. CSS 스타일 (중앙 정렬 강화)
# ---------------------------
st.markdown("""
<style>
/* 전체 폰트 및 페이지 중앙 정렬 */
.block-container { 
    font-family: 'Gamja Flower', sans-serif; 
    max-width: 800px; /* 너무 넓어지지 않게 제한 */
    padding-top: 2rem;
}

h1 { text-align: center; color: #FF6F00; }

/* 문제 텍스트 스타일 */
.big-font { 
    font-size: 70px !important; 
    font-weight: bold; 
    color: #1565C0; 
    text-align: center; 
    margin: 20px 0; 
    background-color: #E3F2FD; 
    border-radius: 20px; 
    padding: 20px;
}

/* ✅✅✅ [핵심] 라디오 버튼 완벽 중앙 정렬 ✅✅✅ */
div.row-widget.stRadio {
    display: flex;
    justify-content: center;
    align-items: center;
    width: 100%;
}

div[role="radiogroup"] {
    display: flex;
    flex-direction: row;
    justify-content: center;
    gap: 20px; /* 보기 사이 간격 */
    width: 100%;
}

/* 라디오 버튼 텍스트 크기 */
div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-size: 30px !important;
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

/* 칭찬 스티커 영역 */
.sticker-box { 
    font-size: 30px; 
    text-align: center; 
    border: 2px dashed #FFCA28; 
    border-radius: 10px; 
    padding: 10px; 
    background-color: #FFF8E1; 
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 3. 세션 상태 초기화
# ---------------------------
if 'level' not in st.session_state: st.session_state.level = 1
if 'score' not in st.session_state: st.session_state.score = 0
if 'num1' not in st.session_state: st.session_state.num1 = 0
if 'num2' not in st.session_state: st.session_state.num2 = 0
if 'operator' not in st.session_state: st.session_state.operator = '+'
if 'answer' not in st.session_state: st.session_state.answer = 0
if 'choices' not in st.session_state: st.session_state.choices = []
if 'problem_generated' not in st.session_state: st.session_state.problem_generated = False
if 'solved' not in st.session_state: st.session_state.solved = False
if 'is_checked' not in st.session_state: st.session_state.is_checked = False
if 'step' not in st.session_state: st.session_state.step = 1
if 'stickers' not in st.session_state: st.session_state.stickers = []

# ---------------------------
# 4. 함수 정의
# ---------------------------
def generate_problem():
    level = st.session_state.level
    if level == 1:
        n1, n2 = random.randint(1, 9), random.randint(1, 9)
        ops = ['+', '-']
    elif level == 2:
        n1, n2 = random.randint(10, 20), random.randint(1, 10)
        ops = ['+', '-']
    else:
        n1, n2 = random.randint(10, 50), random.randint(5, 20)
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
        wrong = ans + random.choice([-5, -2, -1, 1, 2, 5])
        if wrong >= 0 and wrong != ans:
            choices.add(wrong)

    st.session_state.num1 = n1
    st.session_state.num2 = n2
    st.session_state.operator = op
    st.session_state.answer = ans
    st.session_state.choices = list(choices)
    random.shuffle(st.session_state.choices)
    st.session_state.problem_generated = True
    st.session_state.solved = False
    st.session_state.is_checked = False

def show_ceremony():
    gifs = [
        "https://media.giphy.com/media/nNxT5qXR02FOM/giphy.gif",
        "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif",
        "https://media.giphy.com/media/l0HlFTxCJqK7s21pK/giphy.gif",
        "https://media.giphy.com/media/TdfyKrN7HGTIY/giphy.gif",
        "https://media.giphy.com/media/3oz8xAFtqoOUUrsh7W/giphy.gif"
    ]
    messages = ["천재가 나타났다!", "우와! 정말 대단해요!", "정답입니다! 최고!", "수학왕이 될 자격이 있어요!"]
    
    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(random.choice(gifs), width=300)

# ---------------------------
# 5. 메인 화면 구성
# ---------------------------

# === 사이드바 ===
with st.sidebar:
    st.header(f"📒 {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    
    progress = (st.session_state.step % 5) / 5
    if st.session_state.step % 5 == 0 and st.session_state.step != 0: progress = 1.0
    st.write("🚀 다음 레벨까지:")
    st.progress(progress)
    
    st.divider()
    st.subheader("🏆 나의 칭찬 스티커")
    sticker_board = st.container()
    with sticker_board:
        stickers_html = "<div class='sticker-box'>" + " ".join(st.session_state.stickers) + "</div>"
        st.markdown(stickers_html, unsafe_allow_html=True)
        if len(st.session_state.stickers) == 0:
            st.info("아직 스티커가 없어요.")

# === 메인 퀴즈 영역 ===
st.title("🎓 1학년 수학 퀴즈왕")

if not st.session_state.problem_generated:
    generate_problem()

op_display = "×" if st.session_state.operator == '*' else st.session_state.operator
quiz_text = f"{st.session_state.num1} {op_display} {st.session_state.num2} = ❓"
st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

# -------------------------------------------------------
# ✅ 문제 풀이 Form (비활성화 로직 적용)
# -------------------------------------------------------
with st.form("quiz_form"):
    # solved가 True면(정답 맞춤) disabled=True가 되어 선택 불가
    user_choice = st.radio(
        "정답은 무엇일까요?",
        options=st.session_state.choices,
        horizontal=True,
        disabled=st.session_state.solved  # 👈 여기가 핵심!
    )
    
    st.write("") 
    
    # 버튼도 정답 맞추면 비활성화
    submitted = st.form_submit_button(
        "🚀 정답 확인하기", 
        use_container_width=True,
        disabled=st.session_state.solved # 👈 여기도 핵심!
    )

    if submitted:
        st.session_state.is_checked = True
        if user_choice == st.session_state.answer:
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True
                new_sticker = random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "🌈", "🍭", "⚽"])
                st.session_state.stickers.append(new_sticker)
                st.rerun() # 상태 업데이트 후 즉시 리런하여 UI 비활성화 적용
        else:
            st.session_state.solved = False

# === 결과 처리 ===
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()
        
        # 다음 문제 버튼
        if st.button("➡️ 다음 문제 도전! (클릭)", type="primary", use_container_width=True):
            st.session_state.step += 1
            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.snow()
                st.toast(f"🎉 {st.session_state.level}단계로 레벨업!")
            
            st.session_state.problem_generated = False
            st.session_state.is_checked = False
            st.session_state.solved = False
            st.rerun()
    else:
        st.error("땡! 😅 괜찮아요, 다시 한번 생각해볼까요?")
        if st.button("💡 힌트 보기"):
             st.info(f"정답은 {st.session_state.answer} 근처에 있어요!")
