from datetime import datetime

from config import RANKING_LIMIT


# 문자열 시간을 datetime으로 바꿔 정렬에 사용한다.
def _parse_time(value):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return datetime.min


# 점수가 높은 순, 동점이면 더 최근 기록이 먼저 오도록 정렬한다.
def _sorted_records(records):
    return sorted(
        records,
        key=lambda item: (item["score"], _parse_time(item["time"])),
        reverse=True,
    )


# 입력된 시간 값이 문자열이든 datetime이든 같은 형식으로 맞춘다.
def _serialize_time(value):
    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")

    if isinstance(value, str) and value.strip():
        return value.strip()

    return datetime.now().isoformat(timespec="seconds")


# 한 번의 플레이 결과를 rankings와 history에 동시에 저장한다.
def add_record(state, name, score, played_at=None):
    entry = {
        "name": (name or "UNKNOWN").strip() or "UNKNOWN",
        "score": int(score),
        "time": _serialize_time(played_at),
    }

    state.setdefault("rankings", []).append(entry.copy())
    state.setdefault("history", []).append(entry.copy())
    return entry


# 메인 화면에 보여줄 상위 랭킹만 잘라서 돌려준다.
def get_top_rankings(state, limit=RANKING_LIMIT):
    return _sorted_records(state.get("rankings", []))[:limit]


# 같은 이름으로 저장된 플레이 기록만 모아 보여준다.
def get_personal_history(state, name):
    target = (name or "").strip().casefold()
    history = state.get("history", [])
    filtered = [record for record in history if record["name"].casefold() == target]
    return _sorted_records(filtered)


# 기록 화면에 바로 출력할 수 있는 문자열 형식으로 바꾼다.
def format_record(record):
    played_at = _parse_time(record["time"]).strftime("%Y-%m-%d %H:%M:%S")
    return f'{record["name"]} | 점수: {record["score"]} | 플레이: {played_at}'
