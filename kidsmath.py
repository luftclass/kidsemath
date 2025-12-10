import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정
# ---------------------------
st.set_page_config(page_title="1학년 수학 퀴즈왕", page_icon="👑", layout="wide")

# ---------------------------
# 2. CSS 스타일
# ---------------------------
st.markdown("""
<style>
/* 폰트 적용 */
.block-container {
    font-family: 'Gamja Flower', sans-serif;
}

/* 제목 스타일 */
h1 { 
    text-align: center !important; 
    color: #FF6F00; 
    margin-bottom: 10px;
    font-size: 2.5rem !important; 
}

/* 문제 박스 스타일 */
.big-font {
    font-size: 60px !important; 
    font-weight: bold;
    color: #1565C0;
    text-align: center;
    background-color: #E3F2FD;
    border-radius: 20px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0px 4px 6px rgba(0,0,0,0.1);
}

/* ✅✅✅ 보기 버튼(카드) 스타일 - 클릭 영역 확대 ✅✅✅ */
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

/* 텍스트 크기 */
div[class*="stRadio"] label div[data-testid="stMarkdownContainer"] p {
    font-size: 28px !important; 
    font-weight: bold;
    margin: 0 !important;
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
# 4. 효과음 설정 (교체됨)
# ---------------------------
CORRECT_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/button-3.mp3", # 띵동
    "https://www.soundjay.com/human/sounds/applause-01.mp3", # 박수
    "https://www.soundjay.com/misc/sounds/magic-chime-01.mp3" # 띠로링
]

# 🔊 작동 안 되는 사운드 제거 및 새 사운드 추가
WRONG_SOUNDS = [
    "https://www.soundjay.com/buttons/sounds/beep-02.mp3", # 삐!
    "https://www.soundjay.com/buttons/sounds/button-10.mp3", # 띡
    "https://www.soundjay.com/transportation/sounds/car-horn-01.mp3" # 빵! (재밌는 소리)
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
    while len(choices) < 4:
        wrong = ans + random.choice([-5, -3, -2, -1, 1, 2, 3, 5])
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
    # 🎉 GIF 이미지 대폭 추가!
    gifs = [
        "https://media.giphy.com/media/nNxT5qXR02FOM/giphy.gif", # 스폰지밥
        "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif", # 미니언즈 박수
        "https://media.giphy.com/media/l0HlFTxCJqK7s21pK/giphy.gif", # 인사이드 아웃 기쁨이
        "https://media.giphy.com/media/TdfyKrN7HGTIY/giphy.gif", # 배트맨 따봉
        "https://media.giphy.com/media/kxUhZ0Ubz8HQ4/giphy.gif", # 춤추는 펭귄
        "https://media.giphy.com/media/26tOZ42Mg6pbTUPHW/giphy.gif", # 폭죽 팡팡
        "https://media.giphy.com/media/Mc5WxJmFf8NBS/giphy.gif", # 춤추는 고양이
        "https://media.giphy.com/media/3o7abKhOpu0NwenH3O/giphy.gif", # 주토피아 나무늘보
        "https://media.giphy.com/media/l46C93LNM33JJ1SMw/giphy.gif", # 아기곰 댄스
        "https://media.giphy.com/media/chzz1FQgqhytWRWbp3/giphy.gif" # 피카츄 댄스
    ]
    messages = ["천재가 나타났다!", "우와! 대단해요!", "정답입니다! 최고!", "수학왕이 될 자격이 있어요!", "오늘도 멋져요!"]
    
    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        st.image(random.choice(gifs), width=300)

# ---------------------------
# 5. 메인 화면 구성
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

# 메인 타이틀
st.title("🎓 1학년 수학 퀴즈왕")

if not st.session_state.problem_generated:
    generate_problem()

# 문제 출력
col_L, col_Main, col_R = st.columns([1, 2, 1])
with col_Main:
    op_display = "×" if st.session_state.operator == '*' else st.session_state.operator
    quiz_text = f"{st.session_state.num1} {op_display} {st.session_state.num2} = ❓"
    st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

# ------------------------------------------------------------
# 폼 내부 중앙 정렬 (컬럼 사용)
# ------------------------------------------------------------
with st.form("quiz_form"):
    
    # 양쪽 여백을 줘서 가운데로 몰아넣기
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
                # ✅ 정답 소리 재생
                st.audio(random.choice(CORRECT_SOUNDS), autoplay=True)
                st.rerun()
        else:
            st.session_state.solved = False
            # ✅ 오답 소리 재생 (교체됨)
            st.audio(random.choice(WRONG_SOUNDS), autoplay=True)

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
