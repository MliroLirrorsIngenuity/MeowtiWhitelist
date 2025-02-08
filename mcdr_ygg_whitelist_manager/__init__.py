from mcdr_ygg_whitelist_manager.utils.logger_utils import *
from mcdr_ygg_whitelist_manager.utils.lookuper_utils import *
from mcdr_ygg_whitelist_manager.utils.translater_utils import *
from mcdr_ygg_whitelist_manager.operations import *


def on_load(server: PluginServerInterface, prev):
    server.register_help_message('!!whitelist', tr("help_msg_name"))
    register_command(server)


def register_command(server: PluginServerInterface):
    def get_literal_node(literal):
        return Literal(literal)

    server.register_command(
        Literal("!!whitelist")
        .requires(lambda src: src.has_permission(3))
        .on_error(
            RequirementNotMet,
            lambda src: log(src, tr("error.permission_denied")),
            handled=True,
        )
        .runs(lambda src: log(src,tr("help_msg")))
        .then(
            get_literal_node("help")
            .runs(lambda src: log(src,tr("help_msg")))
        )
        .then(
            get_literal_node("add")
            .runs(lambda src: log(src, tr("error.add_require_name")))
            .then(
                Text("player_name").runs(lambda src: log(src, tr("error.require_api")))
                .then(
                    Text("api").runs(lambda src, ctx: add_whitelist(src, ctx["player_name"], str(ctx["api"])))
                    .on_error(
                        RequirementNotMet,
                        lambda src, ctx: log(src, tr("error.unknown_error", ctx["player_name"])),
                        handled=True,
                    )
                )
            )
        )
        .then(
            get_literal_node("remove")
            .runs(lambda src: log(src, tr("error.remove_require_name")))
            .then(
                Text("player_name").runs(lambda src, ctx: remove_whitelist(src, ctx["player_name"]))
            )
        )
        .then(
            get_literal_node("list")
            .runs(lambda src: list_whitelist(src))
        )
    )