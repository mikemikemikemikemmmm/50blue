from fastapi import FastAPI, Response
from starlette.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from src.setting.index import get_settings
from src.utils.index import is_dev_environment

class SecurityMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response: Response = await call_next(request)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = (
            "camera=(), geolocation=(), microphone=()"
        )
        # https://cdn.jsdelivr.net https://fastapi.tiangolo.com for /docs
        # csp_str = "default-src 'self'; style-src 'self' https://cdn.jsdelivr.net; script-src 'self' https://cdn.jsdelivr.net 'unsafe-inline'; img-src 'self' https://fastapi.tiangolo.com data:;"
        # response.headers["Content-Security-Policy"] = csp_str
        return response


def setup_global_middleware(app: FastAPI):
    setting = get_settings()
    allow_origin = "*" if is_dev_environment() else setting.FRONT_ORIGIN
    app.add_middleware(SecurityMiddleware)
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[allow_origin],
        allow_methods=["*"],
        allow_headers=["*"],
    )
