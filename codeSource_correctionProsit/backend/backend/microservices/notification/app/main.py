"""Notification microservice - entry point.

Run:  uvicorn app.main:app --reload --port 8084
  or: python -m app.main
"""
import os
from contextlib import asynccontextmanager

import py_eureka_client.eureka_client as eureka_client
from fastapi import FastAPI

from app.routers import notification

PORT = int(os.getenv("PORT", "8084"))
EUREKA_SERVER = os.getenv("EUREKA_SERVER", "http://localhost:8761/eureka")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Demarrage : enregistrement dans Eureka (apparait comme NOTIFICATION)
    await eureka_client.init_async(
        eureka_server=EUREKA_SERVER,
        app_name="notification",
        instance_host="localhost",
        instance_ip="127.0.0.1",
        instance_port=PORT,
        health_check_url=f"http://localhost:{PORT}/health",
        status_page_url=f"http://localhost:{PORT}/info",
    )
    yield
    # Arret : desinscription d'Eureka
    await eureka_client.stop_async()


app = FastAPI(
    lifespan=lifespan,
    title="Notification Microservice API",
    version="1.0.0",
    description=(
        "Notification microservice (Python / FastAPI, no database). "
        "Only the hello endpoint is implemented; the notification logic is to be developed by students."
    ),
    contact={"name": "Badia Abouhdid"},
    servers=[{"url": f"http://localhost:{PORT}", "description": "Local"}],
    # Same URLs as the other microservices of the project
    docs_url="/swagger-ui",       # Swagger UI
    openapi_url="/v3/api-docs",   # OpenAPI JSON
    redoc_url="/redoc",           # alternative documentation
)

app.include_router(notification.router)


# ---- Sante et info (pour Eureka) ----
@app.get("/health", tags=["Actuator"])
def health():
    return {"status": "UP"}


@app.get("/info", tags=["Actuator"])
def info():
    return {"name": "notification", "version": "1.0.0"}


# TODO (students): if you add other routers, include them