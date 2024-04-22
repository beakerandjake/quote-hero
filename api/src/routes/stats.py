from fastapi import APIRouter
from ..util import elastic
from ..models import CamelCaseModel


router = APIRouter()


class Stats(CamelCaseModel):
    number_of_docs: int
    size_in_bytes: int


@router.get("/stats")
async def get_stats() -> Stats:
    """Returns information about the elastic wikiquote index"""
    return Stats(**elastic.get_stats())
