from meowtiwhitelist.operations import (
    add_whitelist as _raw_add_whitelist,
    remove_whitelist as _raw_remove_whitelist
)
from meowtiwhitelist.utils.uuid_utils.service_loader import build_service_mapping
from meowtiwhitelist.utils.uuid_utils.uuid_utils import fetchers


def get_player_uuid(player_name: str, service_id: str):
    return fetchers[build_service_mapping()[service_id.strip().lower()]](player_name)


def add_whitelist(src, player_name: str, service_id: str):
    _raw_add_whitelist(src, player_name, service_id)


def remove_whitelist(src, player_name: str):
    _raw_remove_whitelist(src, player_name)