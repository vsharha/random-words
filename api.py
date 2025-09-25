from fastapi import FastAPI, HTTPException
from enum import Enum
from load_datasets import datasets_map
import random

app = FastAPI()

class PartsOfSpeech(Enum):
    noun = "N"
    verb = "V"
    adjective = "ADJ"

@app.get("/")
def get_random_word(lang:str = "eng", pos: PartsOfSpeech = PartsOfSpeech.noun):
    return random.choice(list(datasets_map[lang][pos.value].keys()))
