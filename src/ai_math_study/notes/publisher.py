"""Fail-closed publication of new note files."""

from __future__ import annotations

import os
from pathlib import Path


class PublishError(OSError):
    """Raised when durable no-replace publication cannot be guaranteed."""


def publish_new(target: Path, data: bytes) -> None:
    """Fsync a sibling partial and atomically publish it without replacement.

    A hard link is the portable primitive with atomic no-replace semantics used
    here. Filesystems that do not support it are rejected rather than emulated.
    """

    target = Path(target)
    partial = target.with_name(target.name + ".partial")
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        fd = os.open(partial, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as exc:
        raise PublishError(f"partial path already exists: {partial}") from exc
    try:
        with os.fdopen(fd, "wb", closefd=True) as stream:
            stream.write(data)
            stream.flush()
            os.fsync(stream.fileno())
        try:
            os.link(partial, target)
        except FileExistsError as exc:
            raise PublishError(f"target already exists: {target}") from exc
        except OSError as exc:
            raise PublishError("atomic no-replace publication is unavailable") from exc
    finally:
        try:
            partial.unlink()
        except FileNotFoundError:
            pass

