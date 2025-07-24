import streamlit as st
import time
import random

# 상태 초기화
if "game_state" not in st.session_state:
    st.session_state.game_state = "idle"  # idle, wait, go, done
    st.session_state.wait_until = None
    st.session_state.start_time = None
    st.session_state.reaction_time = None

st.title("⚡ 반응속도 테스트")

if st.session_state.game_state == "idle":
    if st.button("🎮 시작하기"):
        wait = random.uniform(2, 5)
        st.session_state.wait_until = time.time() + wait
        st.session_state.game_state = "wait"
        st.rerun()  # 안전한 rerun

elif st.session_state.game_state == "wait":
    if time.time() >= st.session_state.wait_until:
        st.session_state.start_time = time.time()
        st.session_state.game_state = "go"
        st.rerun()  # 안전한 rerun
    else:
        st.info("🟡 준비 중입니다... 초록불이 뜨면 눌러주세요.")
        st.button("❌ 잘못 눌렀나요? 다시 시작", on_click=lambda: st.session_state.update({
            "game_state": "idle",
            "wait_until": None,
            "start_time": None,
            "reaction_time": None
        }))

elif st.session_state.game_state == "go":
    st.success("💚 지금 클릭하세요!")
    if st.button("✅ 클릭!"):
        st.session_state.reaction_time = int((time.time() - st.session_state.start_time) * 1000)
        st.session_state.game_state = "done"

elif st.session_state.game_state == "done":
    st.success(f"⏱ 반응속도: {st.session_state.reaction_time} ms")
    if st.button("🔁 다시하기"):
        st.session_state.game_state = "idle"
        st.session_state.reaction_time = None
        st.session_state.wait_until = None
        st.session_state.start_time = None
