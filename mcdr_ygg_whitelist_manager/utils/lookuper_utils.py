import requests
import re
from typing import Optional


_UUID_PATTERN = re.compile(
    r"([a-fA-F0-9]{8})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{12})"
)


def _format_uuid(raw_id: str) -> str:
    m = _UUID_PATTERN.search(raw_id)
    return f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}-{m.group(5)}" if m else ""


def get_littleskin_uuid_sync(username: str) -> Optional[str]:
    url = "https://littleskin.cn/api/yggdrasil/api/profiles/minecraft"
    response = requests.post(url, json=[username], timeout=5)
    if response.status_code == 200:
        items = response.json()
        if items and isinstance(items, list) and len(items) > 0:
            return _format_uuid(items[0].get("id", ""))
    return None


def get_mojang_uuid_sync(username: str) -> Optional[str]:
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return _format_uuid(response.json().get("id", ""))
    return None


# def get_example_uuid_sync(username: str) -> Optional[str]:
#     url = "https://example.com/api/yggdrasil/api/profiles/minecraft"
#     response = requests.post(url, json=[username], timeout=5)
#     if response.status_code == 200:
#         items = response.json()
#         if items and isinstance(items, list) and len(items) > 0:
#             return _format_uuid(items[0].get("id", ""))
#     return None