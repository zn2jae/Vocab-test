import streamlit as st

st.set_page_config(
    page_title="Voca Test App",
    layout="wide"
)

st.title("📚 Voca Test App")
st.markdown("---")

st.markdown(
    """
    ### **단어 학습의 새로운 시작, Voca Test App에 오신 것을 환영합니다!**

    이 앱은 **Day 1부터 Day 44**까지의 영단어들을 효과적으로 암기하고 복습할 수 있도록 설계된 맞춤형 단어 학습 솔루션입니다.
    여러분이 힘겹게 외웠던 단어들이 여러분의 머릿속에 '영원히' 남도록 도와드릴게요.
    
    왼쪽 사이드바에서 두 가지 강력한 학습 모드를 선택하여 자신에게 맞는 방식으로 단어를 정복해 보세요!
    """
)

# 학습 모드 카드 섹션
st.markdown("---")
st.subheader("💡 **나만의 학습 모드 선택하기**")

col1, col2 = st.columns(2)

with col1:
    with st.container(border=True):
        st.markdown(
            """
            ### **✍️ WtoM (Word to Meaning)**
            
            **[ 영어 단어 → 한국어 뜻 ]**
            
            영단어를 보고 뜻을 맞히는 가장 기본적인 학습 모드입니다.
            단어를 정확하게 이해하고 있는지 확인하고, 복습 효과를 극대화하세요.
            """
        )
        if st.button("WtoM으로 바로가기", use_container_width=True):
            st.switch_page("pages/WtoM.py")

with col2:
    with st.container(border=True):
        st.markdown(
            """
            ### **🧠 MtoW (Meaning to Word)**
            
            **[ 한국어 뜻 → 영어 단어 ]**
            
            뜻만 보고도 단어를 떠올리는 훈련을 할 수 있는 심화 학습 모드입니다.
            수동적인 암기를 넘어, 능동적인 단어 회상 능력을 길러보세요.
            """
        )
        if st.button("MtoW으로 바로가기", use_container_width=True):
            st.switch_page("pages/MtoW.py")

st.markdown("---")

# 플래시카드 소개
st.subheader("💡 **보너스! 플래시카드로 더 쉽게 외우기**")
st.info(
    "단어를 암기하는 데 어려움을 느낀다면, 사이드바의 **'단어 플래시카드'** 메뉴를 활용해보세요! "
    "단어와 뜻이 번갈아 나타나는 플래시카드로 재미있고 효과적으로 학습할 수 있습니다."
)

st.markdown(
    """
    **Made with ❤️ using Streamlit**
    """
)
