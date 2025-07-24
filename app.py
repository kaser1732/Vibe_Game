import streamlit as st
import time
import random

# 상태 초기화
if "state" not in st.session_state:
    st.session_state.state = "ready"
    st.session_state.wait_until = None
    st.session_state.start_time = None
    st.session_state.reaction_time = None

st.title("⚡ 반응속도 테스트")

# 스타일: 큰 네모 박스용
st.markdown("""
    <style>
    .box {
        display: flex;
        justify-content: center;
        align-items: center;
        height: 200px;
        font-size: 36px;
        font-weight: bold;
        color: white;
        border-radius: 16px;
        cursor: pointer;
        user-select: none;
        margin-top: 20px;
    }
    .wait-box {
        background-color: gray;
    }
    .go-box {
        background-color: green;
    }
    .result-box {
        background-color: #444;
    }
    </style>
""", unsafe_allow_html=True)

# 단계별 처리
if st.session_state.state == "ready":
    if st.button("🎮 시작하기"):
        st.session_state.wait_until = time.time() + random.uniform(2, 5)
        st.session_state.state = "waiting"
        st.experimental_rerun()

elif st.session_state.state == "waiting":
    # 사용자가 확인 버튼 누를 때까지 기다림
    st.markdown('<div class="box wait-box">🕓 준비 중입니다...<br>곧 초록불이 뜹니다</div>', unsafe_allow_html=True)
    if st.button("🟢 확인"):
        if time.time() >= st.session_state.wait_until:
            st.session_state.start_time = time.time()
            st.session_state.state = "go"
            st.experimental_rerun()
        else:
            st.warning("⏳ 아직이에요! 너무 빨랐어요!")

elif st.session_state.state == "go":
    if st.button("✅ 클릭!"):
        reaction = int((time.time() - st.session_state.start_time) * 1000)
        st.session_state.reaction_time = reaction
        st.session_state.state = "done"
        st.experimental_rerun()
    else:
        st.markdown('<div class="box go-box">💚 지금 클릭하세요!</div>', unsafe_allow_html=True)

elif st.session_state.state == "done":
    st.markdown(f'<div class="box result-box">⏱ 반응속도: {st.session_state.reaction_time} ms</div>', unsafe_allow_html=True)
    if st.button("🔁 다시하기"):
        st.session_state.state = "ready"
        st.session_state.reaction_time = None
        st.session_state.start_time = None
        st.session_state.wait_until = None
        st.experimental_rerun()
