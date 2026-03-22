# subscription management module for ai-daily-brief

"""
This module provides simple functions to manage a list of subscriber email
addresses stored in a JSON file. In a production system you would probably
use a database, but for this minimal viable product a JSON file is enough.
"""

import json
import os
from typing import List

# Path to the JSON file storing subscriber addresses. By default it is
# placed in the project root under `data/subscribers.json`. The directory
# is created on first use.
_SUBSCRIBERS_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "subscribers.json")


def _ensure_file_exists() -> None:
    """Make sure the JSON file and its parent directory exist.
    If the file does not exist it is created with an empty list.
    """
    directory = os.path.dirname(_SUBSCRIBERS_PATH)
    os.makedirs(directory, exist_ok=True)
    if not os.path.isfile(_SUBSCRIBERS_PATH):
        with open(_SUBSCRIBERS_PATH, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_subscribers() -> List[str]:
    """Return the list of subscriber email addresses.
    The file is created if it does not yet exist.
    """
    _ensure_file_exists()
    with open(_SUBSCRIBERS_PATH, "r", encoding="utf-8") as f:
        try:
            data = json.load(f)
            if isinstance(data, list):
                return data
            # If the file contains something else, reset it.
            return []
        except json.JSONDecodeError:
            return []


def save_subscribers(subscribers: List[str]) -> None:
    """Persist the list of subscribers to the JSON file."""
    _ensure_file_exists()
    # Ensure uniqueness and strip whitespace
    clean = list({s.strip() for s in subscribers if s.strip()})
    with open(_SUBSCRIBERS_PATH, "w", encoding="utf-8") as f:
        json.dump(clean, f, indent=2)


def add_subscriber(email: str) -> None:
    """Add a new email address to the subscriber list.
    Duplicate addresses are ignored.
    """
    email = email.strip()
    if not email:
        return
    subscribers = load_subscribers()
    if email not in subscribers:
        subscribers.append(email)
        save_subscribers(subscribers)


def remove_subscriber(email: str) -> None:
    """Remove an email address from the subscriber list if present."""
    email = email.strip()
    if not email:
        return
    subscribers = load_subscribers()
    if email in subscribers:
        subscribers.remove(email)
        save_subscribers(subscribers)

if __name__ == "__main__":
    # Simple manual test when run directly
    print("current subscribers:", load_subscribers())
    test_email = "test@example.com"
    print(f"adding {test_email}")
    add_subscriber(test_email)
    print("after add:", load_subscribers())
    print(f"removing {test_email}")
    remove_subscriber(test_email)
    print("after remove:", load_subscribers())
