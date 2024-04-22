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


class Hit(CamelCaseModel):
    page_id: int
    title: str


class Result(CamelCaseModel):
    total: int
    top: list[Hit]


@router.post("/search")
async def search(query: Query) -> Result:
    """Searches for pages which match the given words"""
    if query.exact:
        return Result(elastic.search_exact(query.terms))
    return Result(**elastic.search_fuzzy(query.terms))
