import streamlit as st
import pandas as pd
import random
import os
import re
from fpdf import FPDF
import base64

# --- 페이지 설정 ---
st.set_page_config(
    page_title="WtoM (Word to Meaning)",
    layout="wide"
)

# --- 세션 상태 초기화 ---
if 'quiz_started' not in st.session_state:
    st.session_state.quiz_started = False
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'total_questions' not in st.session_state:
    st.session_state.total_questions = 0
if 'current_word_index' not in st.session_state:
    st.session_state.current_word_index = 0
if 'quiz_data' not in st.session_state:
    st.session_state.quiz_data = None
if 'results' not in st.session_state:
    st.session_state.results = []
if 'quiz_day' not in st.session_state:
    st.session_state.quiz_day = None
if 'user_answer' not in st.session_state:
    st.session_state.user_answer = ""

# --- 데이터 로드 함수 ---
def load_words(day):
    file_path = os.path.join("data", f"Day{day}.csv")
    if os.path.exists(file_path):
        try:
            df = pd.read_csv(file_path, encoding='utf-8')
            return df
        except pd.errors.ParserError:
            st.error(f"'{file_path}' 파일의 형식에 오류가 있습니다. CSV 파일을 쌍따옴표로 올바르게 묶었는지 확인해주세요.")
            return None
    else:
        st.error(f"'{file_path}' 파일을 찾을 수 없습니다. 파일 경로를 확인해주세요.")
        return None

# --- 정답 체크 함수 ---
def check_answer(word_meaning, user_answer):
    correct_candidates = []
    
    # 세미콜론(;)으로 1차 분리
    meaning_list = word_meaning.split(';')
    for item in meaning_list:
        # 쉼표(,)로 2차 분리
        sub_items = item.split(',')
        correct_candidates.extend([s.strip() for s in sub_items if s.strip()])
    
    # 사용자의 답변을 정규화합니다. (모든 공백과 특수문자 제거)
    user_answer_normalized = re.sub(r'[\s\.\;:\'"]', '', user_answer).lower()
    
    for candidate in correct_candidates:
        # 정답 후보도 정규화합니다.
        candidate_normalized = re.sub(r'[\s\.\;:\'"]', '', candidate).lower()
        if user_answer_normalized == candidate_normalized:
            return True, word_meaning
            
    return False, word_meaning

# --- 퀴즈 시작 함수 ---
def start_quiz():
    if st.session_state.quiz_day:
        df = load_words(st.session_state.quiz_day)
        if df is not None and not df.empty:
            st.session_state.quiz_data = df.sample(frac=1).reset_index(drop=True)
            st.session_state.total_questions = len(st.session_state.quiz_data)
            st.session_state.quiz_started = True
            st.session_state.score = 0
            st.session_state.current_word_index = 0
            st.session_state.results = []
        else:
            st.warning("선택한 Day에 단어가 없습니다. 다른 Day를 선택해주세요.")

# --- 정답 제출 콜백 함수 ---
def submit_answer():
    if st.session_state.user_answer:
        current_data = st.session_state.quiz_data.iloc[st.session_state.current_word_index]
        word = current_data['word']
        meaning = current_data['meaning']
        user_answer = st.session_state.user_answer

        is_correct, correct_meaning = check_answer(meaning, user_answer)
        st.session_state.results.append({
            '단어': word,
            '정답': correct_meaning,
            '내 답변': user_answer,
            '결과': '✅ 정답' if is_correct else '❌ 오답'
        })
        if is_correct:
            st.success("정답입니다!")
            st.session_state.score += 1
        else:
            st.error(f"오답입니다. 정답은: {correct_meaning}")
        
        st.session_state.current_word_index += 1
        st.session_state.user_answer = "" # 다음 문제를 위해 입력창 초기화
        st.rerun()

# --- 메인 페이지 UI ---
st.title("WtoM (Word to Meaning) - 단어 시험")

if not st.session_state.quiz_started:
    st.info("단어 시험을 시작하려면 아래에서 Day를 선택해주세요.")
    
    # Day 선택 기능
    day_options = [f'Day{i}' for i in range(1, 45)]
    selected_day_str = st.selectbox("Day를 선택하세요", options=day_options, index=None)
    
    if selected_day_str:
        st.session_state.quiz_day = int(selected_day_str.replace('Day', ''))

    st.button("시험 시작", on_click=start_quiz, use_container_width=True)

else:
    if st.session_state.current_word_index < st.session_state.total_questions:
        # --- 퀴즈 진행 중 ---
        current_data = st.session_state.quiz_data.iloc[st.session_state.current_word_index]
        word = current_data['word']
        
        st.header(f"Day {st.session_state.quiz_day} 단어 시험 ({st.session_state.current_word_index + 1}/{st.session_state.total_questions})")
        st.markdown("---")
        st.markdown(f"### **단어:** `{word}`")
        
        # Enter키로 제출 가능한 폼
        with st.form(key=f'quiz_form_{st.session_state.current_word_index}'):
            st.text_input("뜻을 입력하세요:", key='user_answer')
            st.form_submit_button("정답 확인 (Enter키로 제출)", use_container_width=True)
        
        # 폼 제출 후 로직 처리
        if st.session_state.user_answer:
            current_data = st.session_state.quiz_data.iloc[st.session_state.current_word_index]
            word = current_data['word']
            meaning = current_data['meaning']
            user_answer = st.session_state.user_answer

            is_correct, correct_meaning = check_answer(meaning, user_answer)
            st.session_state.results.append({
                '단어': word,
                '정답': correct_meaning,
                '내 답변': user_answer,
                '결과': '✅ 정답' if is_correct else '❌ 오답'
            })
            if is_correct:
                st.success("정답입니다!")
                st.session_state.score += 1
            else:
                st.error(f"오답입니다. 정답은: {correct_meaning}")
            
            st.session_state.current_word_index += 1
            st.session_state.user_answer = ""
            st.rerun()

    else:
        # --- 퀴즈 종료 ---
        st.header("단어 시험 결과")
        st.markdown("---")
        st.subheader(f"총 {st.session_state.total_questions}문제 중 {st.session_state.score}개를 맞혔습니다!")
        
        results_df = pd.DataFrame(st.session_state.results)
        st.table(results_df)
        
        if st.button("다시 시작하기", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_data = None
            st.session_state.results = []
            st.rerun()
