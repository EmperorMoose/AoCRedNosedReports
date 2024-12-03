from enum import Enum


class State(Enum):
    SAFE = "SAFE"
    UNSAFE = "UNSAFE"


def is_monotonic(report):
    increasing = all(report[i + 1] > report[i] for i in range(len(report) - 1))
    decreasing = all(report[i + 1] < report[i] for i in range(len(report) - 1))
    if increasing or decreasing:
        return True
    else:
        return False


def is_valid(report):
    gradual = all(
        1 <= abs(report[i + 1] - report[i]) <= 3 for i in range(len(report) - 1)
    )
    if is_monotonic(report) and gradual:
        return True
    else:
        return False


def is_safe(report):
    # if its monotonic and no sequential differences are greater than 3, its safe
    if is_valid(report):
        return State.SAFE

    # now we have an unsafe report. We will remove values 1 by 1 to try and make it safe
    for i in range(len(report)):
        trimmed_report = report[:i] + report[i + 1 :]
        if is_valid(trimmed_report):
            return State.SAFE

    return State.UNSAFE


reports = []
safety_status = []

with open("levels.txt", "r") as file:
    for line in file:
        input = list(map(int, line.split()))
        reports.append(input)

for report in reports:
    safety_status.append(is_safe(report))

safe_count = safety_status.count(State.SAFE)

for report, status in zip(reports, safety_status):
    print(f"Report: {report}, Status: {status}")

print(f"Safe Count: {safe_count}")
