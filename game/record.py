from datetime import datetime

from config import RANKING_LIMIT


def _parse_time(value):
    try:
        return datetime.fromisoformat(value)
    except (TypeError, ValueError):
        return datetime.min


def _sorted_records(records):
    return sorted(
        records,
        key=lambda item: (item["score"], _parse_time(item["time"])),
        reverse=True,
    )


def _serialize_time(value):
    if isinstance(value, datetime):
        return value.isoformat(timespec="seconds")

    if isinstance(value, str) and value.strip():
        return value.strip()

    return datetime.now().isoformat(timespec="seconds")


def add_record(state, name, score, played_at=None):
    entry = {
        "name": (name or "UNKNOWN").strip() or "UNKNOWN",
        "score": int(score),
        "time": _serialize_time(played_at),
    }

    state.setdefault("rankings", []).append(entry.copy())
    state.setdefault("history", []).append(entry.copy())
    return entry


def get_top_rankings(state, limit=RANKING_LIMIT):
    return _sorted_records(state.get("rankings", []))[:limit]


def get_personal_history(state, name):
    target = (name or "").strip().casefold()
    history = state.get("history", [])
    filtered = [record for record in history if record["name"].casefold() == target]
    return _sorted_records(filtered)


def format_record(record):
    played_at = _parse_time(record["time"]).strftime("%Y-%m-%d %H:%M:%S")
    return f'{record["name"]} | 점수: {record["score"]} | 플레이: {played_at}'
