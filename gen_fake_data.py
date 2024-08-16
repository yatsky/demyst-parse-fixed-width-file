import csv
import faker
import json
import os

fake = faker.Faker()

rows = 10


def gen_line(field_names: list[str]) -> str:
    line = [
        "".join(fake.random_letters(int(spec["Offsets"][idx])))
        for idx, _ in enumerate(field_names)
    ]
    return "".join(line) + "\n"


with open('code-kata/spec.json') as f, open(
    "data/fixed_width_dataset.txt", 'w', encoding="windows-1252", newline=""
) as outfile:
    spec = json.load(f)

    field_names = spec['ColumnNames']

    for _ in range(rows):
        outfile.writelines([gen_line(field_names=field_names) for _ in range(rows)])
