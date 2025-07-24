import streamlit as st
import random

# 페이지 설정
st.set_page_config(page_title="도박 게임 허브", page_icon="🎰")

# 초기 잔액 세션 상태 설정
if "balance" not in st.session_state:
    st.session_state.balance = 100000
if "message" not in st.session_state:
    st.session_state.message = ""

# 공통 베팅 금액 입력
def get_bet():
    return st.number_input("💰 베팅 금액 입력:", min_value=1, max_value=st.session_state.balance, step=1000)

# 결과 메시지 처리
def show_result(msg):
    st.session_state.message = f"{msg}\n💵 현재 잔액: {st.session_state.balance:,}원"

# 게임들 정의
def slot_machine(bet):
    symbols = ["🍒", "🔔", "🍋", "💎", "7️⃣", "🍀"]
    result = [random.choice(symbols) for _ in range(3)]
    if result.count(result[0]) == 3:
        st.session_state.balance += bet * 4
        msg = f"{' | '.join(result)}\n🎉 잭팟! 5배 당첨!"
    elif result.count(result[0]) == 2 or result.count(result[1]) == 2:
        st.session_state.balance += bet
        msg = f"{' | '.join(result)}\n😎 두 개 일치! 2배 당첨!"
    else:
        st.session_state.balance -= bet
        msg = f"{' | '.join(result)}\n💸 꽝입니다."
    show_result(msg)

def high_or_low(bet, guess):
    user = random.randint(1, 13)
    comp = random.randint(1, 13)
    if (guess == "high" and comp > user) or (guess == "low" and comp < user):
        st.session_state.balance += bet
        msg = f"당신: {user}, 상대: {comp}\n🎉 맞췄습니다!"
    elif comp == user:
        msg = f"당신: {user}, 상대: {comp}\n😐 무승부!"
    else:
        st.session_state.balance -= bet
        msg = f"당신: {user}, 상대: {comp}\n❌ 틀렸습니다."
    show_result(msg)

def dice_game(bet, guess):
    roll = random.randint(1, 6)
    if (roll % 2 == 0 and guess == "even") or (roll % 2 == 1 and guess == "odd"):
        st.session_state.balance += bet
        msg = f"🎲 주사위: {roll}\n🎉 맞췄습니다!"
    else:
        st.session_state.balance -= bet
        msg = f"🎲 주사위: {roll}\n❌ 틀렸습니다."
    show_result(msg)

def roulette(bet, choice):
    num = random.randint(0, 36)
    color = random.choice(["red", "black"])
    if choice.isdigit() and int(choice) == num:
        st.session_state.balance += bet * 34
        msg = f"🎯 룰렛: {num} ({color})\n🎉 숫자 정답! 35배!"
    elif choice == color:
        st.session_state.balance += bet
        msg = f"🎯 룰렛: {num} ({color})\n🎉 색상 정답! 2배!"
    else:
        st.session_state.balance -= bet
        msg = f"🎯 룰렛: {num} ({color})\n❌ 틀렸습니다."
    show_result(msg)

def odd_even_sum(bet, user_num, guess):
    comp = random.randint(1, 9)
    total = user_num + comp
    if (total % 2 == 0 and guess == "even") or (total % 2 == 1 and guess == "odd"):
        st.session_state.balance += bet
        msg = f"당신: {user_num}, 컴: {comp} → 합: {total}\n🎉 맞췄습니다!"
    else:
        st.session_state.balance -= bet
        msg = f"당신: {user_num}, 컴: {comp} → 합: {total}\n❌ 틀렸습니다."
    show_result(msg)

def ladder_game(bet, choice):
    result = random.choice(["left", "right"])
    if choice == result:
        st.session_state.balance += bet
        msg = f"결과: {result}\n🎉 맞췄습니다!"
    else:
        st.session_state.balance -= bet
        msg = f"결과: {result}\n❌ 틀렸습니다."
    show_result(msg)

# ---------------- UI ----------------

st.title("🎰 도박 게임 허브 (1인용)")

# 💰 현재 잔액 항상 표시
st.subheader(f"💵 현재 잔액: {st.session_state.balance:,}원")

# 💥 파산 확인
if st.session_state.balance <= 0:
    st.error("💸 파산! 잔액이 0원입니다.")
    st.warning("📞 도박 중독이 의심되면 도움을 요청하세요.\n**상담번호: ☎️ 1336**")
    st.markdown("[👉 도박문제관리센터 바로가기](https://www.ncadd.or.kr)", unsafe_allow_html=True)
    st.stop()

# 🎮 게임 선택
game = st.selectbox("게임을 선택하세요", ["슬롯머신", "하이/로우", "주사위 홀짝", "룰렛", "홀짝 합", "사다리"])
bet = get_bet()

# 게임별 입력 및 실행
if game == "슬롯머신":
    if st.button("🎰 슬롯 돌리기"):
        slot_machine(bet)

elif game == "하이/로우":
    guess = st.radio("상대가 더 높을까 낮을까?", ["high", "low"])
    if st.button("🃏 예측하기"):
        high_or_low(bet, guess)

elif game == "주사위 홀짝":
    guess = st.radio("홀수 or 짝수?", ["odd", "even"])
    if st.button("🎲 던지기"):
        dice_game(bet, guess)

elif game == "룰렛":
    choice = st.text_input("숫자(0~36) 또는 색상(red/black):").lower()
    if st.button("🎡 돌리기"):
        roulette(bet, choice)

elif game == "홀짝 합":
    user_num = st.number_input("당신의 숫자 (1~9)", min_value=1, max_value=9, step=1)
    guess = st.radio("합은 홀수 or 짝수?", ["odd", "even"])
    if st.button("⚖️ 예측하기"):
        odd_even_sum(bet, user_num, guess)

elif game == "사다리":
    choice = st.radio("사다리 방향 선택", ["left", "right"])
    if st.button("🪜 선택하기"):
        ladder_game(bet, choice)

# 결과 출력
if st.session_state.message:
    st.success(st.session_state.message)
