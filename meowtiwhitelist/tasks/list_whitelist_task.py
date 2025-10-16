from mcdreforged.api.all import *

from meowtiwhitelist.constants import PREFIX
from meowtiwhitelist.utils.file_utils import get_whitelist_path, json_file_to_list
from meowtiwhitelist.utils.logger_utils import log
from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.utils.config_utils import config


class ListWhitelistTask:
    def __init__(self, src: CommandSource, page: int):
        self.source = src
        self.page = page
        self.per_page = 10

    def _make_command(self, page_to_build: int) -> str:
        base_command = f'{PREFIX} list'
        return f'{base_command} {page_to_build}'

    def run(self):
        src, page, per_page = self.source, self.page, self.per_page

        whitelist_path = get_whitelist_path(config.server_dirname)
        whitelist_list: list = json_file_to_list(whitelist_path)
        total_items = len(whitelist_list)
        total_pages = (total_items - 1) // per_page + 1

        whitelist_list.reverse()
        start_index = (page - 1) * per_page
        end_index = min(start_index + per_page, total_items)
        page_entries = whitelist_list[start_index:end_index]

        log(src, tr("list"))

        for idx_in_page, entry in enumerate(page_entries):
            reversed_index = start_index + idx_in_page
            item_num = total_items - reversed_index

            player_name, player_uuid = entry['name'], entry['uuid']
            log(src, f'[#{item_num}] {player_name} - {player_uuid}')

        t_prev = RText('<-----')
        if page > 1:
            t_prev.h(tr('prev_page_hover')).c(RAction.run_command, self._make_command(page - 1))
        else:
            t_prev.set_color(RColor.dark_gray)

        t_next = RText('----->')
        if page < total_pages:
            t_next.h(tr('next_page_hover')).c(RAction.run_command, self._make_command(page + 1))
        else:
            t_next.set_color(RColor.dark_gray)

        footer = RTextList(t_prev, f' {page}/{total_pages} ', t_next)
        log(src, footer)