from mcdreforged.plugin.si.server_interface import ServerInterface
from mcdreforged.translation.translation_text import RTextMCDRTranslation

def tr(translation_key: str, *args) -> RTextMCDRTranslation:
    return ServerInterface.get_instance().rtr(
        "mcdr_ygg_whitelist_manager.{}".format(translation_key), *args
    )