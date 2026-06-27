# Week 03 — Login Log Parser

**Concept:** Data structures — lists, dicts, sets, comprehensions, sorting, slicing, unpacking
**Session:** Saturday June 27, 10am–1pm

---

## What You're Building

A command-line tool that reads a login log file, parses each line into structured data, and produces a security-relevant summary report.

```
$ python main.py auth.log

=== Login Failure Report ===
Total failed attempts : 847
Unique IPs            : 23
Unique usernames      : 14

Top offenders (by attempt count):
  192.168.1.105   →  312 attempts
  10.0.0.44       →  198 attempts
  172.16.8.2      →   91 attempts

Suspicious usernames (attempted 5+ times):
  root, admin, ubuntu, pi, test
```

---

## The Log Format

Each line in the log looks like this:

```
Jun 27 03:14:22 server sshd[1234]: Failed password for root from 192.168.1.105 port 54321 ssh2
Jun 27 03:14:25 server sshd[1235]: Accepted password for luther from 10.0.0.1 port 22 ssh2
Jun 27 03:14:31 server sshd[1236]: Failed password for admin from 192.168.1.105 port 54322 ssh2
```

You only care about `Failed password` lines.

---

## What to Build — Four Functions

### 1. `parse_log_line(line: str) -> dict[str, str] | None`

Takes one raw log line. Returns a dict if it's a failed login, `None` if it isn't.

```python
parse_log_line('Jun 27 03:14:22 server sshd[1234]: Failed password for root from 192.168.1.105 port 54321 ssh2')
# → {'timestamp': 'Jun 27 03:14:22', 'username': 'root', 'ip': '192.168.1.105'}

parse_log_line('Jun 27 03:14:25 server sshd[1235]: Accepted password for luther from 10.0.0.1 port 22 ssh2')
# → None  (not a failure)
```

**How:** Split the line on spaces. Check if `"Failed"` is in the line. Extract by index — the format is consistent.

---

### 2. `failures_by_ip(entries: list[dict]) -> dict[str, int]`

Takes the list of parsed failure dicts. Returns a dict mapping each IP to its failure count.

```python
failures_by_ip([
    {'ip': '192.168.1.105', 'username': 'root'},
    {'ip': '192.168.1.105', 'username': 'admin'},
    {'ip': '10.0.0.44',     'username': 'root'},
])
# → {'192.168.1.105': 2, '10.0.0.44': 1}
```

**How:** Loop through entries. Use a dict — if the IP is already a key, increment; if not, set to 1. This is the manual version. After you make it work, rewrite it as a dict comprehension using `Counter` from `collections`.

---

### 3. `top_offenders(counts: dict[str, int], n: int = 5) -> list[tuple[str, int]]`

Takes the IP count dict. Returns the top `n` IPs sorted by attempt count, highest first.

```python
top_offenders({'192.168.1.105': 312, '10.0.0.44': 198, '172.16.8.2': 91}, n=2)
# → [('192.168.1.105', 312), ('10.0.0.44', 198)]
```

**How:** `sorted()` with `key=lambda x: x[1]` and `reverse=True`. Slice with `[:n]`. This is the core sorting + slicing practice for the week.

---

### 4. `summary_report(entries: list[dict]) -> str`

Takes all parsed failure entries. Returns a formatted string — the full report shown at the top.

```python
report = summary_report(entries)
print(report)
```

**How:** Call your other three functions. Use a set comprehension to get unique IPs and unique usernames — `{e['ip'] for e in entries}`. Format the output with f-strings.

---

## `main.py` Structure

```python
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
```

---

## `test_main.py` — What to Test

```python
from main import parse_log_line, failures_by_ip, top_offenders, summary_report

FAILED_LINE = "Jun 27 03:14:22 server sshd[1234]: Failed password for root from 192.168.1.105 port 54321 ssh2"
ACCEPTED_LINE = "Jun 27 03:14:25 server sshd[1235]: Accepted password for luther from 10.0.0.1 port 22 ssh2"


def test_parse_log_line_failed_returns_dict():
    result = parse_log_line(FAILED_LINE)
    assert result is not None
    assert result["username"] == "root"
    assert result["ip"] == "192.168.1.105"


def test_parse_log_line_accepted_returns_none():
    assert parse_log_line(ACCEPTED_LINE) is None


def test_parse_log_line_empty_returns_none():
    assert parse_log_line("") is None


def test_failures_by_ip_counts_correctly():
    entries = [
        {"ip": "1.1.1.1", "username": "root"},
        {"ip": "1.1.1.1", "username": "admin"},
        {"ip": "2.2.2.2", "username": "root"},
    ]
    result = failures_by_ip(entries)
    assert result["1.1.1.1"] == 2
    assert result["2.2.2.2"] == 1


def test_top_offenders_sorted_descending():
    counts = {"a": 10, "b": 50, "c": 30}
    result = top_offenders(counts, n=2)
    assert result[0] == ("b", 50)
    assert result[1] == ("c", 30)


def test_top_offenders_respects_n():
    counts = {"a": 1, "b": 2, "c": 3, "d": 4, "e": 5}
    assert len(top_offenders(counts, n=3)) == 3


def test_summary_report_contains_key_fields():
    entries = [
        {"timestamp": "Jun 27 03:14:22", "ip": "1.1.1.1", "username": "root"},
        {"timestamp": "Jun 27 03:14:25", "ip": "1.1.1.1", "username": "admin"},
        {"timestamp": "Jun 27 03:14:31", "ip": "2.2.2.2", "username": "root"},
    ]
    report = summary_report(entries)
    assert "1.1.1.1" in report
    assert "root" in report
    assert "3" in report  # total failures
```

## Session Order

1. Read the Python docs link from the plan (30 min max)
2. Build `parse_log_line` — get it working with the sample log
3. Build `failures_by_ip` manually, then rewrite as dict comprehension
4. Build `top_offenders` — practice sorting + slicing
5. Build `summary_report` — practice set comprehensions
6. Write all tests — aim for every function covered
7. Run the quality gate — fix everything it flags
8. Commit

```bash
ruff check . && mypy . && bandit -r . && pytest --cov
git add .
git commit -m "week03: login log parser complete"
git push
```

---

## Data Structures Used This Week

| Structure | Where |
|-----------|-------|
| `dict` | One parsed log entry, IP count map |
| `list` | All parsed entries, top offenders result |
| `set` | Unique IPs, unique usernames (in summary) |
| `tuple` | Each `(ip, count)` pair in top offenders |
| List comprehension | Filtering parsed entries from raw lines |
| Dict comprehension | Rewriting `failures_by_ip` after manual version works |
| Set comprehension | Unique IPs and usernames in `summary_report` |