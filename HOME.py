import streamlit as st

st.set_page_config(
    page_title="Voca Test App",
    layout="centered"
)

st.title("Voca Test App")
st.markdown("---")

st.markdown(
    """
    ### Vocab Bible 단어 시험 앱에 오신 것을 환영합니다!
    
    이 앱은 **Day 1부터 Day 44**까지의 영단어를 효과적으로 학습할 수 있도록 도와줍니다.
    
    왼쪽 사이드바에서 원하는 학습 모드를 선택하여 단어 시험을 시작해보세요.
    
    ---
    """
)

st.subheader("📖 학습 모드")

st.markdown(
    """
    **1. WtoM (Word to Meaning)**
    * 영어 단어를 보고, 그 뜻을 맞히는 모드입니다.
    * 단어를 정확하게 알고 있는지 확인하는 데 도움이 됩니다.
    
    **2. MtoW (Meaning to Word)**
    * 한국어 뜻을 보고, 해당 영어 단어를 맞히는 모드입니다.
    * 단어를 보고 뜻을 아는 것을 넘어, 단어를 떠올리는 능력을 훈련할 수 있습니다.
    
    ---
    """
)

st.info("시작하려면 왼쪽의 사이드바에서 메뉴를 선택해주세요.")

# 사이드바에 메뉴 링크 추가 (선택 사항)
st.sidebar.markdown("### 메뉴")
if st.sidebar.button("WtoM으로 이동"):
    st.switch_page("pages/WtoM.py")

if st.sidebar.button("MtoW으로 이동"):
    st.switch_page("pages/MtoW.py")
