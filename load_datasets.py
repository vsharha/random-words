import csv
from typing import Iterator
from pathlib import Path

def file_iterator(file_path: Path | str) -> Iterator[dict]:
    file_path = Path(file_path)

    with file_path.open("r") as f:
        reader = csv.reader(f, delimiter="\t")

        for row in reader:
            yield {row[0]:int(row[1])}

def build_map(lang_dataset_dir) -> dict[str, int]:
    lang_dataset_dir: Path = Path(lang_dataset_dir)

    word_map: dict[str, int] = {}
    for word in file_iterator(lang_dataset_dir):
        word_map.update(word)

    return word_map

def load_datasets(datasets_dir: Path | str):
    datasets_dir = Path(datasets_dir)

    datasets_map: dict[str, dict[str, dict[str, int]]] = {}
    for dataset in datasets_dir.iterdir():
        datasets_map[dataset.name] = {}
        for lang in dataset.iterdir():
            datasets_map[dataset.name][lang.name] = {}
            datasets_map[dataset.name][lang.name].update(build_map(lang))

    return datasets_map

DATASETS_DIR: Path = Path('./datasets')
datasets_map: dict = load_datasets(DATASETS_DIR)
