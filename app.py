import streamlit as st
import random

st.set_page_config(page_title="야자 탈출 게임", layout="centered")

# 상태 초기화
if "stage" not in st.session_state:
    st.session_state.stage = "intro"
if "jump_attempt" not in st.session_state:
    st.session_state.jump_attempt = 0
if "has_stick" not in st.session_state:
    st.session_state.has_stick = False

st.title("🏫 야자를 째고 탈출하라!")
st.markdown("---")

# Stage: 인트로
if st.session_state.stage == "intro":
    st.markdown("**당신은 학교에서 야자를 진행 중이고 몰래 나가고 싶다.**")
    st.markdown("하지만... 밖에는 선생님이 복도를 지키고 있다.")

    choice = st.radio("무엇을 할까?", [
        "1. 창문으로 탈출한다",
        "2. 복도로 조용히 나간다",
        "3. 화장실로 간다",
        "4. 선생님을 때린다",
        "5. 그냥 뛰어간다"
    ])

    if st.button("선택"):
        if choice == "1. 창문으로 탈출한다":
            st.session_state.stage = "window"
        elif choice == "2. 복도로 조용히 나간다":
            st.session_state.stage = "hallway"
        elif choice == "3. 화장실로 간다":
            st.session_state.stage = "toilet"
        elif choice == "4. 선생님을 때린다":
            st.session_state.stage = "fight"
        elif choice == "5. 그냥 뛰어간다":
            st.session_state.stage = "run"
        st.rerun()

# Stage: 창문
elif st.session_state.stage == "window":
    if st.session_state.jump_attempt == 0:
        st.warning("여긴 4층이라서 안 될 것 같다...")
        st.session_state.jump_attempt += 1
        if st.button("다시 선택지로"):
            st.session_state.stage = "intro"
            st.rerun()
    else:
        st.info("그래 낙법 잘 치면 되겠지...")
        st.error("🪂 당신은 사망했습니다.")
        st.markdown("💀 **GAME OVER** 💀")
        if st.button("🔁 다시 시도하기"):
            st.session_state.stage = "intro"
            st.session_state.jump_attempt = 0
            st.rerun()

# Stage: 복도
elif st.session_state.stage == "hallway":
    st.error("👨‍🏫 선생님: 야 너 어디가?")
    st.markdown("💀 **GAME OVER** 💀")
    if st.button("🔁 다시 시도하기"):
        st.session_state.stage = "intro"
        st.rerun()

# Stage: 화장실
elif st.session_state.stage == "toilet":
    if not st.session_state.has_stick:
        st.success("🚽 화장실로 무사히 도착했다.")
        st.markdown("청소도구함이 눈에 띈다. 혹시 뭔가 있을까?")
        if st.button("청소도구함을 조사한다"):
            st.success("🧹 막대기(빗자루 손잡이)를 얻었다!")
            st.session_state.has_stick = True
            st.session_state.stage = "stick_action"
            st.rerun()
    else:
        st.session_state.stage = "stick_action"
        st.rerun()

# Stage: 막대기 액션 선택
elif st.session_state.stage == "stick_action":
    st.markdown("🧹 당신은 막대기를 들고 있다. 이제 어떻게 할까?")
    action = st.radio("막대기로 무엇을 할까?", [
        "천장을 쳐본다",
        "교실 문을 딴다",
        "거울을 깬다"
    ])
    if st.button("실행"):
        if action == "천장을 쳐본다":
            st.error("쾅쾅쾅! 선생님이 뛰어왔다!")
            st.markdown("👨‍🏫 선생님: 화장실에서 뭐 하는 거야?")
            st.markdown("💀 **GAME OVER** 💀")
        elif action == "교실 문을 딴다":
            st.success("✨ 교실 문이 살짝 열렸다! 아무도 눈치채지 못했다.")
            st.balloons()
            st.markdown("🏃‍♂️ 당신은 교실로 복귀한 척하면서 조용히 탈출에 성공했다!")
            st.markdown("🎉 **YOU ESCAPED!**")
        elif action == "거울을 깬다":
            st.error("쨍그랑! 시끄러운 소리에 선생님이 들이닥쳤다.")
            st.markdown("💀 **GAME OVER** 💀")
    if st.button("🔁 다시 시도하기"):
        st.session_state.stage = "intro"
        st.session_state.jump_attempt = 0
        st.session_state.has_stick = False
        st.rerun()

# Stage: 선생님을 때림
elif st.session_state.stage == "fight":
    st.markdown("👊 당신은 선생님을 때리려 했다.")
    st.error("하지만 선생님은 헬창이었다. 당신은 쳐맞았다.")
    st.markdown("💀 **GAME OVER** 💀")
    if st.button("🔁 다시 시도하기"):
        st.session_state.stage = "intro"
        st.rerun()

# Stage: 그냥 뛰어감
elif st.session_state.stage == "run":
    st.markdown("🏃‍♂️ 당신은 아무 생각 없이 그냥 뛰었다!")
    success = random.random() < 0.5  # 50% 확률
    if success:
        st.success("😮 선생님이 뒤돌아보지 않았다! 성공적으로 탈출!")
        st.balloons()
        st.markdown("🏃‍♂️ **YOU ESCAPED!**")
    else:
        st.error("👨‍🏫 선생님: 야!!! 어디가!")
        st.markdown("💀 **GAME OVER** 💀")
    if st.button("🔁 다시 시도하기"):
        st.session_state.stage = "intro"
        st.rerun()
