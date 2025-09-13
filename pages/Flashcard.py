import streamlit as st
import pandas as pd
import random
import os

# --- 페이지 설정 ---
st.set_page_config(
    page_title="단어 플래시카드",
    layout="centered"
)

# --- 세션 상태 초기화 ---
if 'flashcard_day' not in st.session_state:
    st.session_state.flashcard_day = None
if 'flashcard_data' not in st.session_state:
    st.session_state.flashcard_data = None
if 'card_index' not in st.session_state:
    st.session_state.card_index = 0
if 'show_meaning' not in st.session_state:
    st.session_state.show_meaning = False

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

# --- 메인 페이지 UI ---
st.title("단어 플래시카드")
st.markdown("---")

if st.session_state.flashcard_data is None:
    st.info("플래시카드 학습을 시작하려면 Day를 선택해주세요.")
    
    # Day 선택 기능
    day_options = [f'Day{i}' for i in range(1, 45)]
    selected_day_str = st.selectbox("Day를 선택하세요", options=day_options, index=None)
    
    if selected_day_str:
        st.session_state.flashcard_day = int(selected_day_str.replace('Day', ''))

    if st.button("학습 시작", use_container_width=True):
        if st.session_state.flashcard_day:
            df = load_words(st.session_state.flashcard_day)
            if df is not None and not df.empty:
                st.session_state.flashcard_data = df.sample(frac=1).reset_index(drop=True)
                st.session_state.card_index = 0
                st.session_state.show_meaning = False
                st.rerun()
            else:
                st.warning("선택한 Day에 단어가 없습니다. 다른 Day를 선택해주세요.")

else:
    # --- 플래시카드 화면 ---
    total_cards = len(st.session_state.flashcard_data)
    current_card = st.session_state.flashcard_data.iloc[st.session_state.card_index]
    
    st.subheader(f"Day {st.session_state.flashcard_day} 학습 중 ({st.session_state.card_index + 1}/{total_cards})")
    
    # 플래시카드 컨테이너
    card_container = st.container(border=True)
    
    if not st.session_state.show_meaning:
        # 단어 표시
        card_container.markdown(f"<h1 style='text-align: center; color: black;'>{current_card['word']}</h1>", unsafe_allow_html=True)
    else:
        # 뜻 표시
        card_container.markdown(f"<h3 style='text-align: center; color: black;'>{current_card['meaning']}</h3>", unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    # '뜻 보기' 또는 '단어 보기' 버튼
    with col2:
        if st.button("뜻 보기" if not st.session_state.show_meaning else "단어 보기", use_container_width=True):
            st.session_state.show_meaning = not st.session_state.show_meaning
            st.rerun()
            
    # '다음 카드' 버튼
    with col3:
        if st.button("다음 카드", use_container_width=True):
            if st.session_state.card_index < total_cards - 1:
                st.session_state.card_index += 1
                st.session_state.show_meaning = False
                st.rerun()
            else:
                st.success("모든 단어를 학습했습니다! 다시 시작해주세요.")
                st.session_state.flashcard_data = None
                st.session_state.flashcard_day = None
                st.rerun()
    
    # '다시 시작' 버튼
    with col1:
        if st.button("다시 시작", use_container_width=True):
            st.session_state.flashcard_data = None
            st.session_state.flashcard_day = None
            st.rerun()
