from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routers.auth._router import router

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: delete after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router)


@app.get("/")
async def main():
    return {"message": "hey"}
