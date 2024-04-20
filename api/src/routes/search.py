from fastapi import APIRouter
from pydantic import BaseModel, Field, validator


router = APIRouter()


class Query(BaseModel):
    terms: list[str] = Field(min_items=1)

    class Config:
        str_strip_whitespace = True
        str_min_length = 1
        str_max_length = 50


@router.post("/search")
async def search(query: Query):
    """Searches for pages which match the given words"""
    return f"You searched for: {query.terms}"
