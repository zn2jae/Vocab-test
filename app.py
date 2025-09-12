import streamlit as st
import random
import pandas as pd

# ----------------------
# 1. 단어 데이터 (예시: 나중에 Day1~Day20 단어 리스트를 넣으면 됨)
# ----------------------
day_words = {
    "Day1": {
        "define": ["정의하다"],
        "substitute": ["대체하다", "대신하다"]
    },
    "Day2": {
        "stair": ["계단"],
        "philosopher": ["철학자"]
    }
    # 나머지 Day3~Day20은 나중에 추가
}

# ----------------------
# 2. Day 선택
# ----------------------
st.title("📘 단어 시험 웹앱")
selected_day = st.sidebar.selectbox("Day 선택", [f"Day{i}" for i in range(1, 21)])

if st.button("Start" or "시험 시작"):
    st.session_state.quiz_words = list(day_words[selected_day].keys())
    random.shuffle(st.session_state.quiz_words)
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.history = []
    st.session_state.current_index = 0
    st.session_state.show_quiz = True

# ----------------------
# 3. 시험 진행 (단어 -> 뜻)
# ----------------------
if "show_quiz" in st.session_state and st.session_state.show_quiz:
    current_word = st.session_state.quiz_words[st.session_state.current_index]
    current_meanings = day_words[selected_day][current_word]

    st.subheader(f"문제: {current_word}")

    with st.form(key=f'quiz_form_{st.session_state.current_index}'):
        answer = st.text_input("이 단어의 뜻은?")
        submitted = st.form_submit_button("제출")

        if submitted:
            st.session_state.total += 1

            if answer.strip() in current_meanings:
                st.success("정답 ✅")
                st.session_state.score += 1
            else:
                st.error(f"오답 ❌ (정답: {', '.join(current_meanings)})")

            st.session_state.history.append({
                "문제": current_word,
                "정답": ', '.join(current_meanings),
                "내 답": answer
            })

            # 자동 다음 문제
            st.session_state.current_index += 1
            if st.session_state.current_index >= len(st.session_state.quiz_words):
                st.session_state.show_quiz = False
                st.session_state.exam_finished = True
                st.success(f"시험 종료! 최종 점수: {st.session_state.score} / {st.session_state.total}")

# ----------------------
# 4. 시험 종료 후 기록 보기 버튼
# ----------------------
if "exam_finished" in st.session_state and st.session_state.exam_finished:
    if st.button("📊 전체 기록 보기"):
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
