from __future__ import annotations

from typing import TYPE_CHECKING

from ... import constants as cs
from ..handlers.base import BaseLanguageHandler

if TYPE_CHECKING:
    from pathlib import Path

    from ...language_spec import LanguageSpec
    from ...types_defs import ASTNode


class AlHandler(BaseLanguageHandler):
    __slots__ = ()

    def extract_function_name(self, node: ASTNode) -> str | None:
        for child in node.children:
            if child.type in {"identifier", "quoted_identifier"}:
                text = child.text.decode() if child.text else None
                if text and text.startswith('"') and text.endswith('"'):
                    return text[1:-1]
                return text
        return None

    def build_function_qualified_name(
        self,
        node: ASTNode,
        module_qn: str,
        func_name: str,
        lang_config: LanguageSpec | None,
        file_path: Path | None,
        repo_path: Path,
        project_name: str,
    ) -> str:
        return f"{module_qn}{cs.SEPARATOR_DOT}{func_name}"
