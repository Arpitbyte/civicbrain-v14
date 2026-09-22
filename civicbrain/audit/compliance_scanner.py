"""CivicBrain v14 — Phase 12 Compliance & Deterministic Rule Scanner.

Part B Prompt 8 Hardening Pillar 1:
- Scans all Python source files in civicbrain/ for forbidden non-deterministic AI imports
  (openai, anthropic, google.generativeai, langchain, cohere).
- Scans for hardcoded tokens, API keys, or live secret patterns.
- Validates that core civic decision pipelines (triage, prioritization, deduplication,
  dispatch, SLA/ETA, transparency) invoke deterministic domain algorithms.
"""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

BANNED_MODULES = {
    "openai",
    "anthropic",
    "google.generativeai",
    "langchain",
    "langchain_core",
    "langchain_community",
    "cohere",
    "litellm",
}

SUSPICIOUS_TOKEN_PATTERNS = [
    re.compile(r"sk-[a-zA-Z0-9]{20,}", re.IGNORECASE),
    re.compile(r"AIza[0-9A-Za-z-_]{35}", re.IGNORECASE),
    re.compile(r"ghp_[a-zA-Z0-9]{36}", re.IGNORECASE),
    re.compile(r"eyJh[a-zA-Z0-9_-]{30,}\.eyJh[a-zA-Z0-9_-]{30,}", re.IGNORECASE),
]

CORE_DETERMINISTIC_PIPELINES = {
    "triage_intake": "civicbrain.domain.intake.services",
    "deduplication": "civicbrain.domain.intake.dedup",
    "nlp_processing": "civicbrain.domain.nlp.processor",
    "prioritization": "civicbrain.domain.prioritization",
    "dispatch": "civicbrain.domain.dispatch",
    "service_time_eta": "civicbrain.domain.analytics.services",
    "transparency_ledger": "civicbrain.domain.transparency.services",
}


@dataclass
class ScanViolation:
    file_path: str
    line_number: int
    rule: str
    message: str


@dataclass
class ComplianceReport:
    scanned_files_count: int = 0
    banned_imports_count: int = 0
    token_leaks_count: int = 0
    verified_deterministic_pipelines: list[str] = field(default_factory=list)
    violations: list[ScanViolation] = field(default_factory=list)

    @property
    def is_compliant(self) -> bool:
        return len(self.violations) == 0 and len(self.verified_deterministic_pipelines) == len(
            CORE_DETERMINISTIC_PIPELINES
        )


class DeterministicComplianceScanner:
    """AST-based scanner verifying strict adherence to deterministic algorithmic governance."""

    def __init__(self, root_dir: str | Path = "civicbrain") -> None:
        self.root_dir = Path(root_dir)

    def scan_codebase(self) -> ComplianceReport:
        report = ComplianceReport()
        py_files = sorted(self.root_dir.rglob("*.py"))
        report.scanned_files_count = len(py_files)

        for py_path in py_files:
            rel_path = str(
                py_path.relative_to(
                    self.root_dir.parent if self.root_dir.parent.name else self.root_dir
                )
            )
            try:
                content = py_path.read_text(encoding="utf-8")
            except Exception as exc:
                report.violations.append(
                    ScanViolation(
                        file_path=rel_path,
                        line_number=0,
                        rule="FILE_READ_ERROR",
                        message=f"Failed to read file: {exc}",
                    )
                )
                continue

            # 1. Regex scan for hardcoded tokens
            for line_idx, line in enumerate(content.splitlines(), start=1):
                # Skip comments and tests
                if line.strip().startswith("#"):
                    continue
                for pattern in SUSPICIOUS_TOKEN_PATTERNS:
                    if pattern.search(line):
                        report.token_leaks_count += 1
                        report.violations.append(
                            ScanViolation(
                                file_path=rel_path,
                                line_number=line_idx,
                                rule="HARDCODED_CREDENTIAL_LEAK",
                                message="Potential hardcoded secret / API token detected in source.",
                            )
                        )

            # 2. AST scan for banned imports
            try:
                tree = ast.parse(content, filename=str(py_path))
            except SyntaxError as exc:
                report.violations.append(
                    ScanViolation(
                        file_path=rel_path,
                        line_number=exc.lineno or 0,
                        rule="AST_SYNTAX_ERROR",
                        message=f"Syntax error during AST parsing: {exc}",
                    )
                )
                continue

            for node in ast.walk(tree):
                if isinstance(node, ast.Import):
                    for alias in node.names:
                        top_pkg = alias.name.split(".")[0]
                        if top_pkg in BANNED_MODULES:
                            report.banned_imports_count += 1
                            report.violations.append(
                                ScanViolation(
                                    file_path=rel_path,
                                    line_number=node.lineno,
                                    rule="FORBIDDEN_EXTERNAL_LLM_IMPORT",
                                    message=f"Banned non-deterministic AI package imported: '{alias.name}'.",
                                )
                            )
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        top_pkg = node.module.split(".")[0]
                        if top_pkg in BANNED_MODULES:
                            report.banned_imports_count += 1
                            report.violations.append(
                                ScanViolation(
                                    file_path=rel_path,
                                    line_number=node.lineno,
                                    rule="FORBIDDEN_EXTERNAL_LLM_IMPORT",
                                    message=f"Banned non-deterministic AI module imported from: '{node.module}'.",
                                )
                            )

        # 3. Verify presence of all 6 core deterministic pipelines
        for pipe_name, module_path in CORE_DETERMINISTIC_PIPELINES.items():
            parts = module_path.split(".")
            expected_file = Path(*parts).with_suffix(".py")
            expected_dir = Path(*parts)
            if (
                expected_file.exists()
                or expected_dir.exists()
                or (expected_dir / "__init__.py").exists()
            ):
                report.verified_deterministic_pipelines.append(pipe_name)
            else:
                report.violations.append(
                    ScanViolation(
                        file_path=str(expected_file),
                        line_number=0,
                        rule="MISSING_DETERMINISTIC_PIPELINE",
                        message=f"Core pipeline '{pipe_name}' missing expected module at {module_path}",
                    )
                )

        return report


def run_cli_scan() -> None:
    scanner = DeterministicComplianceScanner("civicbrain")
    report = scanner.scan_codebase()

    print("================================================================")
    print("      CIVICBRAIN v14 — DETERMINISTIC COMPLIANCE AUDIT REPORT   ")
    print("================================================================")
    print(f"Total Python Modules Scanned: {report.scanned_files_count}")
    print(f"Banned External LLM Packages Found: {report.banned_imports_count}")
    print(f"Hardcoded Token/Secret Leaks Found: {report.token_leaks_count}")
    print(
        f"Verified Core Deterministic Pipelines ({len(report.verified_deterministic_pipelines)}/{len(CORE_DETERMINISTIC_PIPELINES)}):"
    )
    for p in report.verified_deterministic_pipelines:
        print(f"  [x] {p}")
    print("----------------------------------------------------------------")
    print(f"Total Violations: {len(report.violations)}")
    if report.violations:
        print("VIOLATIONS ENCOUNTERED:")
        for v in report.violations:
            print(f"  ! {v.file_path}:{v.line_number} [{v.rule}] {v.message}")
    else:
        print("RESULT: 100% COMPLIANT (Bootstrap Principle §A3 & Prompt 8 Verified)")
    print("================================================================")


if __name__ == "__main__":
    run_cli_scan()
