import contextvars
import sys

from starlette.applications import Starlette
from starlette.middleware import Middleware
from starlette.responses import JSONResponse
from starlette.routing import Route

var = contextvars.ContextVar("var", default=None)


class ASGIMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)

        if var.get() is not None:
            print(f"var is already set {var.get}, exiting...")
            sys.exit()

        token = var.set("TEST")

        await self.app(scope, receive, send)

        var.reset(token)


async def route(request):
    return JSONResponse({"hello": "world"})


app = Starlette(
    middleware=[Middleware(ASGIMiddleware)],
    routes=[Route('/', route, methods=["POST"])]
)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.server:app",
        host="0.0.0.0",
        port=8001,
    )
