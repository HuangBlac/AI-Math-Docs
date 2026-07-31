"""Evidence-preserving multi-agent note organization.

The orchestration exports are loaded lazily so low-level validation can import the
protection scanner without creating a validation -> notes -> orchestrator cycle.
"""

from typing import Any

from .protection import (
    ProtectedBlock,
    ProtectedTokenError,
    ProtectionBundle,
    protect_markdown,
    restore_markdown,
    validate_token_bijection,
)


def __getattr__(name: str) -> Any:
    if name in {"NoteApplyError", "NoteOrganizationError", "NoteOrganizer", "apply_note_proposal"}:
        from . import orchestrator

        return getattr(orchestrator, name)
    raise AttributeError(name)

__all__ = [
    "NoteApplyError",
    "NoteOrganizationError",
    "NoteOrganizer",
    "ProtectedBlock",
    "ProtectedTokenError",
    "ProtectionBundle",
    "apply_note_proposal",
    "protect_markdown",
    "restore_markdown",
    "validate_token_bijection",
]
