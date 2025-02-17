import os

from mcdr_ygg_whitelist_manager.utils.logger_utils import *
from mcdr_ygg_whitelist_manager.utils.translater_utils import *

CONFIG_FILE = os.path.join("config", "MCDR-ygg-whitelist-manager.json")

class Configuration(Serializable):
    server_dirname: str = "server"
    permission: int = 3

    def save(self):
        ServerInterface.get_instance() \
            .as_plugin_server_interface() \
            .save_config_simple(self, CONFIG_FILE, in_data_folder=False)


if not os.path.exists(CONFIG_FILE):
    config = Configuration()
    config.save()
else:
    config: Configuration = ServerInterface.get_instance() \
        .as_plugin_server_interface() \
        .load_config_simple(
            CONFIG_FILE,
            target_class=Configuration,
            in_data_folder=False,
            source_to_reply=None,
        )

server_dirname = config.server_dirname