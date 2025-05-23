from meowtiwhitelist.operations import (
    add_whitelist_direct as _raw_add_whitelist_direct,
    add_whitelist as _raw_add_whitelist,
    remove_whitelist as _raw_remove_whitelist
)
from meowtiwhitelist.utils.service_loader_utils import build_service_mapping
from meowtiwhitelist.utils.uuid_utils import fetchers


def get_player_uuid(player_name: str, service_id: str):
    """
    Get the UUID of a player using the specified service.

    Args:
        player_name (str): The name of the player.
        service_id (str): The ID of the service to use for fetching the UUID.

    Returns:
        str: The UUID of the player.
    """
    return fetchers[build_service_mapping()[service_id.strip().lower()]](player_name)


def add_whitelist_direct(src, player_name: str, uuid: str):
    """
    Add a player to the whitelist using the specified UUID.
    This is a direct method. It does not check for player name and UUID validity.

    Args:
        src: The source of the command (e.g., console or player).
        player_name (str): The name of the player to add to the whitelist.
        uuid (str): The UUID of the player.
    """
    _raw_add_whitelist_direct(src, player_name, uuid)


def add_whitelist(src, player_name: str, service_id: str):
    """
    Add a player to the whitelist using the specified service.

    Args:
        src: The source of the command (e.g., console or player).
        player_name (str): The name of the player to add to the whitelist.
        service_id (str): The ID of the service to use for fetching the UUID.
    """
    _raw_add_whitelist(src, player_name, service_id)


def remove_whitelist(src, player_name: str):
    """
    Remove a player from the whitelist.

    Args:
        src: The source of the command (e.g., console or player).
        player_name (str): The name of the player to remove from the whitelist.
    """
    _raw_remove_whitelist(src, player_name)