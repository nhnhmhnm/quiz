def list_quizzes(state):
    return state.get("quizzes", [])


def add_quiz(state, question, answer):
    question = (question or "").strip()
    answer = (answer or "").strip()

    if not question or not answer:
        raise ValueError("문제와 정답은 모두 비어 있을 수 없습니다.")

    quiz = {"question": question, "answer": answer}
    state.setdefault("quizzes", []).append(quiz)
    return quiz


def delete_quiz(state, index):
    quizzes = state.get("quizzes", [])

    if index < 1 or index > len(quizzes):
        raise IndexError("삭제할 문제 번호가 올바르지 않습니다.")

    return quizzes.pop(index - 1)
