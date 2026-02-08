from fastapi import FastAPI, Query, HTTPException
from fastapi.params import Depends
from typing import Optional, List

from .nginx_log_parser import NginxLog
from .dependencies import get_selected_fields, get_logs_by_resource
from .schemas import AddToEnum, ConvertToEnum
from .converters import convert_and_save
from .uploaders import add_logs


app = FastAPI()


@app.post("/logs")
async def nginx_log(
        logs: List[NginxLog] = Depends(get_logs_by_resource),
        selected_fields: Optional[set[str]] = Depends(get_selected_fields),
        add_to: Optional[AddToEnum] = Query(None, description="Place to add logs"),
        convert_to: Optional[ConvertToEnum] = Query(None, description="Define convert type"),
        save: bool = Query(False, description="Save logs")
):
    if save and not convert_to:
        raise HTTPException(status_code=400, detail="Convert_To must be specified")

    if save:
        exported_file = convert_and_save(
            logs=logs,
            selected_fields=selected_fields,
            convert_to=convert_to,
        )

    if add_to:
        add_logs(
            logs=logs if add_to ==AddToEnum.db else None,
            file_path=exported_file if add_to == AddToEnum.github else None,
            add_to=add_to,
            selected_fields=selected_fields,
        )

    if selected_fields:
        return [
            log.model_dump(include=selected_fields) for log in logs
        ]

    return logs


