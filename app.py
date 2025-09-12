import streamlit as st
import random
import pandas as pd

# ----------------------
# 1. 단어 데이터 (예시)
# 여러 뜻은 리스트 형태로 저장
# ----------------------
word_dict = {
    "define": ["정의하다"],
    "substitute": ["대체하다", "대신하다"],
    "stair": ["계단"],
    "philosopher": ["철학자"],
    "preparation": ["준비", "대비"]
}

words = list(word_dict.keys())

# ----------------------
# 2. 페이지 선택
# ----------------------
st.title("📘 단어 시험 웹앱")
page = st.sidebar.radio("모드 선택", ["뜻 → 영단어", "영단어 → 뜻"])

# ----------------------
# 3. 세션 초기화
# ----------------------
if "quiz_word" not in st.session_state:
    st.session_state.quiz_word = random.choice(words)
    st.session_state.score = 0
    st.session_state.total = 0
    st.session_state.history = []  # 기록용

quiz_word = st.session_state.quiz_word

# ----------------------
# 4. 뜻 → 영단어 모드
# ----------------------
if page == "뜻 → 영단어":
    meaning = ", ".join(word_dict[quiz_word])
    st.subheader(f"문제: {meaning}")
    answer = st.text_input("이 뜻에 맞는 영어 단어는?")

    if st.button("제출"):
        st.session_state.total += 1
        if answer.strip().lower() == quiz_word:
            st.success("정답입니다! ✅")
            st.session_state.score += 1
        else:
            st.error(f"오답입니다 ❌ (정답: {quiz_word})")
        st.session_state.history.append({
            "문제": meaning,
            "정답": quiz_word,
            "내 답": answer
        })
        st.session_state.quiz_word = random.choice(words)

# ----------------------
# 5. 영단어 → 뜻 모드
# ----------------------
elif page == "영단어 → 뜻":
    st.subheader(f"문제: {quiz_word}")
    answer = st.text_input("이 단어의 뜻은?")

    if st.button("제출"):
        st.session_state.total += 1
        correct_answers = word_dict[quiz_word]
        if answer.strip() in correct_answers:
            st.success("정답입니다! ✅")
            st.session_state.score += 1
        else:
            st.error(f"오답입니다 ❌ (정답: {', '.join(correct_answers)})")
        st.session_state.history.append({
            "문제": quiz_word,
            "정답": ", ".join(correct_answers),
            "내 답": answer
        })
        st.session_state.quiz_word = random.choice(words)

# ----------------------
# 6. 결과 및 기록
# ----------------------
st.write(f"점수: {st.session_state.score} / {st.session_state.total}")

if st.checkbox("📊 전체 기록 보기"):
    if st.session_state.history:
        df = pd.DataFrame(st.session_state.history)
        st.table(df)
    else:
        st.write("아직 기록이 없습니다.")
