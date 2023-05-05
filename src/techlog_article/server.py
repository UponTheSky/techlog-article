from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.httpsredirect import HTTPSRedirectMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.exception_handlers import request_validation_exception_handler
from pydantic import ValidationError

from .auth.adapter.in_.controllers import router as auth_router
from .user.adapter.in_.controllers import router as user_router
from .article.adapter.in_.controllers import router as article_router

from .common.tags import Tags
from .common.database import db_session_middleware_function

_app = FastAPI(
    title="techlog-article",
    description="The backend API of my personal tech blog article",
    version="0.0.1",
    contact={
        "name": "Sung Ju Yea",
        "url": "TBA",  # TODO: add url of the FE homepage
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
    TrustedHostMiddleware, allowed_hosts=["localhost"]
)  # TODO: change this to our FE server


@_app.middleware("http")
async def db_session_middleware(request: Request, call_next):
    return await db_session_middleware_function(request, call_next)


# routers
_app.include_router(article_router)
_app.include_router(auth_router)
_app.include_router(user_router)

# error handler
_app.add_exception_handler(
    exc_class_or_status_code=ValidationError,
    handler=request_validation_exception_handler,
)

app = _app
