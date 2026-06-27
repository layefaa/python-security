import sys
from pathlib import Path


def parse_log_line(line: str) -> dict[str, str] | None:
    ...

def failures_by_ip(entries: list[dict[str, str]]) -> dict[str, int]:
    ...

def top_offenders(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    ...

def summary_report(entries: list[dict[str, str]]) -> str:
    ...

def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <logfile>")
        sys.exit(1)

    log_path = Path(sys.argv[1])
    lines = log_path.read_text().splitlines()
    entries = [e for line in lines if (e := parse_log_line(line)) is not None]
    print(summary_report(entries))

if __name__ == "__main__":
    main()