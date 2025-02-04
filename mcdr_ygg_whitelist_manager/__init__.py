import shutil
import time
import json
import os
from .utils import *

server_dirname = 'server'
world_dirname = 'world'
api_methods = {
    1: get_mojang_uuid_sync,
    2: get_littleskin_uuid_sync
}


def on_load(server: PluginServerInterface, prev):
    server.register_help_message('!!whitelist', '白名单管理插件')


def server_cmd(info: Info, command: str):
    info.get_server().execute(command)


def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def json_file_to_list(json_path: str) -> list:
    with open(json_path, 'r', encoding='UTF-8') as file:
        output_dict = json.load(file)
    return output_dict


def create_whitelist_file(json_list: list, workpath: str, type: str):
    format_time = time.strftime('%y-%m-%d_%H-%M-%S', time.localtime())
    check_dir(os.path.join(workpath, 'whitelist_backup'))
    backup_whitelist_name = format_time + type + 'whitelist.json'
    shutil.move(os.path.join(workpath, 'whitelist.json'), os.path.join(workpath, 'whitelist_backup', backup_whitelist_name))

    file_name: str = os.path.join(workpath, 'whitelist.json')
    with open(file_name, 'w', encoding='UTF-8') as file:
        file.write(json.dumps(json_list, indent=4, ensure_ascii=False))


def get_playerdata_filename_list():
    filename_all = os.listdir(os.path.join(server_dirname, world_dirname, 'playerdata'))
    playerdata_name_list = []
    for filename in filename_all:
        if filename[-4:] == '.dat':
            playerdata_name_list.append(str(filename.split('.dat')[0]))
    return playerdata_name_list


def list_whitelist(info: Info):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    log(info, '===== 白名单 =====：')
    for i in range(0, len(whitelist_list)):
        player_name, player_uuid = whitelist_list[i]['name'], whitelist_list[i]['uuid']
        log(info, f'{i+1}: {player_name} - {player_uuid}')


def show_help_msg(info: Info):
    log(info, '''
    ============== 白名插件 ===============
    !!whitelist add [name] (API_num)    添加白名单
    !!whitelist remove [name]       移除白名单
    !!whitelist list                显示完整白名单
    !!whitelist help                显示此帮助信息
    ======================================''')


def show_choice_msg(info: Info):
    log(info, f'''
    API 可用选项：
    1 = mojang
    2 = littleskin
    ''')


def add_whitelist(info: Info, player_name: str, api: int):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    whitelist_name_list = []
    for value in whitelist_list:
        whitelist_name_list.append(value['name'])

    if player_name in whitelist_name_list:
        log(info, f'添加 {player_name} 白名时出现错误：白名单中已存在该玩家。')
    else:
        uuid = api_methods.get(api, None)(player_name)

        if uuid is not None:
            new_whitelist_dict = {'uuid': uuid, 'name': player_name}
            whitelist_list.append(new_whitelist_dict)
            create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_A_')
            time.sleep(1)
            server_cmd(info, '/whitelist reload')
            log(info, f'添加 {player_name} 白名单成功。')
        else:
            log(info, f'添加 {player_name} 白名单时出现错误，请重试')


def remove_whitelist(info: Info, player_name: str):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    for value in whitelist_list:
        if player_name == value['name']:
            sub_dict = {'uuid': value['uuid'], 'name': value['name']}
            whitelist_list.remove(sub_dict)
    create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_R_')
    log(info, f'白名单已移除玩家: name: {player_name}.')


def on_user_info(server: PluginServerInterface, info: Info):
    if info.content.startswith('!!whitelist'):
        args = info.content.split(' ')

        try:
            if args[1] == 'add':
                if server.get_permission_level(info) >= 3:
                    if len(args) > 2:
                        api = int(args[3]) if len(args) > 3 and args[3] in api_methods else 1
                        add_whitelist(info, args[2], api)
                    else:
                        log(info, 'Player name required.')
                else:
                    log(info, 'Permission denied.')

            elif args[1] == 'remove':
                if server.get_permission_level(info) >= 3:
                    if len(args) > 2:
                        remove_whitelist(info, args[2])
                    else:
                        log(info, 'Player name required.')
                else:
                    log(info, 'Permission denied.')

            elif args[1] == 'list':
                if server.get_permission_level(info) >= 3:
                    list_whitelist(info)
                else:
                    log(info, 'Permission denied.')

            elif args[1] == 'help':
                show_help_msg(info)
            else:
                log(info, f'Error.')
        except IndexError:
            show_help_msg(info)