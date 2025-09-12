import streamlit as st
import random
import pandas as pd

# ----------------------
# 1. 단어 데이터 (나중에 Day1~Day20 단어 리스트를 넣으면 됨)
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

# ----------------------
# 3. Start 버튼 (뜻 -> 단어 페이지)
# ----------------------
if st.button("Start 뜻 → 단어" or "시험 시작"):
    st.session_state.quiz_words_meaning = list(day_words[selected_day].items())  # (word, meanings) 튜플 리스트
    random.shuffle(st.session_state.quiz_words_meaning)
    st.session_state.score_meaning = 0
    st.session_state.total_meaning = 0
    st.session_state.history_meaning = []
    st.session_state.current_index_meaning = 0
    st.session_state.show_quiz_meaning = True
    st.session_state.exam_finished_meaning = False

# ----------------------
# 4. 시험 진행 (뜻 -> 단어)
# ----------------------
if "show_quiz_meaning" in st.session_state and st.session_state.show_quiz_meaning:
    current_word, current_meanings = st.session_state.quiz_words_meaning[st.session_state.current_index_meaning]
    st.subheader(f"문제: {', '.join(current_meanings)}")

    def submit_answer_meaning():
        answer = st.session_state.answer_input_meaning.strip()
        st.session_state.total_meaning += 1

        if answer.lower() == current_word.lower():
            st.success("정답 ✅")
            st.session_state.score_meaning += 1
        else:
            st.error(f"오답 ❌ (정답: {current_word})")

        st.session_state.history_meaning.append({
            "문제": ', '.join(current_meanings),
            "정답": current_word,
            "내 답": answer
        })

        # 자동 다음 문제
        st.session_state.current_index_meaning += 1
        if st.session_state.current_index_meaning >= len(st.session_state.quiz_words_meaning):
            st.session_state.show_quiz_meaning = False
            st.session_state.exam_finished_meaning = True
            st.success(f"시험 종료! 최종 점수: {st.session_state.score_meaning} / {st.session_state.total_meaning}")
        else:
            st.session_state.answer_input_meaning = ""  # 입력 초기화

    st.text_input("이 뜻에 맞는 영어 단어는?", key="answer_input_meaning", on_change=submit_answer_meaning)

# ----------------------
# 5. 시험 종료 후 기록 보기 버튼
# ----------------------
if "exam_finished_meaning" in st.session_state and st.session_state.exam_finished_meaning:
    if st.button("📊 전체 기록 보기 (뜻 → 단어)"):
        df = pd.DataFrame(st.session_state.history_meaning)
        st.table(df)
