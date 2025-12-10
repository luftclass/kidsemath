import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정
# ---------------------------
st.set_page_config(page_title="덧뺄셈 두자리", page_icon="🔢", layout="wide")

# ---------------------------
# 2. CSS 스타일 (제목 두 줄 및 크기 조정)
# ---------------------------
st.markdown("""
<style>
/* 폰트 적용 */
.block-container {
    font-family: 'Gamja Flower', sans-serif;
}

/* 🟢 [수정] 메인 타이틀 (기존 제목) */
h1.main-title { 
    text-align: center !important; 
    color: #FF6F00; 
    margin-top: 5px;
    margin-bottom: 10px;
    font-size: 2.8rem !important; /* 기존 2.5rem에서 약간 확대하여 대비 강조 */
}

/* 🟢 [추가] 서브 타이틀 (새 문구) - 메인 타이틀보다 약 70% 작게 (0.8rem) */
h2.sub-title {
    text-align: center !important;
    color: #888888; /* 회색으로 부드럽게 */
    margin-bottom: 0px;
    font-size: 0.8rem !important; 
    font-weight: normal;
    padding-top: 10px;
}

/* 문제 박스 스타일 */
.big-font {
    font-size: 70px !important; 
    font-weight: bold;
    color: #1565C0;
    text-align: center;
    background-color: #E3F2FD;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}

/* ✅✅✅ 보기 버튼(카드) 스타일 ✅✅✅ */
div[role="radiogroup"] {
    display: flex !important;
    justify-content: center !important;
    align-items: center !important;
    gap: 15px !important; 
    width: 100% !important;
    flex-wrap: wrap !important; 
}

div[class*="stRadio"] label {
    background-color: #FFF9C4 !important; 
    border: 3px solid #FFF176 !important; 
    padding: 15px 30px !important; 
    border-radius: 20px !important; 
    cursor: pointer !important;
    transition: all 0.3s ease !important;
    margin-right: 0 !important; 
    box-shadow: 0 4px 0 #FDD835 !important;
    
    color: black !important;
}

div[class*="stRadio"] label:hover {
    transform: scale(1.05) !important; 
    background-color: #FFF59D !important;
}

div[class*="stRadio"] label[data-checked="true"] {
    background-color: #FFEB3B !important;
    border-color: #FBC02D !important;
    color: black !important; 
}

/* 텍스트 크기 및 색상 */
div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-size: 28px !important; 
    font-weight: bold;
    margin: 0 !important;
    color: black !important; 
}

/* 폼 제출 버튼 스타일 */
div.stButton > button {
    width: 100% !important;
    font-size: 22px !important; 
    padding: 12px 0 !important;
    border-radius: 15px !important;
    background-color: #FF5722 !important;
    color: white !important;
    border: none !important;
    box-shadow: 0 4px 0 #E64A19 !important; 
    margin-top: 20px !important;
}
div.stButton > button:hover {
    background-color: #F4511E !important;
    transform: translateY(2px); 
    box-shadow: 0 2px 0 #E64A19 !important;
}

/* 결과 메시지 */
.success-msg {
    font-size: 32px; 
    font-weight: bold; 
    color: #2E7D32; 
    text-align: center; 
    animation: bounce 1s infinite;
}

/* 스티커 박스 */
.sticker-box {
    font-size: 24px; 
    text-align: center; 
    border: 3px dashed #FFCA28; 
    border-radius: 15px; 
    padding: 10px; 
    background-color: #FFF8E1; 
    min-height: 80px;
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
# 4. 사운드 및 함수 설정
# ---------------------------
CORRECT_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-3.mp3", 
    "https://www.soundjay.com/human/sounds/applause-01.mp3", 
    "https://www.soundjay.com/misc/sounds/magic-chime-01.mp3" 
]
WRONG_SOUND_FIXED = "https://www.soundjay.com/buttons/sounds/button-10.mp3"

def play_sound(url):
    sound_html = f"""
    <audio autoplay="true" style="display:none;">
        <source src="{url}" type="audio/mp3">
    </audio>
    """
    st.markdown(sound_html, unsafe_allow_html=True)

def generate_problem():
    level = st.session_state.level
    ops = ['+', '-'] 
    op = random.choice(ops)

    if level == 1:
        if op == '+':
            n1 = random.randint(1, 5)
            n2 = random.randint(1, 5)
        else:
            n1 = random.randint(2, 9)
            n2 = random.randint(1, n1)
    elif level == 2:
        if op == '+':
            n1 = random.randint(5, 15)
            n2 = random.randint(2, 9)
            if n1 + n2 > 20: n1 = 20 - n2 
        else:
            n1 = random.randint(10, 20)
            n2 = random.randint(2, 9)
    else:
        if op == '+':
            n1 = random.randint(10, 25)
            n2 = random.randint(1, 30 - n1)
        else:
            n1 = random.randint(15, 30)
            n2 = random.randint(5, 15)

    if op == '+': ans = n1 + n2
    else: ans = n1 - n2

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

def show_ceremony():
    gifs = [
        "https://media.giphy.com/media/nNxT5qXR02FOM/giphy.gif",
        "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif",
        "https://media.giphy.com/media/l0HlFTxCJqK7s21pK/giphy.gif",
        "https://media.giphy.com/media/TdfyKrN7HGTIY/giphy.gif",
        "https://media.giphy.com/media/kxUhZ0Ubz8HQ4/giphy.gif",
        "https://media.giphy.com/media/26tOZ42Mg6pbTUPHW/giphy.gif",
        "https://media.giphy.com/media/Mc5WxJmFf8NBS/giphy.gif",
        "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif",
        "https://media.giphy.com/media/l46C93LNM33JJ1SMw/giphy.gif",
        "https://media.giphy.com/media/chzz1FQgqhytWRWbp3/giphy.gif"
    ]
    messages = ["천재가 나타났다!", "우와! 대단해요!", "정답입니다! 최고!", "수학왕이 될 자격이 있어요!", "오늘도 멋져요!"]
    
    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(random.choice(gifs), width=300)

# ---------------------------
# 6. 메인 화면 구성
# ---------------------------

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

# 🟢 [수정] 두 줄 제목 삽입
st.markdown("<h2 class='sub-title'>바보똥꾸돼지야 아빠가 만든</h2>", unsafe_allow_html=True)
st.markdown("<h1 class='main-title'>덧셈 뺄셈 두자리수</h1>", unsafe_allow_html=True)


if not st.session_state.problem_generated:
    generate_problem()

col_L, col_Main, col_R = st.columns([1, 2, 1])
with col_Main:
    quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ❓"
    st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# 폼 영역
# ---------------------------
with st.form("quiz_form"):
    c1, c2, c3 = st.columns([1, 4, 1]) 
    
    with c2:
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
            use_container_width=True, 
            disabled=st.session_state.solved
        )

    if submitted:
        st.session_state.is_checked = True
        
        if user_choice == st.session_state.answer:
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True
                st.session_state.stickers.append(random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "⚽", "🍭", "🦖"]))
                
                play_sound(random.choice(CORRECT_SOUNDS))
                st.rerun()
        else:
            st.session_state.solved = False
            play_sound(WRONG_SOUND_FIXED)

# ---------------------------
# 결과 화면
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()
        
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
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
            if st.button("💡 힌트 보기", use_container_width=True):
                 st.info(f"정답은 {st.session_state.answer} 근처에 있어요!")
