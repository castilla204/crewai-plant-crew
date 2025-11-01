#!/usr/bin/env python
import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from app.crew_runner import run_crew


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("task", nargs="?", default="Parada de emergencia en la cinta T901")
    args = parser.parse_args()
    print(json.dumps(run_crew(args.task), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
