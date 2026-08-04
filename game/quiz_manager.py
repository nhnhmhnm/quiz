# 현재 등록된 퀴즈 목록을 그대로 반환한다.
def list_quizzes(state):
    return state.get("quizzes", [])


# 새 객관식 문제를 추가하기 전에 입력값이 올바른지 검사한다.
def add_quiz(state, question, choices, answer_index):
    question = (question or "").strip()

    if not question:
        raise ValueError("문제는 비어 있을 수 없습니다.")

    if not isinstance(choices, list) or len(choices) != 4:
        raise ValueError("보기는 4개여야 합니다.")

    normalized_choices = [str(choice).strip() for choice in choices]
    if any(not choice for choice in normalized_choices):
        raise ValueError("보기는 모두 입력해야 합니다.")

    try:
        answer_index = int(answer_index)
    except (TypeError, ValueError) as error:
        raise ValueError("정답 번호는 1~4 사이여야 합니다.") from error

    if answer_index < 1 or answer_index > 4:
        raise ValueError("정답 번호는 1~4 사이여야 합니다.")

    quiz = {
        "question": question,
        "choices": normalized_choices,
        "answer_index": answer_index,
    }
    state.setdefault("quizzes", []).append(quiz)
    return quiz


# 메뉴에서 보이는 번호(1부터 시작)를 실제 리스트 인덱스로 바꿔 삭제한다.
def delete_quiz(state, index):
    quizzes = state.get("quizzes", [])

    if index < 1 or index > len(quizzes):
        raise IndexError("삭제할 문제 번호가 올바르지 않습니다.")

    return quizzes.pop(index - 1)
