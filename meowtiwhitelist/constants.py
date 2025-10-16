import os

from mcdreforged.api.all import ServerInterface

PREFIX = "!!whitelist"

VERSION = ServerInterface.get_instance().as_plugin_server_interface().get_self_metadata().version

CONFIG_DIR = os.path.join("config", "MeowtiWhitelist")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SERVICE_DIR = os.path.join(CONFIG_DIR, "service")

EXAMPLE_DIR = os.path.join(CONFIG_DIR, "example")
EXAMPLE_FILES = {
"mojang.yml":
"""# Please edit before use.
id: 0

name: 'Mojang'
# Don't change it unless you really want to.
serviceType: MOJANG"""
,
"littleskin.yml":
"""# Please edit before use.
id: 0

name: 'LittleSkin'
# Don't change it unless you really want to.
serviceType: BLESSING_SKIN
yggdrasilAuth:
  blessingSkin:
    apiRoot: 'https://littleskin.cn/api/yggdrasil'"""
,
"elyby.yml":
"""# Please edit before use.
id: 0

name: 'Elyby'
# Don't change it unless you really want to.
serviceType: CUSTOM_YGGDRASIL
custom:
  method: 'GET'
  url: 'https://authserver.ely.by/api/users/profiles/minecraft'"""
}