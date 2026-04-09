import pkgutil
import importlib
from fastapi import FastAPI
from fastapi.routing import APIRouter
import app.routes as routes_package

def register_routers(app: FastAPI) -> None:
    for _, module_name, _ in pkgutil.iter_modules(routes_package.__path__):
        module = importlib.import_module(f"app.routes.{module_name}")
        if hasattr(module, "router") and isinstance(module.router, APIRouter):
            app.include_router(module.router)