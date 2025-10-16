import requests
import re
from typing import Optional, Dict, Union

from meowtiwhitelist.utils.service_loader_utils import services

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

def get_mojang_uuid(username: str) -> Optional[str]:
    url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    response = requests.get(url, timeout=5)
    if response.status_code == 200:
        return _format_uuid(response.json().get("id", ""))
    return None

def get_blessing_skin_uuid(username: str, api_root: str) -> Union[int, str, None]:
    url = f"{api_root.rstrip('/')}/api/profiles/minecraft"
    response = requests.post(url, json=[username], timeout=5)
    if response.status_code == 200:
        items = response.json()
        if items and isinstance(items, list) and len(items) > 0:
            return _format_uuid(items[0].get("id", ""))
    else:
        return response.status_code
    return None

def get_custom_yggdrasil_uuid(username: str, url: str, method: str = 'GET') -> Union[str, None]:
    if method.upper() == 'POST':
        response = requests.post(url, json=[username], timeout=5)
    elif method.upper() == 'GET':
        url = f"{url.rstrip('/')}/{username}"
        response = requests.get(url, timeout=5)
    else:
        return None

    if response.status_code == 200:
        items = response.json()
        if method.upper() == 'POST':
            if items and isinstance(items, list) and len(items) > 0:
                return _format_uuid(items[0].get("id", ""))
        else:
            return _format_uuid(items.get("id", ""))
    return None

class UUIDFetcher:
    @staticmethod
    def create_fetchers(services) -> Dict[int, callable]:
        fetchers = {}
        for service in services:
            service_id = service.get("id", -1)
            service_type = service.get("serviceType", "").upper()
            api_root = service.get("yggdrasilAuth", {}).get("blessingSkin", {}).get("apiRoot", "")
            url = service.get("custom", {}).get("url", "")
            method = service.get("custom", {}).get("method", "GET")

            if service_type == "MOJANG":
                fetchers[service_id] = get_mojang_uuid
            elif service_type == "BLESSING_SKIN":
                fetchers[service_id] = lambda username, root=api_root: get_blessing_skin_uuid(username, root)
            elif service_type == "CUSTOM_YGGDRASIL":
                fetchers[service_id] = lambda username, u=url, m=method: get_custom_yggdrasil_uuid(username, u, m)
        return fetchers

fetchers = UUIDFetcher.create_fetchers(services)