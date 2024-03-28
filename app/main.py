from fastapi import FastAPI, Request, status
import logging
from .routers import router
from .routers import test_router
import debugpy
from fastapi.exceptions import RequestValidationError

logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

debugpy.listen(("0.0.0.0", 5678))


app = FastAPI()

@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
	return exc

app.include_router(router.router, prefix="/memories", tags=["memories"])
app.include_router(test_router.router, prefix="/test", tags=["testing"])


