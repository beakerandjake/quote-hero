from fastapi import APIRouter

router = APIRouter()


@router.post("/search")
async def search():
    """Searches for pages which match the given words"""
    return "Search it!"
