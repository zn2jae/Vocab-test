import streamlit as st
import pandas as pd
import random
import os
import re

# --- 페이지 설정 ---
st.set_page_config(
    page_title="MtoW (Meaning to Word)",
    layout="wide"
)

# --- 세션 상태 초기화 ---
if 'quiz_started_mtow' not in st.session_state:
    st.session_state.quiz_started_mtow = False
if 'score_mtow' not in st.session_state:
    st.session_state.score_mtow = 0
if 'total_questions_mtow' not in st.session_state:
    st.session_state.total_questions_mtow = 0
if 'current_word_index_mtow' not in st.session_state:
    st.session_state.current_word_index_mtow = 0
if 'quiz_data_mtow' not in st.session_state:
    st.session_state.quiz_data_mtow = None
if 'results_mtow' not in st.session_state:
    st.session_state.results_mtow = []
if 'quiz_day_mtow' not in st.session_state:
    st.session_state.quiz_day_mtow = None

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

# --- 퀴즈 시작 함수 ---
def start_quiz_mtow():
    if st.session_state.quiz_day_mtow:
        df = load_words(st.session_state.quiz_day_mtow)
        if df is not None and not df.empty:
            st.session_state.quiz_data_mtow = df.sample(frac=1).reset_index(drop=True)
            st.session_state.total_questions_mtow = len(st.session_state.quiz_data_mtow)
            st.session_state.quiz_started_mtow = True
            st.session_state.score_mtow = 0
            st.session_state.current_word_index_mtow = 0
            st.session_state.results_mtow = []
        else:
            st.warning("선택한 Day에 단어가 없습니다. 다른 Day를 선택해주세요.")

# --- 메인 페이지 UI ---
st.title("MtoW (Meaning to Word) - 뜻 맞히기")

if not st.session_state.quiz_started_mtow:
    st.info("단어 시험을 시작하려면 아래에서 Day를 선택해주세요.")

    day_options = [f'Day{i}' for i in range(1, 45)]
    selected_day_str = st.selectbox("Day를 선택하세요", options=day_options, index=None)
    
    if selected_day_str:
        st.session_state.quiz_day_mtow = int(selected_day_str.replace('Day', ''))

    st.button("시험 시작", on_click=start_quiz_mtow, use_container_width=True)

else:
    if st.session_state.current_word_index_mtow < st.session_state.total_questions_mtow:
        current_data = st.session_state.quiz_data_mtow.iloc[st.session_state.current_word_index_mtow]
        word = current_data['word']
        meaning = current_data['meaning']
        
        st.header(f"Day {st.session_state.quiz_day_mtow} 단어 시험 ({st.session_state.current_word_index_mtow + 1}/{st.session_state.total_questions_mtow})")
        st.markdown("---")
        
        display_meaning = meaning.split(';')[0].strip()
        if ',' in display_meaning:
            display_meaning = display_meaning.split(',')[0].strip()
        
        st.markdown(f"### **뜻:** `{display_meaning}`")
        
        with st.form(key=f'quiz_form_mtow_{st.session_state.current_word_index_mtow}'):
            user_answer = st.text_input("단어를 입력하세요:", key=f'user_answer_form_mtow_{st.session_state.current_word_index_mtow}')
            submit_button = st.form_submit_button("제출", use_container_width=True)

            if submit_button:
                is_correct = (user_answer.strip().lower() == word.strip().lower())
                
                st.session_state.results_mtow.append({
                    '뜻': meaning,
                    '정답': word,
                    '내 답변': user_answer,
                    '결과': '✅ 정답' if is_correct else '❌ 오답'
                })
                if is_correct:
                    st.success("정답입니다!")
                    st.session_state.score_mtow += 1
                else:
                    st.error(f"오답입니다. 정답은: {word}")
                
                st.session_state.current_word_index_mtow += 1
                st.rerun()
            
    else:
        st.header("고생하셨습니다")
        
        results_df = pd.DataFrame(st.session_state.results_mtow)
        st.table(results_df)
        
        if st.button("다시 시작하기", use_container_width=True):
            st.session_state.quiz_started_mtow = False
            st.session_state.quiz_data_mtow = None
            st.session_state.results_mtow = []
            st.rerun()
