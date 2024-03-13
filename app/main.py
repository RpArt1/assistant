from fastapi import FastAPI
import logging
from .routers import router
import debugpy


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

debugpy.listen(("0.0.0.0", 5678))
print("Waiting for client to attach...")
logging.info("Test endpoint called")

debugpy.wait_for_client()

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