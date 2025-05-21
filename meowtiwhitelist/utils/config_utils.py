import os

from mcdreforged.api.all import *

from meowtiwhitelist.constants import CONFIG_FILE


class Configuration(Serializable):
    server_dirname: str = "server"
    permission: int = 3
    disable_backup: bool = False
    # I_KNOW_BACKUP_IS_DISABLED not in config file, but in the blackhole (what?)

    def save(self):
        # Only save disable_backup, unless disable_backup is True, then additionally save I_KNOW_BACKUP_IS_DISABLED
        data = self.__dict__.copy()
        if not data.get('disable_backup', False):
            data.pop('I_KNOW_BACKUP_IS_DISABLED', None)
        else:
            # If disable_backup is True, ensure I_KNOW_BACKUP_IS_DISABLED exists and is False.
            if 'I_KNOW_BACKUP_IS_DISABLED' not in data:
                data['I_KNOW_BACKUP_IS_DISABLED'] = False
        # Only save the necessary fields
        save_data = {k: v for k, v in data.items() if k in ['server_dirname', 'permission', 'disable_backup', 'I_KNOW_BACKUP_IS_DISABLED'] or (k not in ['I_KNOW_BACKUP_IS_DISABLED'])}
        # If disable_backup is False, do not save I_KNOW_BACKUP_IS_DISABLED
        if not data.get('disable_backup', False):
            save_data.pop('I_KNOW_BACKUP_IS_DISABLED', None)
        ServerInterface.get_instance().as_plugin_server_interface().save_config_simple(
            type(self)(**save_data), CONFIG_FILE, in_data_folder=False
        )

    def is_backup_disabled(self):
        return bool(getattr(self, 'disable_backup', False) and getattr(self, 'I_KNOW_BACKUP_IS_DISABLED', False))

    def need_backup_disable_warning(self):
        return bool(getattr(self, 'disable_backup', False) and not getattr(self, 'I_KNOW_BACKUP_IS_DISABLED', False))


def load_raw_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}
    return ServerInterface.get_instance().as_plugin_server_interface().load_config_simple(
        CONFIG_FILE, in_data_folder=False, target_class=Configuration
    ).serialize()


def migrate_config(raw: dict) -> Configuration:
    config = Configuration()
    # Just in case.
    if 'enable_backup' in raw:
        raw['disable_backup'] = not raw.pop('enable_backup')
    config.__dict__.update(raw)
    return config


def init_config():
    raw = load_raw_config()
    config = migrate_config(raw)
    return config

config: Configuration = init_config()