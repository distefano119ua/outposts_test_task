from typing import List
from pathlib import Path
from datetime import datetime
import json
import csv

from .settings import settings
from .schemas import NginxLog, ConvertToEnum


def save_as_csv(logs: List[NginxLog], path: Path, selected_fields: set[str]) -> None:
    if not logs:
        return

    logs = [log.model_dump(include=selected_fields) for log in logs]
    fieldnames = logs[0].keys()
    #ADD logging
    with open(path, "w", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(logs)


def save_as_json(logs: List[NginxLog], path: Path, selected_fields: set[str]) -> None:
    if not logs:
        return

    data = [log.model_dump(include=selected_fields, mode='json') for log in logs]
    #ADD logging
    with open(path, "w", encoding="utf-8") as jsonfile:
        json.dump(data, jsonfile, ensure_ascii=False, indent=2)


def build_output_path(
    output_dir: Path,
    convert_to: ConvertToEnum,
) -> Path:
    #ADD logging
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"nginx_logs_{ts}.{convert_to.value}"
    return output_dir / filename


def convert_and_save(
        logs: List[NginxLog],
        convert_to: ConvertToEnum,
        selected_fields: set[str],
        output_dir: Path = Path(settings.EXPORT_LOGS_DIR)
) -> Path:
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = build_output_path(output_dir, convert_to)

    if convert_to == ConvertToEnum.csv:
        save_as_csv(logs, output_path, selected_fields)

    elif convert_to == ConvertToEnum.json:
        save_as_json(logs, output_path, selected_fields)

    #print(output_path, flush=True)
    return output_path