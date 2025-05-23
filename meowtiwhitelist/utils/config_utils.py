import os

from mcdreforged.api.all import *

from meowtiwhitelist.constants import CONFIG_FILE


class Configuration(Serializable):
    server_dirname: str = "server"
    permission: int = 3
    disable_backup: bool = False

    def save(self):
        ServerInterface.get_instance().as_plugin_server_interface().save_config_simple(
            self, CONFIG_FILE, in_data_folder=False
        )


def load_raw_config() -> dict:
    if not os.path.exists(CONFIG_FILE):
        return {}
    return ServerInterface.get_instance().as_plugin_server_interface().load_config_simple(
        CONFIG_FILE, in_data_folder=False, target_class=Configuration
    ).serialize()


def migrate_config(raw: dict) -> Configuration:
    config = Configuration()
    config.__dict__.update(raw)
    return config


def init_config():
    raw = load_raw_config()
    config = migrate_config(raw)
    return config


config: Configuration = init_config()