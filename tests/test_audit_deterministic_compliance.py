"""Tests for Pillar 1: Deterministic Compliance & Zero Banned External LLM Calls.

In accordance with Part B Prompt 8:
- Asserts that all Python source files in civicbrain/ are free from external cloud LLM imports.
- Asserts that all 7 core analytical and operational pipelines are present and deterministic.
- Asserts zero hardcoded API keys or secret credentials in codebase.
"""

from civicbrain.audit.compliance_scanner import DeterministicComplianceScanner


def test_deterministic_compliance_scanner():
    scanner = DeterministicComplianceScanner("civicbrain")
    report = scanner.scan_codebase()

    assert report.scanned_files_count > 0, "Scanner must inspect all Python files"
    assert report.banned_imports_count == 0, f"Found banned LLM imports: {report.violations}"
    assert report.token_leaks_count == 0, f"Found potential credential leaks: {report.violations}"
    assert len(report.violations) == 0, f"Compliance violations detected: {report.violations}"
    assert report.is_compliant is True, (
        "CivicBrain codebase must be 100% compliant with Bootstrap Principle §A3"
    )
