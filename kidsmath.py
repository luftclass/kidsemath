import streamlit as st
import random

# ---------------------------
# 1. 페이지 설정
# ---------------------------
st.set_page_config(page_title="초1 수학 퀴즈왕", page_icon="👑", layout="wide") # wide 모드로 변경

# ---------------------------
# 2. CSS 스타일
# ---------------------------
st.markdown("""
<style>
/* 전체 폰트 및 정렬 */
.block-container { font-family: 'Gamja Flower', sans-serif; }
h1 { text-align: center; color: #FF6F00; }
.big-font { font-size: 70px !important; font-weight: bold; color: #1565C0; text-align: center; margin: 20px 0; background-color: #E3F2FD; border-radius: 20px; padding: 20px;}

/* 라디오 버튼 스타일 */
div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p { font-size: 28px !important; }
div[role="radiogroup"] { justify-content: center; gap: 30px; }

/* 정답 메시지 */
.success-msg { font-size: 35px; font-weight: bold; color: #2E7D32; text-align: center; margin-bottom: 20px; animation: bounce 1s infinite; }

/* 칭찬 스티커 영역 */
.sticker-box { font-size: 30px; text-align: center; border: 2px dashed #FFCA28; border-radius: 10px; padding: 10px; background-color: #FFF8E1; }
</style>
""", unsafe_allow_html=True)

# ---------------------------
# 3. 세션 상태 초기화 (변수 설정)
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
# ✨ 새로 추가된 상태: 획득한 스티커 리스트
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

# ✨ 업그레이드된 축하 함수 (GIF 이미지 사용)
def show_ceremony():
    # 귀여운 GIF URL 모음
    gifs = [
        "https://media.giphy.com/media/nNxT5qXR02FOM/giphy.gif", # 춤추는 곰
        "https://media.giphy.com/media/11sBLVxNs7v6WA/giphy.gif", # 미니언즈 박수
        "https://media.giphy.com/media/l0HlFTxCJqK7s21pK/giphy.gif", # 피카츄
        "https://media.giphy.com/media/TdfyKrN7HGTIY/giphy.gif", # 배트맨 엄지척
        "https://media.giphy.com/media/3oz8xAFtqoOUUrsh7W/giphy.gif" # 아기 춤
    ]
    messages = ["천재가 나타났다!", "우와! 정말 대단해요!", "정답입니다! 최고!", "수학왕이 될 자격이 있어요!"]
    
    st.balloons()
    st.markdown(f"<div class='success-msg'>🎉 {random.choice(messages)}</div>", unsafe_allow_html=True)
    
    # 가운데 정렬을 위해 컬럼 사용
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.image(random.choice(gifs), width=300)

# ---------------------------
# 5. 메인 화면 구성
# ---------------------------

# === 사이드바: 칭찬 스티커 판 ===
with st.sidebar:
    st.header(f"📒 {st.session_state.score}점")
    st.write(f"현재 레벨: **{st.session_state.level} 단계**")
    
    # 레벨업 게이지 (5문제마다 레벨업하므로 5로 나눈 나머지 활용)
    progress = (st.session_state.step % 5) / 5
    if st.session_state.step % 5 == 0 and st.session_state.step != 0: progress = 1.0
    st.write("🚀 다음 레벨까지:")
    st.progress(progress)
    
    st.divider()
    st.subheader("🏆 나의 칭찬 스티커")
    st.write("문제를 맞추면 스티커가 모여요!")
    
    # 스티커 보여주기 (5개씩 줄바꿈)
    sticker_board = st.container()
    with sticker_board:
        stickers_html = "<div class='sticker-box'>" + " ".join(st.session_state.stickers) + "</div>"
        st.markdown(stickers_html, unsafe_allow_html=True)
        if len(st.session_state.stickers) == 0:
            st.info("아직 스티커가 없어요. 첫 문제를 풀어보세요!")

# === 메인 퀴즈 영역 ===
st.title("🎓 1학년 수학 퀴즈왕")

if not st.session_state.problem_generated:
    generate_problem()

# 문제 출력
op_display = "×" if st.session_state.operator == '*' else st.session_state.operator
quiz_text = f"{st.session_state.num1} {op_display} {st.session_state.num2} = ❓"
st.markdown(f'<div class="big-font">{quiz_text}</div>', unsafe_allow_html=True)

with st.form("quiz_form"):
    # 라디오 버튼을 가운데 정렬 느낌으로 표시
    user_choice = st.radio(
        "정답은 무엇일까요?",
        options=st.session_state.choices,
        horizontal=True
    )
    
    # 버튼 디자인을 위한 공백
    st.write("") 
    submitted = st.form_submit_button("🚀 정답 확인하기", use_container_width=True)

    if submitted:
        st.session_state.is_checked = True
        if user_choice == st.session_state.answer:
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True
                
                # ✨ 스티커 추가 로직 (랜덤 스티커)
                new_sticker = random.choice(["⭐", "🍎", "🍩", "🤖", "🦄", "🌈", "🍭", "⚽"])
                st.session_state.stickers.append(new_sticker)
        else:
            st.session_state.solved = False

# === 결과 처리 ===
if st.session_state.is_checked:
    if st.session_state.solved:
        show_ceremony()
        
        # 다음 문제 버튼 (초록색 강조)
        if st.button("➡️ 다음 문제 도전! (클릭)", type="primary", use_container_width=True):
            st.session_state.step += 1
            
            # 레벨업 체크
            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.snow() # 레벨업 하면 눈내리기 효과 추가
                st.toast(f"🎉 와우! {st.session_state.level}단계로 레벨업 했어요!")
            
            st.session_state.problem_generated = False
            st.session_state.is_checked = False
            st.session_state.solved = False
            st.rerun()
    else:
        st.error("땡! 😅 괜찮아요, 다시 한번 생각해볼까요?")
        # 오답일 때 힌트 버튼 보여주기
        if st.button("💡 힌트 보기"):
             st.info(f"정답은 {st.session_state.answer} 근처에 있어요!")
