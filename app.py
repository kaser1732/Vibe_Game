import streamlit as st
import time
import random

if "state" not in st.session_state:
    st.session_state.state = "ready"
    st.session_state.wait_until = None
    st.session_state.start_time = None
    st.session_state.reaction_time = None

st.title("⚡ 반응속도 테스트")

# 스타일
st.markdown("""
    <style>
    .click-box {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        height: 300px;
        background-color: #28a745;
        color: white;
        font-size: 32px;
        font-weight: bold;
        border-radius: 16px;
        cursor: pointer;
        user-select: none;
        transition: 0.2s;
    }
    .click-box:hover {
        background-color: #218838;
    }
    </style>
""", unsafe_allow_html=True)

# 단계별 처리
if st.session_state.state == "ready":
    if st.button("🎮 시작하기"):
        st.session_state.wait_until = time.time() + random.uniform(2, 5)
        st.session_state.state = "waiting"

elif st.session_state.state == "waiting":
    st.info("🕓 준비 중입니다... 아래 버튼을 눌러 확인")
    if st.button("🔍 확인하기"):
        if time.time() >= st.session_state.wait_until:
            st.session_state.start_time = time.time()
            st.session_state.state = "go"

elif st.session_state.state == "go":
    # 박스를 클릭하면 반응 기록
    if st.button("💚 지금 클릭하세요!", use_container_width=True):
        st.session_state.reaction_time = int((time.time() - st.session_state.start_time) * 1000)
        st.session_state.state = "done"

elif st.session_state.state == "done":
    st.success(f"⏱ 반응속도: {st.session_state.reaction_time} ms")
    if st.button("🔁 다시하기"):
        st.session_state.state = "ready"
        st.session_state.reaction_time = None
        st.session_state.start_time = None
        st.session_state.wait_until = None
