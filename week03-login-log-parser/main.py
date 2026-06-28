import sys
from pathlib import Path
from collections import Counter


def parse_log_line(line: str) -> dict[str, str] | None:
    line_split = line.split(' ')
    if 'Failed' in line_split:
        return {"timestamp": " ".join(line_split[:3]), "ip": line_split[4], "username": line_split[6]}
    return None

def failures_by_ip(entries: list[dict[str, str]]) -> dict[str, int]:
    counts = Counter(entry["ip"] for entry in entries)
    return counts

def top_offenders(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    sorted_count_by_value = sorted(counts.items(), key=lambda x: x[1], reverse=True)
    return sorted_count_by_value[:n]


def summary_report(entries: list[dict[str, str]]) -> str:
    total_failed_attempts = 0
    unique_ip = 0
    unique_usernames = 0

    top_offenders = []

    suspicious_username = 0



def main() -> None:
    if len(sys.argv) != 2:
        print("Usage: python main.py <logfile>")
        sys.exit(1)

    log_path = Path(sys.argv[1])
    lines = log_path.read_text().splitlines()
    entries = [e for line in lines if (e := parse_log_line(line)) is not None]
    # print(summary_report(entries))


if __name__ == "__main__":
    main()
