from fastapi import FastAPI, HTTPException, Depends, Query
from enum import Enum

from starlette.middleware.cors import CORSMiddleware

from load_datasets import datasets_map
import random
from pathlib import Path

app = FastAPI()

origins = [
    # "http://localhost:5173",
    "https://wordle-international.netlify.app/"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

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

def filter_words(lang:str = "eng", min_freq: int | None = None, max_len: int | None = None, min_len: int | None = None, max_index:int | None=None, pos:PartOfSpeech=PartOfSpeech.noun) -> list[str]:
    word_freqs = datasets_map.get(lang).get(pos.value)
    words = list(word_freqs.items())

    if min_freq is not None:
        words = [(word, freq) for word, freq in words if freq >= min_freq]

    if min_len is not None:
        words = [(word, freq) for word, freq in words if len(word) >= min_len]

    if max_len is not None:
        words = [(word, freq) for word, freq in words if len(word) <= max_len]

    if max_index is not None:
        words = words[:max_index]

    return [word for word, _ in words]

@app.get("/word")
def get_random_word(min_freq: int | None = None, max_len: int | None = None, min_len: int | None = None, lang:str = "eng", pos: PartOfSpeech = Depends(parse_pos)) -> dict[str, str]:
    validate_dataset(lang, pos)

    words: list[str] = filter_words(lang, min_freq, max_len, min_len, pos)

    if not words:
        raise HTTPException(status_code=404, detail="No words found with the given criteria")

    return {"word": random.choice(words)}

@app.get("/words")
def get_word_list(min_freq: int | None = None, max_len: int | None = None, min_len: int | None = None, lang:str = "eng", max_index: int | None = None, pos: PartOfSpeech = Depends(parse_pos)) -> dict[str, list[str]]:
    validate_dataset(lang, pos)

    words: list[str] = filter_words(lang, min_freq, max_len, min_len, max_index, pos)
    return {"words": words}

@app.get("/languages")
def get_lang_list(pos: PartOfSpeech = Depends(parse_pos)) -> dict[str, list[str]]:
    languages = [str(lang.name) for lang in Path("datasets").iterdir()]

    return {"languages": [lang for lang in languages if datasets_map.get(lang) is not None and datasets_map.get(lang).get(pos.value) is not None]}
