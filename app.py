import streamlit as st
import time
import random

# 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "ready"  # ready, waiting, go, result
    st.session_state.start_time = None
    st.session_state.reaction_time = None
    st.session_state.wait_until = None

st.title("⚡ 반응속도 테스트")

# 현재 단계에 따라 분기
if st.session_state.stage == "ready":
    if st.button("🎮 시작하기"):
        wait = random.uniform(2, 5)
        st.session_state.wait_until = time.time() + wait
        st.session_state.stage = "waiting"

elif st.session_state.stage == "waiting":
    if time.time() >= st.session_state.wait_until:
        st.session_state.start_time = time.time()
        st.session_state.stage = "go"
        st.experimental_rerun()
    else:
        st.write("🟡 준비 중입니다... 초록불이 뜨면 눌러주세요!")

elif st.session_state.stage == "go":
    st.write("💚 지금 클릭하세요!")
    if st.button("✅ 클릭!"):
        st.session_state.reaction_time = int((time.time() - st.session_state.start_time) * 1000)
        st.session_state.stage = "result"
        st.experimental_rerun()

elif st.session_state.stage == "result":
    st.success(f"⏱ 반응속도: {st.session_state.reaction_time} ms")
    if st.button("🔁 다시하기"):
        st.session_state.stage = "ready"
        st.session_state.reaction_time = None
        st.session_state.start_time = None
        st.session_state.wait_until = None
        st.experimental_rerun()
