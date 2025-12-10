import streamlit as st
import random

# ... (CSS 및 초기 설정 코드는 그대로 유지) ...
# ... (generate_problem 함수 그대로 유지) ...
# ... (show_ceremony 함수 그대로 유지) ...

# ---------------------------
# 메인 화면
# ---------------------------
st.title("🎓 1학년 수학 퀴즈")
st.markdown(f"**현재 단계:** {st.session_state.level} / **점수:** {st.session_state.score}점")

if not st.session_state.problem_generated:
    generate_problem()

quiz_text = f"{st.session_state.num1} {st.session_state.operator} {st.session_state.num2} = ?"
st.markdown(f'<div class="big-font">❓ 문제<br>{quiz_text}</div>', unsafe_allow_html=True)

# ---------------------------
# [중요] 문제 풀이 영역 (수정됨)
# ---------------------------
# st.form을 사용하면 'on_change'는 사용할 수 없습니다.
# 대신 버튼을 눌렀을 때의 로직을 탄탄하게 만들어야 합니다.
with st.form("quiz_form"):
    user_choice = st.radio(
        "정답을 골라보세요:",
        options=st.session_state.choices,
        horizontal=True,
        label_visibility="collapsed"
    )

    submitted = st.form_submit_button("정답 확인하기")

    if submitted:
        st.session_state.is_checked = True # 정답 확인 시도함
        
        if user_choice == st.session_state.answer:
            # [수정 포인트] 이미 푼 문제가 아닐 때만 점수 추가!
            if not st.session_state.solved:
                st.session_state.score += 10
                st.session_state.solved = True
        else:
            st.session_state.solved = False

# ---------------------------
# 결과 표시
# ---------------------------
if st.session_state.is_checked:
    if st.session_state.solved:
        # 정답인 경우
        show_ceremony()
        # 점수가 갱신된 것을 즉시 보여주기 위해 여기서 다시 출력하거나 rerender가 필요할 수 있음
        # 하지만 Streamlit 흐름상 위에서 +10 되고 다음 리런 때 반영됨. 
        # 즉시 반영된 점수를 보고 싶다면 아래처럼 강제 출력
        st.markdown(f"<div style='text-align:center; font-weight:bold;'>현재 점수: {st.session_state.score}점</div>", unsafe_allow_html=True)

        # 다음 문제 버튼 (Form 바깥에 위치해야 함)
        if st.button("➡️ 다음 문제 풀기"):
            st.session_state.step += 1
            # 5문제마다 레벨업 체크
            if st.session_state.step % 5 == 0:
                st.session_state.level = min(3, st.session_state.level + 1)
                st.balloons() # 레벨업 축하
            
            # 상태 초기화
            st.session_state.problem_generated = False
            st.session_state.is_checked = False
            st.session_state.solved = False
            st.rerun()
            
    else:
        # 오답인 경우
        st.error("😅 아쉬워요. 다시 한번 생각해볼까요?")
