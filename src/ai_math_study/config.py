from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import tomllib
from typing import Any

from ai_math_study.ports.llm import ProviderProfile


@dataclass(frozen=True)
class StudyConfig:
    root: Path
    study_dir: Path
    pdf: Path
    expected_pdf_sha256: str
    chapters: tuple[int, ...]
    markdown_roots: tuple[Path, ...]
    excludes: tuple[str, ...]
    models: dict[str, str]
    model_profiles: dict[str, ProviderProfile]
    openai: dict[str, Any]
    deepseek: dict[str, Any]
    subagents: dict[str, Any]
    mastery: dict[str, int]
    raw: dict[str, Any]

    @classmethod
    def load(cls, path: str | Path = "study.toml") -> "StudyConfig":
        config_path = Path(path).resolve()
        raw = tomllib.loads(config_path.read_text(encoding="utf-8"))
        base = (config_path.parent / raw["project"].get("root", ".")).resolve()
        return cls(
            root=base,
            study_dir=(base / raw["project"]["study_dir"]).resolve(),
            pdf=(base / raw["project"]["pdf"]).resolve(),
            expected_pdf_sha256=raw["project"]["expected_pdf_sha256"].upper(),
            chapters=tuple(int(item) for item in raw["project"]["chapters"]),
            markdown_roots=tuple((base / item).resolve() for item in raw["sources"]["markdown_roots"]),
            excludes=tuple(raw["sources"].get("exclude", [])),
            models={key: str(value) for key, value in raw["models"].items()},
            model_profiles={
                role: ProviderProfile(
                    provider=str(value["provider"]),
                    model=str(value["model"]),
                    thinking=bool(value.get("thinking", False)),
                    reasoning_effort=value.get("reasoning_effort"),
                )
                for role, value in raw.get("model_profiles", {}).items()
            },
            openai=dict(raw.get("openai", {})),
            deepseek=dict(raw.get("deepseek", {})),
            subagents=dict(raw["subagents"]),
            mastery={key: int(value) for key, value in raw["mastery"].items()},
            raw=raw,
        )

    def verify_pdf(self) -> str:
        digest = sha256(self.pdf.read_bytes()).hexdigest().upper()
        if digest != self.expected_pdf_sha256:
            raise ValueError(
                f"LFTP PDF hash mismatch: expected {self.expected_pdf_sha256}, got {digest}"
            )
        return digest
