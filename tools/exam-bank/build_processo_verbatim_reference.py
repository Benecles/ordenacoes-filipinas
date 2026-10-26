#!/usr/bin/env python3
"""Build a deterministic text-only Processo exam-bank reference."""
import json
import sys
from collections import defaultdict
from pathlib import Path


def main() -> None:
    if len(sys.argv) != 3:
        raise SystemExit("usage: build_processo_verbatim_reference.py SOURCE_BANK OUTPUT_JSON")
    source_path, output_path = map(Path, sys.argv[1:])
    bank = json.loads(source_path.read_text(encoding="utf-8"))
    questions = defaultdict(list)
    for record in bank["questions"]:
        for appearance in record["appearances"]:
            questions[record["id"]].append({
                "year": appearance["year"],
                "question_number": appearance["question_number"],
                "verbatim_text": appearance["verbatim_text"],
            })
    result = {
        "generated_from": "work/pipeline/processo-civil-i/exam-bank.json",
        "questions": [
            {"id": question_id, "appearances": appearances}
            for question_id, appearances in sorted(questions.items())
        ],
    }
    output_path.write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


if __name__ == "__main__":
    main()
