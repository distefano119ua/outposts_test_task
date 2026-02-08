from fastapi import FastAPI
from .settings import settings

app = FastAPI()


@app.get("/logs")
async def get_logs():
    with open(settings.PATH_TO_FILE) as f:
        logs = f.readlines()

    return logs