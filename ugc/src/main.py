import logging

import uvicorn as uvicorn
from fastapi import FastAPI

from api.v1.bookmark import router as mark_router
from api.v1.like import router as like_router
from api.v1.progress_film import router as progress_router
from api.v1.review import router as review_router
from broker.kafka_settings import kafka
from core.config import settings
from fastapi import FastAPI

# initialize logger
logger = logging.getLogger(__name__)

app = FastAPI(
    docs_url="/ugc_api/openapi",
    openapi_url="/ugc_api/openapi.json",
)

app.include_router(mark_router)
app.include_router(like_router)
app.include_router(progress_router)
app.include_router(review_router)


@app.on_event("startup")
async def startup_event():
    logger.info("Initializing API ...")
    await kafka.get_producer()


@app.on_event("shutdown")
async def shutdown_event():
    logger.info("Shutting down API")
    await kafka.stop_producer()


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.ugc_host,
        port=settings.ugc_port,
    )
