#!/usr/bin/env python3
"""Validate adaptive-dev-loop skill structure and protected invariants."""

from __future__ import annotations

import re
import sys
from pathlib import Path

SKILL_ROOT_PARENT_INDEX = 1
FIRST_STAGE = 1
LAST_STAGE = 8
EXIT_OK = 0
EXIT_FAILED_CHECKS = 1
EXIT_MISSING_SKILL = 2

ROOT = Path(__file__).resolve().parents[SKILL_ROOT_PARENT_INDEX]
SKILL = ROOT / "SKILL.md"
REFERENCES = ROOT / "references"

REQUIRED_STAGES = [f"步骤 {index}" for index in range(FIRST_STAGE, LAST_STAGE + 1)]
REQUIRED_TEMPLATES = [
    "readme-template.md",
    "analysis-template.md",
    "tasks-template.md",
    "iteration-log-template.md",
    "final-report-template.md",
]
PROTECTED_SKILL_TERMS = ["自适应循环", "迭代上限", "收敛", "步骤 9"]
PROTECTED_REFERENCE_TERMS = {
    "references/evolution.md": ["审批门", "回滚", "保护区"],
    "references/boundaries.md": ["绝不做", "掩盖"],
}
GATE_TERMS = ["按推荐自动推进", "候选方案", "推荐项", "验收标准", "授权依据"]


class Reporter:
    def __init__(self) -> None:
        self.passed = 0
        self.failed = 0

    def ok(self, message: str) -> None:
        print(f"  OK {message}")
        self.passed += 1

    def no(self, message: str) -> None:
        print(f"  FAIL {message}")
        self.failed += 1


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def check_frontmatter(reporter: Reporter, skill_text: str) -> None:
    print("[1] frontmatter")
    reporter.ok("name") if re.search(r"^name:", skill_text, re.M) else reporter.no("missing name")
    if re.search(r"^description:", skill_text, re.M):
        reporter.ok("description")
        return
    reporter.no("missing description")


def check_references(reporter: Reporter, skill_text: str) -> None:
    print("[2] references")
    used = set(re.findall(r"references/[A-Za-z0-9_-]+\.md", skill_text))
    actual = {f"references/{path.name}" for path in REFERENCES.glob("*.md")}
    report_set(reporter, sorted(used - actual), "dead references")
    report_set(reporter, sorted(actual - used), "orphan references")


def report_set(reporter: Reporter, items: list[str], label: str) -> None:
    if items:
        reporter.no(f"{label}: {', '.join(items)}")
        return
    reporter.ok(f"no {label}")


def check_skill_terms(reporter: Reporter, skill_text: str) -> None:
    print("[3] protected skill terms")
    for term in REQUIRED_STAGES + PROTECTED_SKILL_TERMS:
        reporter.ok(term) if term in skill_text else reporter.no(f"missing {term}")


def check_templates(reporter: Reporter) -> None:
    print("[4] templates")
    for template in REQUIRED_TEMPLATES:
        path = REFERENCES / template
        reporter.ok(template) if path.exists() else reporter.no(f"missing {template}")


def check_reference_terms(reporter: Reporter) -> None:
    print("[5] protected reference terms")
    for relative_path, terms in PROTECTED_REFERENCE_TERMS.items():
        text = read_text(ROOT / relative_path)
        for term in terms:
            reporter.ok(f"{relative_path}: {term}") if term in text else reporter.no(f"{relative_path}: missing {term}")


def check_gate_terms(reporter: Reporter) -> None:
    print("[6] confirmation gate terms")
    combined = "\n".join(read_text(path) for path in [SKILL, REFERENCES / "grilling.md", REFERENCES / "analysis-template.md"])
    for term in GATE_TERMS:
        reporter.ok(term) if term in combined else reporter.no(f"missing {term}")


def main() -> int:
    if not SKILL.exists():
        print(f"missing SKILL.md under {ROOT}")
        return EXIT_MISSING_SKILL
    reporter = Reporter()
    skill_text = read_text(SKILL)
    check_frontmatter(reporter, skill_text)
    check_references(reporter, skill_text)
    check_skill_terms(reporter, skill_text)
    check_templates(reporter)
    check_reference_terms(reporter)
    check_gate_terms(reporter)
    print(f"\nstructure-check: PASS={reporter.passed} FAIL={reporter.failed}")
    return EXIT_OK if reporter.failed == 0 else EXIT_FAILED_CHECKS


if __name__ == "__main__":
    sys.exit(main())
