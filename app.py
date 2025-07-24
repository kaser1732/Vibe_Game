import streamlit as st
import time
import random

st.set_page_config(layout="centered")

st.title("🎵 리듬 게임 - 타이밍을 맞춰 클릭하세요!")
st.markdown("타이밍이 맞을 때 `클릭`을 누르세요! 총 10박자 🎶")

if "step" not in st.session_state:
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.logs = []
    st.session_state.start_time = 0
    st.session_state.beat_times = []

# 게임 시작
if st.button("게임 시작", key="start_btn"):
    st.session_state.step = 0
    st.session_state.score = 0
    st.session_state.logs = []
    st.session_state.beat_times = []

    beat_interval = 1.5  # 박자 간격
    st.session_state.start_time = time.time()

    # 리듬 10박자 타이밍 생성
    for i in range(10):
        st.session_state.beat_times.append(st.session_state.start_time + beat_interval * i)

    st.experimental_rerun()

# 게임 진행 중
if st.session_state.beat_times and st.session_state.step < len(st.session_state.beat_times):
    next_beat = st.session_state.beat_times[st.session_state.step]
    now = time.time()

    time_left = next_beat - now

    if time_left <= 0:
        st.write(f"🎯 박자 {st.session_state.step + 1}!")

        if st.button("💥 지금 클릭!", key=f"click_{st.session_state.step}"):
            click_time = time.time()
            delta = abs(click_time - next_beat)

            if delta < 0.2:
                result = "🎯 Perfect"
                st.session_state.score += 100
            elif delta < 0.4:
                result = "👍 Good"
                st.session_state.score += 50
            else:
                result = "❌ Miss"
            st.session_state.logs.append((st.session_state.step + 1, result))
            st.session_state.step += 1
            st.experimental_rerun()
        else:
            # 자동 Miss 처리
            if time_left < -0.6:
                st.session_state.logs.append((st.session_state.step + 1, "❌ Miss"))
                st.session_state.step += 1
                st.experimental_rerun()
    else:
        st.write(f"⏱️ 다음 박자까지 {time_left:.2f}초...")

# 결과 출력
if st.session_state.step == 10:
    st.subheader("🎉 결과")
    for beat, result in st.session_state.logs:
        st.write(f"{beat}박자 → {result}")
    st.markdown(f"**총점: {st.session_state.score}점**")
