import random

from config import QUIZ_COUNT
from game.record import add_record


# 대소문자와 공백 차이로 정답 판정이 흔들리지 않도록 문자열을 정리한다.
def _normalize_text(value):
    return " ".join(str(value).strip().casefold().split())


# 예전 주관식 형식도 호환할 수 있게 남겨둔 정답 비교 함수다.
def _is_correct_text(user_answer, expected_answer):
    expected_options = [
        _normalize_text(option)
        for option in str(expected_answer).split("|")
        if option.strip()
    ]
    return _normalize_text(user_answer) in expected_options


# 객관식 문제 1개를 출력하고 정답 여부와 정답 문구를 돌려준다.
def _play_multiple_choice_quiz(quiz, index, question_count):
    print(f"[{index}/{question_count}] {quiz['question']}")
    for choice_index, choice in enumerate(quiz["choices"], start=1):
        print(f"{choice_index}. {choice}")

    user_answer = input("정답 번호(1~4): ").strip()

    try:
        selected = int(user_answer)
    except ValueError:
        selected = 0

    is_correct = selected == quiz["answer_index"]
    correct_text = quiz["choices"][quiz["answer_index"] - 1]
    return is_correct, correct_text


# 호환성을 위해 남겨둔 주관식 플레이 함수다.
def _play_short_answer_quiz(quiz, index, question_count):
    print(f"[{index}/{question_count}] {quiz['question']}")
    user_answer = input("정답: ").strip()
    correct_text = quiz["answer"].split("|", 1)[0]
    return _is_correct_text(user_answer, quiz["answer"]), correct_text


def _prompt_player_name():
    while True:
        name = input("랭킹에 등록할 이름을 입력하세요: ").strip()
        if name:
            return name
        print("이름은 비워둘 수 없습니다.")


# 등록된 문제 중 일부를 랜덤으로 뽑아 게임을 진행하고 점수를 기록한다.
def play_quiz(state):
    quizzes = state.get("quizzes", [])

    if not quizzes:
        print("등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")
        return None

    # 문제가 10개보다 적더라도 에러 없이 플레이할 수 있게 최소값을 사용한다.
    question_count = min(QUIZ_COUNT, len(quizzes))
    selected_quizzes = random.sample(quizzes, question_count)
    score = 0

    print(f"\n퀴즈를 시작합니다. 총 {question_count}문제입니다.\n")

    for index, quiz in enumerate(selected_quizzes, start=1):
        # 현재는 객관식 중심이지만, 예전 형식이 섞여 있어도 동작하도록 분기한다.
        if "choices" in quiz and "answer_index" in quiz:
            is_correct, correct_text = _play_multiple_choice_quiz(quiz, index, question_count)
        else:
            is_correct, correct_text = _play_short_answer_quiz(quiz, index, question_count)

        if is_correct:
            score += 1
            print("정답입니다.\n")
        else:
            print(f"오답입니다. 정답: {correct_text}\n")

    print(f"최종 점수: {score} / {question_count}")
    name = _prompt_player_name()
    entry = add_record(state, name, score)
    print(f"플레이 기록이 저장되었습니다. ({entry['time']})")
    return entry
