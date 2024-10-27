from http.client import HTTPException

from anaconda_catalogs.catalog import API_VERSION
from fastapi import APIRouter
from flask import session

api_router = APIRouter()

BACKEND_BASE_URL = "http://localhost:8080/modules"

@api_router.post("/input")
async def add_entry(entry):
    uri = f"{BACKEND_BASE_URL}/input"

