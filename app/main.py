from fastapi import FastAPI
import logging
from .routers import router

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI()

@app.get("/")
def root():
    return {"hello": "world"}

@app.get("/test")
def get_test():
    logging.info("Test endpoint called")
    return {"get test": "ok"}

@app.post("/test")
def post_test():
    logging.info("Test endpoint called")
    return {"post test": "ok"}

app.include_router(router.router, prefix="/memories", tags=["memories"])