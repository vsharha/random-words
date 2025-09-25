from fastapi import FastAPI, HTTPException, Depends, Query
from enum import Enum
from load_datasets import datasets_map
import random

app = FastAPI()

class PartsOfSpeech(Enum):
    noun = "N"
    verb = "V"
    adjective = "ADJ"

def parse_pos(pos: str = Query("n")):
    for member in PartsOfSpeech:
        if pos.lower() == member.name.lower() or member.name.lower().startswith(pos.lower()):
            return member
    raise HTTPException(status_code=400, detail="Invalid part of speech")

@app.get("/")
def get_random_word(max_index: int | None = None, max_len: int | None = None, min_len: int | None = None, lang:str = "eng", pos: PartsOfSpeech = Depends(parse_pos)):
    if datasets_map.get(lang) is None:
        raise HTTPException(status_code=400, detail="Language is currently not supported")

    if datasets_map.get(lang).get(pos.value) is None:
        raise HTTPException(status_code=400, detail=f"Part of speech {pos.value} is currently not supported for language {lang}")

    words = list(datasets_map.get(lang).get(pos.value).keys())

    if max_index is not None:
        words = [word for i, word in enumerate(words) if i < max_index]

    if min_len is not None:
        words = [word for word in words if len(word) >= min_len]

    if max_len is not None:
        words = [word for word in words if len(word) <= max_len]

    if not words:
        raise HTTPException(status_code=404, detail="No words found with the given criteria")

    return random.choice(words)
