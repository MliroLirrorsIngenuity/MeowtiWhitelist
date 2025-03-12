from typing import Optional

from meowtiwhitelist import tr
from meowtiwhitelist.utils.logger_utils import log
from meowtiwhitelist.utils.uuid_utils.uuid_utils import fetchers


def get_player_uuid(src, service_id: int, player_name: str) -> Optional[str]:
    if service_id not in fetchers:
        log(src, tr("api.error.not_configured", service_id))
        return None

    uuid_func = fetchers[service_id]
    uuid = uuid_func(player_name)

    if isinstance(uuid, int):
        log(src, tr("api.error.status_code", uuid))
        return None
    elif uuid is None:
        log(src, tr("api.error.unknown_error", player_name))
        return None

    return uuid