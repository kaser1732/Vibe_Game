import streamlit as st
import time
import random

if "started" not in st.session_state:
    st.session_state.started = False
if "start_time" not in st.session_state:
    st.session_state.start_time = 0.0
if "message" not in st.session_state:
    st.session_state.message = ""
if "result" not in st.session_state:
    st.session_state.result = None

st.title("⚡ 반응속도 테스트")

if not st.session_state.started:
    if st.button("🎮 시작하기"):
        st.session_state.started = True
        st.session_state.message = "준비하세요..."
        st.session_state.result = None
        wait_time = random.uniform(2, 5)
        time.sleep(wait_time)
        st.session_state.message = "💚 지금 클릭하세요!"
        st.session_state.start_time = time.time()
        st.experimental_rerun()
else:
    st.write(st.session_state.message)
    if st.session_state.message == "💚 지금 클릭하세요!":
        if st.button("✅ 클릭!"):
            reaction_time = (time.time() - st.session_state.start_time) * 1000
            st.session_state.result = f"⏱ 반응속도: {int(reaction_time)} ms"
            st.session_state.started = False
            st.experimental_rerun()
    else:
        if st.button("🚫 너무 빨라요! 다시 시작"):
            st.session_state.result = "⚠️ 너무 빨리 눌렀습니다. 다시 시도하세요."
            st.session_state.started = False
            st.experimental_rerun()

if st.session_state.result:
    st.markdown(st.session_state.result)
