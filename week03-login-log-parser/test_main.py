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