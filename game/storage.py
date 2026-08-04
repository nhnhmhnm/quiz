import json
import os
from copy import deepcopy

from config import DEFAULT_QUIZZES, ENCODING, STATE_FILE


# 상태 파일이 없거나 읽을 수 없을 때 사용할 기본 구조다.
def _default_state():
    return {
        "quizzes": deepcopy(DEFAULT_QUIZZES),
        "rankings": [],
        "history": [],
    }


# 객관식 보기가 정확히 4개인지 확인하면서 공백을 정리한다.
def _normalize_choices(choices):
    if not isinstance(choices, list):
        return None

    normalized = [str(choice).strip() for choice in choices if str(choice).strip()]
    if len(normalized) != 4:
        return None

    return normalized


# state.json 안의 퀴즈 데이터를 현재 프로그램 형식에 맞춰 정리한다.
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

        # 예전 주관식 형식은 더 이상 사용하지 않아 주석 처리했다.
        # answer = str(quiz.get("answer", "")).strip()
        # if answer:
        #     normalized.append({"question": question, "answer": answer})

    return normalized


# 랭킹/기록 데이터도 타입과 필수 값만 남기도록 정리한다.
def _normalize_records(records):
    normalized = []

    if not isinstance(records, list):
        return normalized

    for record in records:
        if not isinstance(record, dict):
            continue

        name = str(record.get("name", "")).strip()

        try:
            score = int(record.get("score", 0))
        except (TypeError, ValueError):
            score = 0

        played_at = str(record.get("time", "")).strip()
        if not name or not played_at:
            continue

        normalized.append({"name": name, "score": score, "time": played_at})

    return normalized


# 파일에서 읽은 전체 상태를 정리해서 프로그램이 안전하게 사용할 수 있게 만든다.
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


# 저장 파일이 있으면 불러오고, 없거나 손상됐으면 기본 상태로 시작한다.
def load_state():
    if not os.path.exists(STATE_FILE):
        return _default_state()

    try:
        with open(STATE_FILE, "r", encoding=ENCODING) as file:
            return _normalize_state(json.load(file))
    except (json.JSONDecodeError, OSError):
        print("상태 파일을 읽지 못해 기본 데이터로 시작합니다.")
        return _default_state()


# 저장할 때도 한 번 더 정규화해서 잘못된 데이터가 파일에 남지 않게 한다.
def save_state(state):
    with open(STATE_FILE, "w", encoding=ENCODING) as file:
        json.dump(_normalize_state(state), file, ensure_ascii=False, indent=2)
