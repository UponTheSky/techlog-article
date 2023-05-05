import uvicorn
from .server import app

if __name__ == "__main__":
    uvicorn.run(
        app=app, host="0.0.0.0", port=8000, reload=True
    )  # TODO: get rid of reload=True when in production
