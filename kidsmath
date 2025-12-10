import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="초1 수학 퀴즈", page_icon="✏️")

st.title("🎓 1학년 수학: 덧셈과 뺄셈")
st.write("문제를 보고 알맞은 답을 골라보세요!")

# 세션 상태 초기화
if 'num1' not in st.session_state:
    st.session_state.num1 = 0
    st.session_state.num2 = 0
    st.session_state.operator = '+'
    st.session_state.answer = 0
    st.session_state.choices = []
    st.session_state.problem_generated = False

# 문제 생성 함수
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

# 메인 로직
if not st.session_state.problem_generated:
    generate_problem()

col1, col2, col3 = st.columns([1, 2, 1])
with col2:
    st.markdown(f"### ❓ 문제: {st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?")

with st.form("quiz_form"):
    user_choice = st.radio("정답을 선택하세요:", options=st.session_state.choices, horizontal=True)
    submitted = st.form_submit_button("정답 확인")

    if submitted:
        if user_choice == st.session_state.answer:
            st.success("🎉 정답입니다! 참 잘했어요.")
            if st.form_submit_button("다음 문제"): 
                st.session_state.problem_generated = False
                st.rerun()
        else:
            st.error(f"😅 다시 생각해볼까요? (정답은 {st.session_state.answer})")
            
if st.button("새로운 문제 만들기"):
    st.session_state.problem_generated = False
    st.rerun()
