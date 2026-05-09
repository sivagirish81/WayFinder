from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wayfinder_api.api import approvals, audit, demo, health, integrations, slack, traces, trips
from wayfinder_api.logging import configure_logging
from wayfinder_api.tracing import configure_tracing


def create_app() -> FastAPI:
    configure_logging()
    app = FastAPI(title="Wayfinder API", version="0.1.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    for router in [
        health.router,
        trips.router,
        demo.router,
        slack.router,
        approvals.router,
        integrations.router,
        audit.router,
        traces.router,
    ]:
        app.include_router(router)
    configure_tracing(app)
    return app


app = create_app()
