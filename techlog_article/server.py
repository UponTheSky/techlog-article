from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import ValidationError

from .auth.adapter.in_.controllers import router as auth_router
from .user.adapter.in_.controllers import router as user_router  # noqa: F401
from .article.adapter.in_.controllers import router as article_router

from .common.tags import Tags
from .common.database import db_session_middleware_function
from .common.config import config

_app = FastAPI(
    title="techlog-article",
    description="The backend API of my personal tech blog article",
    version="0.0.1",
    contact={
        "name": "Sung Ju Yea",
        "url": "https://github.com/uponTheSky/",
        "email": "sungju.yea@gmail.com",
    },
    openapi_tags=[
        {"name": Tags.user, "description": "The APIs about the users"},
        {
            "name": Tags.auth,
            "description": "The APIs providing access tokens to the users",
        },
        {"name": Tags.article, "description": "The APIs about the users"},
    ],
)

# swagger ui: turn off in production
if config.DEBUG:
    _app.docs_url = None
    _app.redoc_url = None

# TODO: revisit before deployment

# middlewares
_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if not (config.DEBUG or config.ENV == "local"):
    _app.add_middleware(HTTPSRedirectMiddleware)

_app.add_middleware(TrustedHostMiddleware, allowed_hosts=["*"])


@_app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    return await db_session_middleware_function(request, call_next)


# routers
_app.include_router(article_router)
_app.include_router(auth_router)

"""
Here we disallow the user service to be used by the users.
This is becaue we don't want to allow the users to create accounts
and write articles in our application.

The purposes of this implementation is to demonstrate
- how I understand RDBMS(Postgres)
- how I understand the basic process of user authentification
"""
# _app.include_router(user_router)

# error handler
_app.add_exception_handler(
    exc_class_or_status_code=ValidationError,
    handler=request_validation_exception_handler,
)


@_app.get("/health")
async def health_check():
    return {"message": "The backend WAS works okay"}


app = _app
