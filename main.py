import uvicorn

from techlog_article.server import app  # noqa: F401
from techlog_article.common.config import config

if __name__ == "__main__":
    uvicorn.run(
        "main:app", host=config.APP_HOST, port=config.APP_PORT, reload=config.DEBUG
    )
