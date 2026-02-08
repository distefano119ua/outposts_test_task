from fastapi import Depends, Query, HTTPException

from .schemas import ResourceEnum
from .nginx_log_parser import NginxLogFields
from .nginx import get_nginx_logs


def get_selected_fields(
        fields: NginxLogFields = Depends()
) -> set[str] | None:
    data = fields.model_dump(exclude_none=True)
    return {k for k, v in data.items() if v} or None


async def get_logs_by_resource(resource: ResourceEnum = Query(...)):
    if resource == ResourceEnum.nginx:
        #TO DO add logging
        print("Work on NGINX logs", flush=True)
        return await get_nginx_logs()
    else:
        raise HTTPException(status_code=400, detail="Temporary unavailable")

