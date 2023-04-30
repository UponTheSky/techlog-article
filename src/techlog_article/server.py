from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import ValidationError

from .auth.adapter.in_.controllers import router as auth_router
from .user.adapter.in_.controllers import router as user_router
from .article.adapter.in_.controllers import router as article_router

_app = FastAPI()

# middlewares
_app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # TODO: delete after deployment
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
_app.add_middleware(HTTPSRedirectMiddleware)
_app.add_middleware(
    TrustedHostMiddleware, allowed_hosts=["*"]
)  # TODO: change this to our FE server

# routers
_app.include_router(article_router)
_app.include_router(auth_router)
_app.include_router(user_router)

# error handler
_app.add_exception_handler(
    exc_class_or_status_code=ValidationError,
    handler=request_validation_exception_handler,
)

app: FastAPI = _app
