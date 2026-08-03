import json
import os
from copy import deepcopy

from config import DEFAULT_QUIZZES, ENCODING, STATE_FILE


def _default_state():
    return {
        "quizzes": deepcopy(DEFAULT_QUIZZES),
        "rankings": [],
        "history": [],
    }


def _normalize_choices(choices):
    if not isinstance(choices, list):
        return None

    normalized = [str(choice).strip() for choice in choices if str(choice).strip()]
    if len(normalized) != 4:
        return None

    return normalized


def _normalize_quizzes(quizzes):
    normalized = []

    if not isinstance(quizzes, list):
        return normalized

    for quiz in quizzes:
        if not isinstance(quiz, dict):
            continue

        question = str(quiz.get("question", "")).strip()
        if not question:
            continue

        choices = _normalize_choices(quiz.get("choices"))
        answer_index = quiz.get("answer_index")

        if choices is not None:
            try:
                answer_index = int(answer_index)
            except (TypeError, ValueError):
                continue

            if 1 <= answer_index <= 4:
                normalized.append(
                    {
                        "question": question,
                        "choices": choices,
                        "answer_index": answer_index,
                    }
                )
            continue

        answer = str(quiz.get("answer", "")).strip()
        if answer:
            normalized.append({"question": question, "answer": answer})

    return normalized


def _normalize_records(records):
    normalized = []

    if not isinstance(records, list):
        return normalized

    for record in records:
        if not isinstance(record, dict):
            continue

        name = str(record.get("name", "UNKNOWN")).strip() or "UNKNOWN"

        try:
            score = int(record.get("score", 0))
        except (TypeError, ValueError):
            score = 0

        played_at = str(record.get("time", "")).strip()
        if not played_at:
            continue

        normalized.append({"name": name, "score": score, "time": played_at})

    return normalized


def _normalize_state(state):
    if not isinstance(state, dict):
        return _default_state()

    quizzes = _normalize_quizzes(state.get("quizzes", []))
    if not quizzes:
        quizzes = deepcopy(DEFAULT_QUIZZES)

    return {
        "quizzes": quizzes,
        "rankings": _normalize_records(state.get("rankings", [])),
        "history": _normalize_records(state.get("history", [])),
    }


def load_state():
    if not os.path.exists(STATE_FILE):
        return _default_state()

    try:
        with open(STATE_FILE, "r", encoding=ENCODING) as file:
            return _normalize_state(json.load(file))
    except (json.JSONDecodeError, OSError):
        print("상태 파일을 읽지 못해 기본 데이터로 시작합니다.")
        return _default_state()


def save_state(state):
    with open(STATE_FILE, "w", encoding=ENCODING) as file:
        json.dump(_normalize_state(state), file, ensure_ascii=False, indent=2)
