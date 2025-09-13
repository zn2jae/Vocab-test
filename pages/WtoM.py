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
    
    # 뜻풀이에서 쉼표와 세미콜론을 모두 구분자로 사용해 정답 후보를 만듭니다.
    meaning_list = re.split(';|,', word_meaning)
    for item in meaning_list:
        correct_candidates.append(item.strip())
    
    # 사용자의 답변과 모든 정답 후보를 정규화하여 비교합니다.
    user_answer_normalized = re.sub(r'[\s\.\;:\'"]', '', user_answer).lower()
    
    for candidate in correct_candidates:
        candidate_normalized = re.sub(r'[\s\.\;:\'"]', '', candidate).lower()
        if user_answer_normalized == candidate_normalized:
            return True, word_meaning
            
    return False, word_meaning

# --- PDF 생성 함수 ---
def create_pdf(results_df, day):
    class PDF(FPDF):
        def header(self):
            self.set_font('malgun', '', 12)
            self.cell(0, 10, f'Voca Test Results - Day {day}', 0, 1, 'C')
            self.ln(10)

        def footer(self):
            self.set_y(-15)
            self.set_font('malgun', '', 8)
            self.cell(0, 10, f'Page {self.page_no()}/{{nb}}', 0, 0, 'C')

        def chapter_title(self, title):
            self.set_font('malgun', '', 12)
            self.cell(0, 10, title, 0, 1, 'L')
            self.ln(4)

        def chapter_body(self, data):
            self.set_font('malgun', '', 10)
            self.multi_cell(0, 6, data)
            self.ln()
    
    # 폰트 파일이 없으면 오류 메시지를 표시하고 종료합니다.
    font_path = "fonts/malgun.ttf"
    if not os.path.exists(font_path):
        st.error("폰트 파일을 찾을 수 없습니다. 'fonts' 폴더에 'malgun.ttf'를 넣어주세요.")
        return None

    pdf = PDF()
    pdf.add_font('malgun', '', font_path, uni=True)
    pdf.set_font('malgun', '', 10)
    
    pdf.add_page()
    pdf.alias_nb_pages()

    # 테이블 헤더
    pdf.set_font('malgun', '', 10)
    pdf.cell(50, 10, '단어', 1, 0, 'C')
    pdf.cell(80, 10, '정답', 1, 0, 'C')
    pdf.cell(60, 10, '내 답변', 1, 1, 'C')
    
    # 테이블 내용
    for index, row in results_df.iterrows():
        pdf.cell(50, 10, str(row['단어']), 1, 0)
        pdf.cell(80, 10, str(row['정답']), 1, 0)
        pdf.cell(60, 10, str(row['내 답변']), 1, 1)

    return pdf.output(dest='S').encode('latin1')

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
        meaning = current_data['meaning']
        
        st.header(f"Day {st.session_state.quiz_day} 단어 시험 ({st.session_state.current_word_index + 1}/{st.session_state.total_questions})")
        st.markdown("---")
        st.markdown(f"### **단어:** `{word}`")
        
        user_answer = st.text_input("뜻을 입력하세요:", key=f"word_input_{st.session_state.current_word_index}")

        # Enter키 제출 기능
        if user_answer:
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
            st.rerun()

    else:
        # --- 퀴즈 종료 ---
        st.header("단어 시험 결과")
        st.markdown("---")
        st.subheader(f"총 {st.session_state.total_questions}문제 중 {st.session_state.score}개를 맞혔습니다!")
        
        results_df = pd.DataFrame(st.session_state.results)
        
        # PDF 다운로드 버튼
        pdf_file = create_pdf(results_df, st.session_state.quiz_day)
        if pdf_file:
            st.download_button(
                label="PDF 결과 다운로드",
                data=pdf_file,
                file_name=f'Voca_Test_Day{st.session_state.quiz_day}_Results.pdf',
                mime="application/pdf",
                use_container_width=True
            )

        if st.button("다시 시작하기", use_container_width=True):
            st.session_state.quiz_started = False
            st.session_state.quiz_data = None
            st.session_state.results = []
            st.rerun()
