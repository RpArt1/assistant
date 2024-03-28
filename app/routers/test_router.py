from fastapi import APIRouter, Depends, HTTPException
import logging

router = APIRouter()

@router.get("/")
def get_test():
    logging.info("Test endpoint called")
    return {"get test": "ok"}

@router.post("/")
def post_test():
    logging.info("Test endpoint called")
    return {"post test": "ok"}
