from mcdreforged.api.all import ServerInterface, RTextMCDRTranslation


def tr(translation_key: str, *args) -> RTextMCDRTranslation:
    return ServerInterface.get_instance().rtr(
        "meowtiwhitelist.{}".format(translation_key), *args
    )