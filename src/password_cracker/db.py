from __future__ import annotations

import hmac
import json
from pathlib import Path
from typing import Dict

DEFAULT_DATABASE: Dict[str, str] = {
    "test user 1": "ez pswd",
    "test user 2": "super difficult password probably",
}

DATABASE_FILE = Path.cwd() / "password_cracker_db.json"
password_database: Dict[str, str] = {}


def _load_database() -> Dict[str, str]:
    if DATABASE_FILE.exists():
        try:
            with DATABASE_FILE.open("r", encoding="utf-8") as handle:
                data = json.load(handle)
                return {str(user): str(password) for user, password in data.items()}
        except (OSError, ValueError):
            pass
    return DEFAULT_DATABASE.copy()


password_database = _load_database()


def list_users() -> list[str]:
    return sorted(password_database.keys())


def has_user(user: str) -> bool:
    return user in password_database


def get_password(user: str) -> str | None:
    return password_database.get(user)


def set_password(user: str, password: str) -> None:
    password_database[user] = password


def save_password_database() -> None:
    with DATABASE_FILE.open("w", encoding="utf-8") as handle:
        json.dump(password_database, handle, indent=2)


def check_password(user: str, guess: str) -> bool:
    actual = password_database.get(user)
    if actual is None:
        return False
    if len(guess) != len(actual):
        return False
    for expected_char, actual_char in zip(guess, actual):
        if expected_char != actual_char:
            return False
    return True


def check_password_cpython(user: str, guess: str) -> bool:
    actual = password_database.get(user)
    if actual is None:
        return False
    return guess == actual


def check_password_constant_time(user: str, guess: str) -> bool:
    actual = password_database.get(user)
    if actual is None:
        return False
    return hmac.compare_digest(guess, actual)
