from .settings import settings
from .nginx_log_parser import parse_nginx_logs

import httpx
from fastapi import HTTPException
from typing import List


async def get_nginx_logs():

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(settings.NGINX_LOGS_URL)
            response.raise_for_status()

            raw_logs: List[str] = response.json()

        except httpx.ConnectError:
            # nginx service is unavailable
            raise HTTPException(
                status_code=503,
                detail="Nginx service is unavailable"
            )

        except httpx.ReadTimeout:
            raise HTTPException(
                status_code=504,
                detail="Nginx service timeout"
            )

        except httpx.HTTPStatusError as e:
            # nginx returned 4xx / 5xx
            raise HTTPException(
                status_code=502,
                detail=f"Nginx service error: {e.response.status_code}"
            )

        except httpx.RequestError as e:
            # any other transport-level error
            raise HTTPException(
                status_code=502,
                detail=f"Request to nginx failed: {str(e)}"
            )

    return parse_nginx_logs(raw_logs)
