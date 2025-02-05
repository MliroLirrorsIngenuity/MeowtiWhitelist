from mcdr_ygg_whitelist_manager.utils.file_utils import *
from mcdr_ygg_whitelist_manager.utils.logger import *
from mcdr_ygg_whitelist_manager.utils.lookuper import *
from mcdr_ygg_whitelist_manager.utils.translater import *

server_dirname = 'server'
world_dirname = 'world'


def server_cmd(src, command: str):
    src.get_server().execute(command)


def json_file_to_list(json_path: str) -> list:
    with open(json_path, 'r', encoding='UTF-8') as file:
        output_dict = json.load(file)
    return output_dict


def create_whitelist_file(json_list: list, workpath: str, type: str):
    backup_dir = get_backup_dir(workpath)
    backup_whitelist_path = get_backup_whitelist_path(backup_dir, type)
    whitelist_path = os.path.join(workpath, 'whitelist.json')

    move_existing_whitelist(whitelist_path, backup_whitelist_path)

    write_new_whitelist(whitelist_path, json_list)

    clean_old_backups(backup_dir)


def get_playerdata_filename_list():
    filename_all = os.listdir(os.path.join(server_dirname, world_dirname, 'playerdata'))
    playerdata_name_list = []
    for filename in filename_all:
        if filename[-4:] == '.dat':
            playerdata_name_list.append(str(filename.split('.dat')[0]))
    return playerdata_name_list


def add_whitelist(src, player_name: str, api: str):
    api_methods = {
        1: get_mojang_uuid_sync,
        2: get_littleskin_uuid_sync
    }
    if api.casefold() == 'mojang':
        api = 1
    elif api.casefold() == 'littleskin':
        api = 2
    elif api.isdigit() and int(api) in api_methods:
        api = int(api)
    else:
        log(src, tr("error.invalid_api"))
        log(src,tr("help_msg"))
        return

    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    whitelist_name_list = []
    for value in whitelist_list:
        whitelist_name_list.append(value['name'])

    if player_name in whitelist_name_list:
        log(src, tr("error.duplicate_name", player_name))
    else:
        uuid = api_methods.get(api, None)(player_name)

        if uuid is not None:
            new_whitelist_dict = {'uuid': uuid, 'name': player_name}
            whitelist_list.append(new_whitelist_dict)
            create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_A_')
            time.sleep(1)
            server_cmd(src, '/whitelist reload')
            log(src, tr("success.add", player_name))
        else:
            log(src, tr("error.unknown_error", player_name))


def remove_whitelist(src, player_name: str):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    player_entry = next((entry for entry in whitelist_list if entry['name'] == player_name), None)
    if player_entry:
        whitelist_list.remove(player_entry)
        create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_R_')
        log(src, tr("success.remove", player_name))
    else:
        log(src, tr("error.not_found", player_name))


def list_whitelist(src):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    log(src, tr("list"))
    for i in range(0, len(whitelist_list)):
        player_name, player_uuid = whitelist_list[i]['name'], whitelist_list[i]['uuid']
        log(src, f'{i+1}: {player_name} - {player_uuid}')