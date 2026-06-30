"""
shared/document_reader.py

Reads .txt and .pdf files into plain text.
Used by specialists to ingest user-uploaded requirement documents.
"""

from __future__ import annotations
import pathlib
from typing import Any


TOOL_DEFINITION: dict[str, Any] = {
    "name": "read_document",
    "description": (
        "Read a .txt or .pdf file and return its text content. "
        "Use this when the user provides a document describing what board to build. "
        "Documents are typically placed in the inputs/ folder."
    ),
    "input_schema": {
        "type": "object",
        "properties": {
            "path": {
                "type": "string",
                "description": "Path to the .txt or .pdf file (absolute or relative to the project root).",
            }
        },
        "required": ["path"],
    },
}


def read_document(path: str) -> str:
    p = pathlib.Path(path)
    if not p.exists():
        return f"ERROR: File not found: {path}"

    suffix = p.suffix.lower()

    if suffix == ".txt":
        return p.read_text(encoding="utf-8")

    if suffix == ".pdf":
        try:
            import pypdf  # type: ignore
        except ImportError:
            return "ERROR: pypdf is not installed. Run: pip install pypdf"
        reader = pypdf.PdfReader(str(p))
        pages = [page.extract_text() or "" for page in reader.pages]
        return "\n\n".join(pages).strip()

    return f"ERROR: Unsupported file type '{suffix}'. Supported: .txt, .pdf"


def handle(args: dict[str, Any]) -> str:
    return read_document(args["path"])
