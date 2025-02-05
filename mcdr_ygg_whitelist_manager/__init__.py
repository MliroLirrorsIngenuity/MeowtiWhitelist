import shutil
import time
import json
import os
from .utils import *

server_dirname = 'server'
world_dirname = 'world'


def on_load(server: PluginServerInterface, prev):
    server.register_help_message('!!whitelist', '白名单管理插件')
    register_command(server)


def server_cmd(src, command: str):
    src.get_server().execute(command)


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


def show_help_msg(src):
    log(src,'''
    =======================白名插件=======================
    !!whitelist add [name] (API num/name)    添加白名单
    !!whitelist remove [name]                移除白名单
    !!whitelist list                         显示完整白名单
    !!whitelist help                         显示此帮助信息
    ======================================================''')
    show_choice_msg(src)


def show_choice_msg(src):
    log(src,f'''
    API 可用选项：
    1 = Mojang
    2 = LittleSkin
    ''')


def add_whitelist(src, player_name: str, api: str):
    api_methods = {
        1: get_mojang_uuid_sync,
        2: get_littleskin_uuid_sync
#       3: example
    }
    if api.casefold() == 'mojang':
        api = 1
    elif api.casefold() == 'littleskin':
        api = 2
#   elif api.casefold() == 'example':
#       api = 3
    elif api.isdigit() and int(api) in api_methods:
        api = int(api)
    else:
        log(src, "无效的 API 参数")
        show_choice_msg(src)
        return

    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    whitelist_name_list = []
    for value in whitelist_list:
        whitelist_name_list.append(value['name'])

    if player_name in whitelist_name_list:
        log(src, f'添加 {player_name} 白名时出现错误：白名单中已存在该玩家。')
    else:
        uuid = api_methods.get(api, None)(player_name)

        if uuid is not None:
            new_whitelist_dict = {'uuid': uuid, 'name': player_name}
            whitelist_list.append(new_whitelist_dict)
            create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_A_')
            time.sleep(1)
            server_cmd(src, '/whitelist reload')
            log(src, f'添加 {player_name} 白名单成功。')
        else:
            log(src, f'添加 {player_name} 白名单时出现错误，请重试')


def remove_whitelist(src, player_name: str):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    for value in whitelist_list:
        if player_name == value['name']:
            sub_dict = {'uuid': value['uuid'], 'name': value['name']}
            whitelist_list.remove(sub_dict)
    create_whitelist_file(whitelist_list, os.path.join(server_dirname), '_R_')
    log(src, f'白名单已移除玩家: {player_name}.')


def list_whitelist(src):
    whitelist_list: list = json_file_to_list(os.path.join(server_dirname, 'whitelist.json'))
    log(src, '===== 白名单 =====：')
    for i in range(0, len(whitelist_list)):
        player_name, player_uuid = whitelist_list[i]['name'], whitelist_list[i]['uuid']
        log(src, f'{i+1}: {player_name} - {player_uuid}')


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        return Literal(literal)

    server.register_command(
        Literal("!!whitelist")
        .requires(lambda src: src.has_permission(3))
        .on_error(
            RequirementNotMet,
            lambda src: log(src, "权限不足"),
            handled=True,
        )
        .runs(lambda src: show_help_msg(src))
        .then(
            get_literal_node("help")
            .runs(lambda src: show_help_msg(src))
        )
        .then(
            get_literal_node("add")
            .runs(lambda src: log(src, "需要玩家名，正确用法：!!whitelist add [name] (API num/name)"))
            .then(
                Text("player_name").runs(lambda src: log(src, "需要API参数，正确用法：!!whitelist add [name] (API num/name)"))
                .then(
                    Text("api").runs(lambda src, ctx: add_whitelist(src, ctx["player_name"], str(ctx["api"])))
                )
            )
        )
        .then(
            get_literal_node("remove")
            .runs(lambda src: log(src, "需要玩家名，正确用法：!!whitelist remove [name]"))
            .then(
                Text("player_name").runs(lambda src, ctx: remove_whitelist(src, ctx["player_name"]))
            )
        )
        .then(
            get_literal_node("list")
            .runs(lambda src: list_whitelist(src))
        )
    )