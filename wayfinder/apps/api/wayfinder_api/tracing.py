from fastapi import FastAPI


def configure_tracing(app: FastAPI) -> None:
    try:
        from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
    except ModuleNotFoundError:
        return

    FastAPIInstrumentor.instrument_app(app)
