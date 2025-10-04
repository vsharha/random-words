from fastapi import FastAPI, HTTPException, Depends, Query
from enum import Enum
from load_datasets import datasets_map
import random
from pathlib import Path

app = FastAPI()

class PartOfSpeech(Enum):
    noun = "N"
    verb = "V"
    adjective = "ADJ"

def parse_pos(pos: str = Query("n")) -> None | PartOfSpeech:
    for member in PartOfSpeech:
        if pos.lower() == member.name.lower() or member.name.lower().startswith(pos.lower()):
            return member
    raise HTTPException(status_code=400, detail="Invalid part of speech")

def validate_dataset(lang:str, pos:PartOfSpeech) -> None:
    if datasets_map.get(lang) is None:
        raise HTTPException(status_code=400, detail="Language is currently not supported")

    if datasets_map.get(lang).get(pos.value) is None:
        raise HTTPException(status_code=400, detail=f"Part of speech {pos.value} is currently not supported for language {lang}")

def filter_words(lang:str = "eng", pos:PartOfSpeech = Depends(parse_pos), max_index: int | None = None, max_len: int | None = None, min_len: int | None = None) -> list[str]:
    words: list[str] = list(datasets_map.get(lang).get(pos.value).keys())

    if max_index is not None:
        words = [word for i, word in enumerate(words) if i < max_index]

    if min_len is not None:
        words = [word for word in words if len(word) >= min_len]

    if max_len is not None:
        words = [word for word in words if len(word) <= max_len]

    return words

@app.get("/")
def get_random_word(max_index: int | None = None, max_len: int | None = None, min_len: int | None = None, lang:str = "eng", pos: PartOfSpeech = Depends(parse_pos)) -> dict[str, str]:
    validate_dataset(lang, pos)

    words: list[str] = filter_words(lang, pos, max_index, max_len, min_len)

    if not words:
        raise HTTPException(status_code=404, detail="No words found with the given criteria")

    return {"word": random.choice(words)}

@app.get("/words")
def get_word_list(length: int | None = None, lang:str = "eng", pos: PartOfSpeech = Depends(parse_pos)) -> dict[str, list[str]]:
    validate_dataset(lang, pos)

    words: list[str] = filter_words(lang, pos, length)
    return {"words": words}

@app.get("/languages")
def get_lang_list() -> dict[str, list[str]]:
    return {"languages": [str(lang.name) for lang in Path("datasets").iterdir()]}
