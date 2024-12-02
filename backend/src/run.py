import uvicorn
from config.config import get_settings


def start():
    settings = get_settings()
    uvicorn.run(
        "main:app", host="0.0.0.0", port=settings.port, reload=True, log_level="info"
    )


if __name__ == "__main__":
    start()
