import re
import bleach
from fastapi import HTTPException

MAX_IDEA_LENGTH = 2000

_INJECTION_PATTERNS = [
    r"ignore\s+(previous|all|above)\s+instructions?",
    r"you\s+are\s+now",
    r"act\s+as\s+(a|an|the)",
    r"new\s+persona",
    r"system\s*prompt",
    r"<\s*script",
    r"</\s*script",
    r"DROP\s+TABLE",
    r";\s*DELETE\s+FROM",
    r"UNION\s+SELECT",
    r"jailbreak",
    r"disregard\s+(your|all|any)",
    r"pretend\s+(you\s+are|to\s+be)",
]

_COMPILED = [re.compile(p, re.IGNORECASE) for p in _INJECTION_PATTERNS]


def sanitize(raw: str) -> str:
    if len(raw) > MAX_IDEA_LENGTH:
        raise HTTPException(status_code=400, detail=f"Idea must be under {MAX_IDEA_LENGTH} characters.")

    # Strip all HTML tags and attributes
    cleaned = bleach.clean(raw, tags=[], attributes={}, strip=True)

    # Block prompt injection attempts
    for pattern in _COMPILED:
        if pattern.search(cleaned):
            raise HTTPException(status_code=400, detail="Invalid input detected.")

    # Allow only printable UTF-8 — reject control characters (except newline/tab)
    sanitized = "".join(ch for ch in cleaned if ch.isprintable() or ch in "\n\t")

    if len(sanitized.strip()) < 20:
        raise HTTPException(status_code=400, detail="Idea is too short. Please describe it in at least 20 characters.")

    return sanitized.strip()
