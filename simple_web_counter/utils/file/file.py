import csv
from pathlib import Path
from typing import List, Optional


def read_last_row_from_tsv(path: Path) -> Optional[List[str]]:
    with open(path) as f:
        reader = csv.reader(f, delimiter="\t")

        row = None

        for row in reader:
            continue

        return row


def add_row_to_tsv(path: Path, row: List[str]) -> None:
    with open(path, "a") as f:
        writer = csv.writer(f, delimiter="\t", lineterminator="\n")
        writer.writerow(row)
