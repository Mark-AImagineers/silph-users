# app/api/version.py

from fastapi import APIRouter
import json
from pathlib import Path

router = APIRouter()

VERSION_FILE = Path(__file__).parent.parent.parent / "version.json"

@router.get("/version", tags=["System"])
async def get_version():
    with open(VERSION_FILE) as f:
        return json.load(f)