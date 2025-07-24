import streamlit as st
import time
import random

# 초기 상태
if "state" not in st.session_state:
    st.session_state.state = "ready"
    st.session_state.wait_until = None
    st.session_state.start_time = None
    st.session_state.reaction_time = None

st.title("⚡ 반응속도 테스트")

# 스타일 정의
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

# 상태 흐름
if st.session_state.state == "ready":
    if st.button("🎮 시작하기"):
        st.session_state.wait_until = time.time() + random.uniform(2, 5)
        st.session_state.state = "waiting"
        st.rerun()

elif st.session_state.state == "waiting":
    if time.time() >= st.session_state.wait_until:
        st.session_state.start_time = time.time()
        st.session_state.state = "go"
        st.rerun()
    else:
        st.info("🕓 준비 중입니다...")

elif st.session_state.state == "go":
    # 큰 박스 전체가 클릭되도록 HTML로 처리
    st.markdown(f"""
        <div class="click-box" onclick="fetch('{st.request.url}', {{method: 'POST'}}).then(() => window.location.reload());">
            💚 지금 클릭하세요!
        </div>
    """, unsafe_allow_html=True)
    # 사용자 클릭 감지를 위해 dummy form (Streamlit 방식)
    with st.form("click_form", clear_on_submit=True):
        clicked = st.form_submit_button("📥 내부 감지용 버튼 (숨김)", help="표시되지 않습니다")
        if clicked:
            st.session_state.reaction_time = int((time.time() - st.session_state.start_time) * 1000)
            st.session_state.state = "done"
            st.rerun()

elif st.session_state.state == "done":
    st.success(f"⏱ 반응속도: {st.session_state.reaction_time} ms")
    if st.button("🔁 다시하기"):
        st.session_state.state = "ready"
        st.session_state.wait_until = None
        st.session_state.start_time = None
        st.session_state.reaction_time = None
        st.rerun()
