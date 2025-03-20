import time

from mcdreforged.plugin.si.plugin_server_interface import PluginServerInterface
from mcdreforged.plugin.si.server_interface import ServerInterface

from meowtiwhitelist.utils.config_utils import server_dirname
from meowtiwhitelist.utils.logger_utils import log, log_available_services, log_conflict_errors
from meowtiwhitelist.utils.uuid_utils.service_loader import build_service_mapping, service_conflicts
from meowtiwhitelist.utils.uuid_utils.uuid_utils import fetchers
from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.utils.file_utils import (
    get_backup_dir,
    get_backup_whitelist_path,
    get_whitelist_path,
    move_existing_whitelist,
    write_new_whitelist,
    clean_old_backups,
    json_file_to_list
)


def create_whitelist_file(json_list: list, workpath: str, type: str):
    backup_dir = get_backup_dir(workpath)
    backup_whitelist_path = get_backup_whitelist_path(backup_dir, type)
    whitelist_path = get_whitelist_path(workpath)

    move_existing_whitelist(whitelist_path, backup_whitelist_path)
    write_new_whitelist(whitelist_path, json_list)
    clean_old_backups(backup_dir)


def add_whitelist(src, player_name: str, service_id: str):
    if service_conflicts:
        log_conflict_errors(src, service_conflicts)
        return

    player_name = player_name.strip()
    if not player_name:
        log(src, tr("error.empty_username"))
        return

    service_map = build_service_mapping()
    normalized_service = service_id.strip().lower()

    if normalized_service not in service_map:
        log(src, tr("error.invalid_service"))
        log_available_services(src)
        return

    service_id = service_map[normalized_service]

    if (uuid_func := fetchers.get(service_id)) is None:
        log(src, tr("error.service_not_configured", service_id))
        return

    whitelist_path = get_whitelist_path(server_dirname)
    whitelist_list: list = json_file_to_list(whitelist_path)
    whitelist_name_list = {entry['name'] for entry in whitelist_list}

    if player_name in whitelist_name_list:
        log(src, tr("error.duplicate_name", player_name))
    else:
        uuid = uuid_func(player_name)
        if isinstance(uuid, int):
            log(src, tr("error.service_status_code", uuid))
        elif uuid is not None:
            new_whitelist_dict = {'uuid': uuid, 'name': player_name}
            whitelist_list.append(new_whitelist_dict)
            create_whitelist_file(whitelist_list, server_dirname, '_A_')
            time.sleep(1)
            server_cmd(src, 'whitelist reload')
            log(src, tr("success.add", player_name))
        else:
            log(src, tr("error.unknown_error", player_name))


def remove_whitelist(src, player_name: str):
    whitelist_path = get_whitelist_path(server_dirname)
    whitelist_list: list = json_file_to_list(whitelist_path)
    player_entry = next((entry for entry in whitelist_list if entry['name'] == player_name), None)
    if player_entry:
        whitelist_list.remove(player_entry)
        create_whitelist_file(whitelist_list, server_dirname, '_R_')
        log(src, tr("success.remove", player_name))
    else:
        log(src, tr("error.not_found", player_name))


def list_whitelist(src):
    whitelist_path = get_whitelist_path(server_dirname)
    whitelist_list: list = json_file_to_list(whitelist_path)
    log(src, tr("list"))
    for i, entry in enumerate(whitelist_list, 1):
        player_name, player_uuid = entry['name'], entry['uuid']
        log(src, f'{i}: {player_name} - {player_uuid}')


def reload_plugin(src, server: PluginServerInterface):
    ServerInterface.reload_plugin(server, "meowtiwhitelist")
    server_cmd(src, 'whitelist reload')
    log(src, tr("success.reload"))


def server_cmd(src, command: str):
    src.get_server().execute(command)