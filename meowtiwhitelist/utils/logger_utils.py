from mcdreforged.api.all import *

from meowtiwhitelist.utils.translater_utils import tr
from meowtiwhitelist.utils.service_loader_utils import services, service_conflicts


def log(source: CommandSource,text):
    text = RTextList(text)
    source.reply(text)


def log_available_services(src):
    if service_conflicts:
        log_conflict_errors(src, service_conflicts)
        return

    log(src, tr("available_services.header"))
    valid_services = [s for s in services if s.get('id', -1) > 0]

    if not valid_services:
        log(src, tr("available_services.none"))
        return

    for service in valid_services:
        log(src, tr("available_services.item", service['name'], service['id']))


def log_conflict_errors(src, conflicts):
    log(src, tr("error.conflict_header"))
    for conflict in conflicts:
        if conflict['type'] == 'id':
            log(src, tr("error.conflict_id", conflict['value'], ", ".join(conflict['files'])))
        else:
            log(src, tr("error.conflict_name", conflict['value'], ", ".join(conflict['files'])))