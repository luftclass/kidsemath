import streamlit as st
import random

# 페이지 기본 설정
st.set_page_config(page_title="초1 수학 퀴즈", page_icon="✏️")

# --- 스타일 설정 (글자 크기 키우기) ---
# 문제 폰트 30% 확대, 보기 선택란 50% 확대 등을 위한 CSS 코드입니다.
st.markdown("""
    <style>
    /* 문제 텍스트 스타일 */
    .big-font {
        font-size: 40px !important;
        font-weight: bold;
        color: #1E88E5;
        margin-bottom: 20px;
    }
    /* 라디오 버튼(보기) 텍스트 크기 키우기 */
    div[class*="stRadio"] > label > div[data-testid="stMarkdownContainer"] > p {
        font-size: 24px !important;
    }
    /* 라디오 버튼 동그라미 크기 키우기 */
    div[class*="stRadio"] div[role="radiogroup"] > label > div:first-child {
        transform: scale(1.5);
    }
    /* 정답 확인 버튼 스타일 */
    div.stButton > button:first-child {
        font-size: 20px;
        padding: 10px 24px;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("🎓 1학년 수학: 덧셈과 뺄셈")

# --- 세션 상태 초기화 ---
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.operator = '+'
    st.session_state.answer = 0
    st.session_state.choices = []
    st.session_state.problem_generated = False
    st.session_state.solved = False # 문제를 풀었는지 확인하는 변수

# --- 문제 생성 함수 ---
def generate_problem():
    n1 = random.randint(1, 9)
    n2 = random.randint(1, 9)
    op = random.choice(['+', '-'])
    
    if op == '-':
        if n1 < n2:
            n1, n2 = n2, n1
        ans = n1 - n2
    else:
        ans = n1 + n2
        
    choices = set()
    choices.add(ans)
    
    while len(choices) < 3:
        wrong = ans + random.randint(-5, 5)
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

# --- 동물 세레모니 함수 ---
def show_ceremony():
    animals = ["🐶 강아지", "🐱 고양이", "🐰 토끼", "🐼 팬더", "🐨 코알라", "🐯 호랑이", "🦁 사자", "🐧 펭귄"]
    messages = ["대단해요!", "참 잘했어요!", "멋져요!", "천재인가봐요!", "정답입니다!"]
    
    animal = random.choice(animals)
    msg = random.choice(messages)
    
    st.balloons() # 풍선 효과
    st.success(f"## 🎉 {animal}가 축하해줘요: \"{msg}\"")
    
    # 귀여운 동물 이모지 크게 보여주기
    st.markdown(f"<div style='text-align: center; font-size: 100px;'>{animal.split()[0]}</div>", unsafe_allow_html=True)

# --- 메인 로직 ---

# 처음이거나 다음 문제 버튼을 눌렀을 때
if not st.session_state.problem_generated:
    generate_problem()

# 문제 보여주기 (CSS 적용)
quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?"
st.markdown(f'<p class="big-font">❓ 문제: {quiz_text}</p>', unsafe_allow_html=True)

# 퀴즈 폼
with st.form("quiz_form"):
    # 라디오 버튼 (CSS로 크기 키움)
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True
    )
    
    # 제출 버튼
    submitted = st.form_submit_button("정답 확인")

    if submitted:
        if user_choice == st.session_state.answer:
            st.session_state.solved = True # 정답 상태로 변경
        else:
            st.error(f"😅 아쉬워요. 다시 한번 생각해볼까요?")

# 정답을 맞췄을 때만 세레모니와 다음 문제 버튼 표시 (폼 밖에서 처리)
if st.session_state.solved:
    show_ceremony()
    
    # 다음 문제 버튼
    if st.button("다음 문제 풀기 ➡️", type="primary"):
        st.session_state.problem_generated = False
        st.session_state.solved = False
        st.rerun()
