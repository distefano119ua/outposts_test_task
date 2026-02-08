import httpx
import base64
from typing import List
from pathlib import Path
from fastapi import HTTPException

from .settings import settings
from .schemas import AddToEnum, NginxLog


def _get_file_sha(url: str, headers: dict) -> str:
    response = httpx.get(url, headers=headers, timeout=10.0)
    response.raise_for_status()

    data = response.json()
    sha = data.get("sha")

    if not sha:
        raise HTTPException(
            status_code=502,
            detail="GitHub response does not contain file sha"
        )

    return sha

def add_to_github(file_path: Path) -> None:
    if not file_path.exists():
        raise HTTPException(status_code=500, detail="File not found")

    owner, repo = settings.GITHUB_REPO.split("/", 1)
    github_path = f"{settings.GITHUB_EXPORTS_PATH}/{file_path.name}"

    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{github_path}"
    print(url, flush=True)
    content_bytes = file_path.read_bytes()
    content_b64 = base64.b64encode(content_bytes).decode("utf-8")

    payload = {
        "message": f"Add nginx logs: {file_path.name}",
        "content": content_b64,
        "branch": settings.GITHUB_BRANCH,
    }

    headers = {
        "Authorization": f"Bearer {settings.GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
    }

    #ADD logging
    try:
        response = httpx.put(url, json=payload, headers=headers, timeout=10.0)

        if response.status_code in (200, 201):
            return

        if response.status_code == 409:
            sha = _get_file_sha(url, headers)
            payload["sha"] = sha

            overwrite_response = httpx.put(
                url,
                json=payload,
                headers=headers,
                timeout=10.0,
            )
            overwrite_response.raise_for_status()
            return

        response.raise_for_status()

    except httpx.HTTPStatusError as e:
        raise HTTPException(
            status_code=502,
            detail=f"GitHub API error: {e.response.text}"
        )

    except httpx.RequestError as e:
        raise HTTPException(
            status_code=502,
            detail=f"GitHub request failed: {str(e)}"
        )


def add_logs(
    logs: List[NginxLog] | None,
    file_path: Path | None,
    add_to: AddToEnum,
    selected_fields: set[str] | None = None,
) -> None:
    if add_to == AddToEnum.github:
        if not file_path:
            raise HTTPException(
                status_code=400,
                detail="No file path provided",
            )
        add_to_github(file_path)

    elif add_to == AddToEnum.db:
        raise HTTPException(
            status_code=400,
            detail="Database is not configured"
        )