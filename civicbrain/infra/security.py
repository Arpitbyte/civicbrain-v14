"""Security helpers: CSV formula injection defenses and sanitization."""


def sanitize_csv_cell(value: str | None) -> str:
    """Neutralize spreadsheet formula injection vulnerabilities (CSV Injection / Formula Injection).

    If a cell value begins with characters interpreted by Excel/Calc as a formula
    (=, +, -, @, tab, newline), prepends a single quote (') to force literal interpretation.
    """
    if not value:
        return ""
    val_str = str(value).strip()
    if val_str and val_str[0] in ("=", "+", "-", "@", "\t", "\r"):
        return f"'{val_str}"
    return val_str
