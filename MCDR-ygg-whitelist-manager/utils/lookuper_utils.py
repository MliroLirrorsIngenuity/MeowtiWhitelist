import asyncio
import aiohttp
import json
import re
from typing import Dict, Optional, Any
from logger_utils import log

_UUID_PATTERN = re.compile(
    r"([a-fA-F0-9]{8})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{4})"
    r"([a-fA-F0-9]{12})"
)

async def _fetch_json(session: aiohttp.ClientSession, method: str, url: str, **kwargs) -> Optional[Any]:
    try:
        async with session.request(method, url, **kwargs) as response:
            text = await response.text()
            return json.loads(text)
    except Exception as e:
        log(f"Error during fetching {url}: {e}", level="error")
        return None

def _format_uuid(raw_id: str) -> str:
    m = _UUID_PATTERN.search(raw_id)
    if m:
        return f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}-{m.group(5)}"
    else:
        log(f"Invalid UUID format: {raw_id}", level="warning")
        return ""

# LittleSkin API
async def fetch_littleskin_uuid(session: aiohttp.ClientSession, username: str) -> Optional[str]:
    littleskin_url = "https://littleskin.cn/api/yggdrasil/api/profiles/minecraft"
    body = [username]
    try:
        async with session.post(littleskin_url, json=body) as response:
            response_text = await response.text()
            items = json.loads(response_text)
            if items and isinstance(items, list) and len(items) > 0:
                for item in items:
                    item_id = item.get("id", "")
                    formatted = _format_uuid(item_id)
                    if formatted:
                        return formatted
    except Exception as e:
        log(f"Error fetching LittleSkin API: {e}", level="error")
    return None

# Mojang API
async def fetch_mojang_uuid(session: aiohttp.ClientSession, username: str) -> Optional[str]:
    mojang_url = f"https://api.mojang.com/users/profiles/minecraft/{username}"
    mojang_item = await _fetch_json(session, "GET", mojang_url)
    if mojang_item and isinstance(mojang_item, dict):
        item_id = mojang_item.get("id", "")
        return _format_uuid(item_id)
    return None

VALIDATORS = {
    "littleskin": fetch_littleskin_uuid,
    "mojang": fetch_mojang_uuid,
}

async def get_uuid_info(username: str) -> Dict[str, str]:
    result = {"username": username}
    async with aiohttp.ClientSession() as session:
        for platform, fetch_func in VALIDATORS.items():
            uuid = await fetch_func(session, username)
            if uuid:
                result[f"{platform}_uuid"] = uuid

    return result

def get_uuid_info_sync(username: str) -> Dict[str, str]:
    return asyncio.run(get_uuid_info(username))