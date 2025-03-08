import os
from collections import defaultdict

import yaml
from meowtiwhitelist.constants import SERVICE_DIR


def load_all_services():
    if not os.path.exists(SERVICE_DIR):
        os.makedirs(SERVICE_DIR, exist_ok=True)

    api_configs = []
    id_to_files = defaultdict(list)
    name_to_files = defaultdict(list)

    for filename in os.listdir(SERVICE_DIR):
        if filename.endswith((".yml", ".yaml")):
            file_path = os.path.join(SERVICE_DIR, filename)
            with open(file_path, "r", encoding="utf-8") as f:
                config = yaml.safe_load(f)
                config["id"] = int(config.get("id", -1))
                service_id = config["id"]
                service_name = config.get("name", "").strip().lower()

                api_configs.append(config)
                id_to_files[service_id].append(filename)
                if service_name:
                    name_to_files[service_name].append(filename)

    api_configs.sort(key=lambda x: x.get('id', 0))

    conflicts = []
    for service_id, files in id_to_files.items():
        if len(files) > 1:
            conflicts.append({
                'type': 'id',
                'value': service_id,
                'files': files.copy()
            })
    for service_name, files in name_to_files.items():
        if len(files) > 1:
            conflicts.append({
                'type': 'name',
                'value': service_name,
                'files': files.copy()
            })

    return api_configs, conflicts


api_services, service_conflicts = load_all_services()


def build_service_mapping() -> dict:
    service_map = {}
    for service in api_services:
        if (service_id := service.get('id', -1)) <= 0:
            continue

        normalized_name = service.get('name', '').strip().lower()
        service_map.update({
            normalized_name: service_id,
            str(service_id): service_id
        })
    return service_map