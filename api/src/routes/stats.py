from fastapi import APIRouter
from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel
from ..util import elastic


router = APIRouter()


class CamelCaseModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True,
    )


class Stats(CamelCaseModel):
    number_of_docs: int
    size_in_bytes: int


@router.get("/stats")
async def get_stats() -> Stats:
    """Returns information about the elastic wikiquote index"""
    return Stats(**elastic.get_stats())
