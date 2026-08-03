import random

from config import QUIZ_COUNT
from game.record import add_record


def _normalize_text(value):
    return " ".join(str(value).strip().casefold().split())


def _is_correct_text(user_answer, expected_answer):
    expected_options = [
        _normalize_text(option)
        for option in str(expected_answer).split("|")
        if option.strip()
    ]
    return _normalize_text(user_answer) in expected_options


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


def _play_short_answer_quiz(quiz, index, question_count):
    print(f"[{index}/{question_count}] {quiz['question']}")
    user_answer = input("정답: ").strip()
    correct_text = quiz["answer"].split("|", 1)[0]
    return _is_correct_text(user_answer, quiz["answer"]), correct_text


def play_quiz(state):
    quizzes = state.get("quizzes", [])

    if not quizzes:
        print("등록된 퀴즈가 없어 게임을 시작할 수 없습니다.")
        return None

    question_count = min(QUIZ_COUNT, len(quizzes))
    selected_quizzes = random.sample(quizzes, question_count)
    score = 0

    print(f"\n퀴즈를 시작합니다. 총 {question_count}문제입니다.\n")

    for index, quiz in enumerate(selected_quizzes, start=1):
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
    name = input("랭킹에 등록할 이름을 입력하세요: ").strip() or "UNKNOWN"
    entry = add_record(state, name, score)
    print(f"플레이 기록이 저장되었습니다. ({entry['time']})")
    return entry
