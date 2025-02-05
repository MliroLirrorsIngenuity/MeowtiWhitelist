import shutil
import time
import json
import os

def check_dir(dir_path):
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)


def get_backup_dir(workpath: str) -> str:
    backup_dir = os.path.join(workpath, 'whitelist_backup')
    check_dir(backup_dir)
    return backup_dir


def get_backup_whitelist_path(backup_dir: str, type: str) -> str:
    format_time = time.strftime('%y-%m-%d_%H-%M-%S', time.localtime())
    backup_whitelist_name = f"{format_time}_{type}_whitelist.json"
    return os.path.join(backup_dir, backup_whitelist_name)


def move_existing_whitelist(whitelist_path: str, backup_whitelist_path: str):
    if os.path.exists(whitelist_path):
        shutil.move(whitelist_path, backup_whitelist_path)


def write_new_whitelist(whitelist_path: str, json_list: list):
    with open(whitelist_path, 'w', encoding='UTF-8') as file:
        json.dump(json_list, file, indent=4, ensure_ascii=False)


def clean_old_backups(backup_dir: str):
    backups = sorted(
        [f for f in os.listdir(backup_dir) if f.endswith('_whitelist.json')],
        key=lambda f: os.path.getctime(os.path.join(backup_dir, f))
    )
    while len(backups) > 5:
        oldest_backup = backups.pop(0)
        os.remove(os.path.join(backup_dir, oldest_backup))