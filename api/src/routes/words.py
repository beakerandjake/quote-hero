from fastapi import APIRouter
from ..util.random_word import random_word

router = APIRouter()


@router.get("/words")
async def get_random_word():
    """Returns a random word from the list of words"""
    return random_word()
