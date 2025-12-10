import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정 (넓은 화면 사용)
# ---------------------------
st.set_page_config(page_title="1학년 수학 퀴즈왕", page_icon="👑", layout="wide")

# ---------------------------
# 2. CSS 스타일 (강력한 내부 요소 중앙 정렬)
# ---------------------------
st.markdown("""
<style>
    /* 1. 전체 페이지 폰트 및 기본 정렬 */
    .block-container {
        font-family: 'Gamja Flower', sans-serif;
        text-align: center;
        align-items: center;
        display: flex;
        flex-direction: column;
    }

    /* 2. 제목 스타일 */
    h1 { 
        text-align: center !important; 
        color: #FF6F00;
        width: 100%;
    }

    /* 3. 문제 텍스트 박스 */
    .big-font {
        font-size: 80px !important;
        font-weight: bold;
        color: #1565C0;
        text-align: center;
        margin: 20px auto; 
        background-color: #E3F2FD;
        border-radius: 20px;
        padding: 40px;
        box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
        width: 80%; 
    }

    /* ✅✅✅ [핵심 수정] 라디오 버튼 내부 그룹(Table 역할) 중앙 정렬 ✅✅✅ */
    
    /* 라디오 버튼 전체를 감싸는 가장 바깥 틀 */
    div[data-testid="stRadio"] {
        display: flex !important;
        justify-content: center !important;
        align-items: center !important;
        width: 100% !important;
        margin: 0 auto !important;
    }

    /* 라디오 버튼 알맹이들이 들어있는 내부 컨테이너 (여기가 중요!) */
    div[role="radiogroup"] {
        display: flex !important;
        justify-content: center !important; /* 가로 중앙 정렬 */
        align-items: center !important;     /* 세로 중앙 정렬 */
        width: 100% !important;             /* 전체 너비 사용 */
        gap: 40px !important;               /* 보기 사이 간격 넓히기 */
    }

    /* 보기 텍스트(라벨) 스타일 */
    div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
        font-size: 35px !important;
        font-weight: bold;
        display: block;
        margin: 0 auto;
    }

    /* 4. 폼(Form) 버튼 중앙 정렬 */
    div.stButton {
        display: flex;
        justify-content: center;
        width: 100%;
    }
    
    div.stButton > button {
        width: 50% !important; 
        font-size: 25px !important;
        padding: 10px 0 !important;
        border-radius: 15px !important;
        margin: 20px auto !important;
        display: block !important;
    }

    /* 5. 정답 메시지 */
    .success-msg {
        font-size: 40px;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 20px;
        animation: bounce 1s infinite;
    }

    /* 6. 스티커 박스 */
    .sticker-box {
        font-size: 30px;
        text-align: center;
        border: 3px dashed #FFCA28;
        border-radius: 15px;
        padding: 15px;
        background-color: #FFF8E1;
        min-height: 100px;
    }
    
    /* 7. 폼(Form) 자체를 중앙 정렬 */
    div[data-testid="stForm"] {
        display: flex;
        flex-direction: column;
        align-items: center; /* 폼 내부 요소들을 가운데로 모음 */
        width: 80%; 
        margin: 0 auto; 
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
# 4. 효과음 및 함수
# ---------------------------
CORRECT_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-4.mp3",
    "https://www.soundjay.com/buttons/sounds/button-10.mp3"
]
WRONG_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-3.mp3",
    "https://www.soundjay.com/buttons/sounds/fail-button-2.mp3"
]

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
    st.session_state.solved = False

def show_ceremony():
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
# 5. 화면 구성
# ---------------------------

# 사이드바
with st.sidebar:
    st.header(f"📒 점수: {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    progress = (st.session_state.step % 5) / 5
    if st.session_state.step % 5 == 0 and st.session_state.step != 0: progress = 1.0
    st.write("🚀 다음 레벨까지:")
    st.progress(progress)
    st.divider()
    st.subheader("🏆 나의 칭찬 스티커")
    stickers_html = "<div class='sticker-box'>" + " ".join(st.session_state.stickers) + "</div>"
    st.markdown(stickers_html, unsafe_allow_html=True)

# 메인 화면
st.title("🎓 1학년 수학 퀴즈왕")

if not st.session_state.problem_generated:
    generate_problem()

op_display = "×" if st.session_state.operator == '*' else st.session_state.operator
quiz_text = f"{st.session_state.num1} {op_display} {st.session_state.num2} = ❓"
st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# ✅ 폼 영역
# ---------------------------
with st.form("quiz_form"):
    
    # 여기서 라디오 버튼들이 중앙으로 올 것입니다.
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True, 
        label_visibility="collapsed",
        disabled=st.session_state.solved
    )

    st.write("") 

    submitted = st.form_submit_button(
        "🚀 정답 확인하기", 
        use_container_width=False, 
        disabled=st.session_state.solved
    )

    if submitted:
        st.session_state.is_checked = True
        
        if user_choice == st.session_state.answer:
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True
                st.session_state.stickers.append(random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "⚽"]))
                st.audio(random.choice(CORRECT_SOUNDS), autoplay=True)
                st.rerun()
        else:
            st.session_state.solved = False
            st.audio(random.choice(WRONG_SOUNDS), autoplay=True)

# 결과 화면
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()
        
        # 버튼 중앙 정렬을 위해 컬럼 활용
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
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
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
             if st.button("💡 힌트 보기", use_container_width=True):
                 st.info(f"정답은 {st.session_state.answer} 근처에 있어요!")
