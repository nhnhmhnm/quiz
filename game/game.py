import random

from config import QUIZ_COUNT
from game.record import add_record


def _normalize_text(value):
    return " ".join(str(value).strip().casefold().split())


def _is_correct(user_answer, expected_answer):
    expected_options = [
        _normalize_text(option)
        for option in str(expected_answer).split("|")
        if option.strip()
    ]
    return _normalize_text(user_answer) in expected_options


def play_quiz(state):
    quizzes = state.get("quizzes", [])

    if not quizzes:
        print("등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")
        return None

    name = input("이름을 입력하세요: ").strip() or "UNKNOWN"
    question_count = min(QUIZ_COUNT, len(quizzes))
    selected_quizzes = random.sample(quizzes, question_count)
    score = 0

    print(f"\n{name}님의 퀴즈를 시작합니다. 총 {question_count}문제입니다.\n")

    for index, quiz in enumerate(selected_quizzes, start=1):
        print(f"[{index}/{question_count}] {quiz['question']}")
        user_answer = input("정답: ").strip()

        if _is_correct(user_answer, quiz["answer"]):
            score += 1
            print("정답입니다.\n")
        else:
            expected = quiz["answer"].split("|", 1)[0]
            print(f"오답입니다. 정답: {expected}\n")

    entry = add_record(state, name, score)
    print(f"{name}님의 최종 점수: {score} / {question_count}")
    print(f"플레이 기록이 저장되었습니다. ({entry['time']})")
    return entry
