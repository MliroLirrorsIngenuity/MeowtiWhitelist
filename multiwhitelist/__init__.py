from mcdreforged.api.all import *

from multiwhitelist.constants import PREFIX
from multiwhitelist.utils.file_utils import create_example_files
from multiwhitelist.utils.translater_utils import tr
from multiwhitelist.command import register_command


def on_load(server: PluginServerInterface, prev):
    server.register_help_message(PREFIX, tr("help_msg_name"))
    create_example_files()
    register_command(server)