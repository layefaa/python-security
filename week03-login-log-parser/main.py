import sys
from pathlib import Path

def parse_log_line(line: str) -> dict[str, str] | None:
    line_split = line.split()
    if 'Failed' in line_split:
        try:
            ip_index = line_split.index('from') + 1
            ip = line_split[ip_index]
            if 'invalid' in line_split:
                user_index = line_split.index('user') + 1
            else:
                user_index = line_split.index('for') + 1
            username = line_split[user_index]
            return {
                "timestamp": f"{line_split[0]} {line_split[1]} {line_split[2]}",
                "ip": ip,
                "username": username
            }
        except ValueError:
            return None
    return None

def failures_by_ip(entries: list[dict[str, str]]) -> dict[str, int]:
    counts = {}
    for entry in entries:
        ip = entry["ip"]
        counts[ip] = counts.get(ip, 0) + 1
    return counts

def failures_by_username(entries: list[dict[str, str]]) -> dict[str, int]:
    counts = {}
    for entry in entries:
        username = entry["username"]
        counts[username] = counts.get(username, 0) + 1
    return counts

def top_offenders(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]:
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)[:n]

def summary_report(entries: list[dict[str, str]]) -> str:
    total_failed_attempts = len(entries)
    ip_counts = failures_by_ip(entries)
    username_counts = failures_by_username(entries)
    unique_ip = len(ip_counts)
    unique_usernames = len(username_counts)
    top_offender_list = top_offenders(ip_counts, 3)

    offender_lines = "\n".join(
        f"  {ip}: {count} attempts" for ip, count in top_offender_list
    )

    suspicious_usernames_attempted_5_times = "\n".join(
        f"  {username}: {count} attempts"
        for username, count in username_counts.items()
        if count >= 5
    )

    return (
        f"=== Login Failure Report ===\n"
        f"  Total failed attempts : {total_failed_attempts}\n"
        f"  Unique IPs            : {unique_ip}\n"
        f"  Unique usernames      : {unique_usernames}\n\n"
        f"Top offenders (by attempt count):\n{offender_lines}\n\n"
        f"Suspicious usernames (attempted 5+ times):\n{suspicious_usernames_attempted_5_times}\n"
    )

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