from fastapi import APIRouter
from pydantic import Field
from ..util import elastic
from ..models import CamelCaseModel

router = APIRouter()


class Query(CamelCaseModel):
    terms: list[str] = Field(min_items=1)
    exact: bool

    class Config:
        str_strip_whitespace = True
        str_min_length = 1
        str_max_length = 50


@router.post("/search")
async def search(query: Query):
    """Searches for pages which match the given words"""
    if query.exact:
        return elastic.search_exact(query.terms)
    return elastic.search_fuzzy(query.terms)
