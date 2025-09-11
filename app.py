import streamlit as st
import random

# ----------------------
# 1. 단어 데이터 (예시)
# 실제로는 pdf에서 추출한 후 여기에 붙여넣으면 됨
# 형식: {"단어": "뜻"}
# ----------------------
word_dict = {
    "define": "정의하다",
    "substitute": "대체하다",
    "stair": "계단",
    "philosopher": "철학자",
    "preparation": "준비"
}

words = list(word_dict.keys())

st.title("📘 단어 시험 웹앱")
st.write("랜덤으로 문제를 출제합니다. 단어 뜻을 입력해보세요!")

# ----------------------
# 2. 문제 출제
# ----------------------
if "quiz_word" not in st.session_state:
    st.session_state.quiz_word = random.choice(words)
    st.session_state.score = 0
    st.session_state.total = 0

quiz_word = st.session_state.quiz_word

st.subheader(f"문제: {quiz_word}")
answer = st.text_input("이 단어의 뜻은?")

# ----------------------
# 3. 정답 확인
# ----------------------
if st.button("제출"):
    st.session_state.total += 1
    correct_answer = word_dict[quiz_word]
    if answer.strip() == correct_answer:
        st.success("정답입니다! ✅")
        st.session_state.score += 1
    else:
        st.error(f"오답입니다 ❌ (정답: {correct_answer})")

    # 다음 문제로 갱신
    st.session_state.quiz_word = random.choice(words)

# ----------------------
# 4. 점수 표시
# ----------------------
st.write(f"점수: {st.session_state.score} / {st.session_state.total}")
