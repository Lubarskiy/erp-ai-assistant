from fastapi import APIRouter
router = APIRouter()

@router.post("/search")
def search():
    return {"items": []}

@router.post("/reindex")
def reindex():
    return {"status": "queued"}
