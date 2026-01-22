from fastapi import FastAPI


def setup_routers(app: FastAPI):
    router = []
    for route in router:
        app.include_router(route)
