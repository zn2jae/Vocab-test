import streamlit as st

st.set_page_config(page_title="Home", page_icon="🏠")

st.title("🏠 Welcome to the Vocabulary Test App")

st.markdown("""
이 앱에서는 Day별로 단어 시험을 치를 수 있습니다.

- 단어 → 뜻
- 뜻 → 단어

왼쪽 사이드바에서 Day를 선택하고, 원하는 시험 페이지로 이동하세요.
""")

st.info("페이지는 사이드바에서 선택 가능합니다.")
