from __future__ import annotations

import os
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any, List, Tuple

from pylatexenc.latexwalker import (  # type: ignore[import]
    LatexWalker,
    LatexWalkerParseError,
    LatexCharsNode,
    LatexGroupNode,
    LatexEnvironmentNode,
    LatexMacroNode,
    LatexMathNode,
    LatexCommentNode,
    LatexSpecialsNode,
)

from app.utils.logger import get_logger

logger = get_logger(__name__)


_VERBATIM_ENVIRONMENTS = {
    "verbatim",
    "Verbatim",
    "lstlisting",
    "minted",
}
_VERBATIM_MACROS = {
    "verb",
    "Verb",
    "url",
    "path",
}
_TABULAR_ENV_PREFIXES = ("tabular", "array", "longtable", "tabu")
_MATH_ENVIRONMENTS = {
    "math",
    "displaymath",
    "equation",
    "equation*",
    "align",
    "align*",
    "gather",
    "gather*",
    "multline",
    "multline*",
    "split",
    "cases",
}


@dataclass(frozen=True)
class _TraversalContext:
    in_tabular: bool = False
    in_math: bool = False
    in_verbatim: bool = False
    in_document: bool = False

    def with_tabular(self) -> "_TraversalContext":
        if self.in_tabular:
            return self
        return _TraversalContext(True, self.in_math, self.in_verbatim, self.in_document)

    def with_math(self) -> "_TraversalContext":
        if self.in_math:
            return self
        return _TraversalContext(
            self.in_tabular, True, self.in_verbatim, self.in_document
        )

    def with_verbatim(self) -> "_TraversalContext":
        if self.in_verbatim:
            return self
        return _TraversalContext(self.in_tabular, self.in_math, True, self.in_document)

    def with_document(self) -> "_TraversalContext":
        if self.in_document:
            return self
        return _TraversalContext(
            self.in_tabular,
            self.in_math,
            self.in_verbatim,
            True,
        )


@dataclass
class _TraversalState:
    documentclass_seen: bool = False
    document_environment_seen: bool = False


class LatexSanitizer:
    """Utilities for sanitising LaTeX sources prior to compilation."""

    @classmethod
    def sanitize_content(cls, content: str) -> str:
        try:
            return cls._sanitize_content(content)
        except LatexWalkerParseError as exc:
            logger.warning(
                "AST-based LaTeX sanitization failed (%s). Falling back to regex sanitizer.",
                exc,
            )
            return cls._fallback_sanitize(content)
        except Exception as exc:  # noqa: BLE001
            logger.warning(
                "Unexpected error during LaTeX sanitization (%s). Falling back to regex sanitizer.",
                exc,
            )
            return cls._fallback_sanitize(content)

    @classmethod
    def sanitize_file(cls, tex_path: str | Path) -> None:
        tex_path = Path(tex_path)
        try:
            content = tex_path.read_text(encoding="utf-8")
        except FileNotFoundError:
            raise

        sanitized = cls.sanitize_content(content)

        if sanitized != content:
            tex_path.write_text(sanitized, encoding="utf-8")
            logger.info("Preflight sanitization applied to LaTeX source")
        else:
            logger.info("Preflight sanitization not needed (no changes)")

    @classmethod
    def cleanup_aux_files(cls, tex_path: str | Path) -> None:
        tex_path = str(tex_path)
        try:
            base_path = tex_path.replace(".tex", "")
            aux_files = [
                f"{base_path}.aux",
                f"{base_path}.log",
                f"{base_path}.out",
                f"{base_path}.toc",
                f"{base_path}.fdb_latexmk",
                f"{base_path}.fls",
                f"{base_path}.synctex.gz",
            ]

            for aux_file in aux_files:
                if os.path.exists(aux_file):
                    os.remove(aux_file)
                    logger.debug("Cleaned up auxiliary file: %s", aux_file)

        except Exception as exc:  # noqa: BLE001
            logger.warning("Failed to cleanup LaTeX files: %s", exc)

    @classmethod
    def _sanitize_content(cls, content: str) -> str:
        walker = LatexWalker(content)
        nodelist, _, _ = walker.get_latex_nodes()

        replacements: List[Tuple[int, int, str]] = []
        state = _TraversalState()
        cls._collect_replacements(
            nodelist,
            content,
            _TraversalContext(),
            replacements,
            state,
        )

        sanitized = cls._apply_replacements(content, replacements)

        if not state.documentclass_seen:
            logger.warning(
                "Sanitizer did not detect a \\documentclass macro. LaTeX structure may be incomplete."
            )
        if not state.document_environment_seen:
            logger.warning(
                "Sanitizer did not detect a document environment. Verify \\begin{document} / \\end{document} exist."
            )

        return sanitized

    @classmethod
    def _collect_replacements(
        cls,
        nodes: Any,
        content: str,
        context: "_TraversalContext",
        replacements: List[Tuple[int, int, str]],
        state: "_TraversalState",
    ):
        if not nodes:
            return

        for node in nodes:
            cls._process_node(node, content, context, replacements, state)

    @classmethod
    def _process_node(
        cls,
        node,
        content: str,
        context: "_TraversalContext",
        replacements: List[Tuple[int, int, str]],
        state: "_TraversalState",
    ):
        if isinstance(node, LatexCharsNode):
            if context.in_verbatim or context.in_math or context.in_tabular:
                return
            sanitized = cls._escape_specials_in_text(node.chars)
            if sanitized != node.chars:
                replacements.append((node.pos, node.pos + node.len, sanitized))
            return

        if isinstance(node, LatexCommentNode):
            if not context.in_document:
                return
            segment = content[node.pos : node.pos + node.len]
            line_start = content.rfind("\n", 0, node.pos) + 1
            line_prefix = content[line_start : node.pos]
            if line_prefix.strip():
                escaped = "\\%" + segment[1:]
                replacements.append((node.pos, node.pos + node.len, escaped))
            return

        if isinstance(node, LatexSpecialsNode):
            if context.in_tabular or context.in_math or context.in_verbatim:
                return
            specials = getattr(node, "specials_chars", "")
            sanitized = cls._escape_specials_in_text(specials)
            if sanitized != specials:
                replacements.append((node.pos, node.pos + node.len, sanitized))
            return

        if isinstance(node, LatexEnvironmentNode):
            env_name = (node.environmentname or "").strip()
            if env_name == "document":
                state.document_environment_seen = True
                context = context.with_document()

            env_lower = env_name.lower()
            if env_lower in _VERBATIM_ENVIRONMENTS:
                return
            if cls._is_tabular_environment(env_lower):
                return

            new_context = context
            if cls._is_math_environment(env_lower):
                new_context = context.with_math()

            cls._collect_replacements(
                node.nodelist,
                content,
                new_context,
                replacements,
                state,
            )
            return

        if isinstance(node, LatexMathNode):
            new_context = context.with_math()
            cls._collect_replacements(
                getattr(node, "nodelist", None),
                content,
                new_context,
                replacements,
                state,
            )
            return

        if isinstance(node, LatexGroupNode):
            cls._collect_replacements(
                node.nodelist,
                content,
                context,
                replacements,
                state,
            )
            return

        if isinstance(node, LatexMacroNode):
            macroname = (node.macroname or "").strip()
            if macroname == "documentclass":
                state.documentclass_seen = True

            if macroname in _VERBATIM_MACROS:
                return

            nodeargd = getattr(node, "nodeargd", None)
            if nodeargd:
                for idx, arg in enumerate(nodeargd.argnlist):
                    if arg is None:
                        continue
                    if macroname == "href" and idx == 0:
                        continue
                    cls._collect_replacements(
                        getattr(arg, "nodelist", None),
                        content,
                        context,
                        replacements,
                        state,
                    )
            return

        if hasattr(node, "nodelist"):
            cls._collect_replacements(
                getattr(node, "nodelist", None),
                content,
                context,
                replacements,
                state,
            )

    @staticmethod
    def _apply_replacements(
        content: str, replacements: List[Tuple[int, int, str]]
    ) -> str:
        if not replacements:
            return content

        updated = content
        for start, end, replacement in sorted(
            replacements, key=lambda item: item[0], reverse=True
        ):
            updated = updated[:start] + replacement + updated[end:]
        return updated

    @classmethod
    def _fallback_sanitize(cls, content: str) -> str:
        tabular_pattern = r"\\begin\{tabular[^}]*\}(.*?)\\end\{tabular[^}]*\}"
        segments = []
        last_end = 0
        for match in re.finditer(tabular_pattern, content, re.DOTALL):
            if match.start() > last_end:
                pre = content[last_end : match.start()]
                segments.append(cls._escape_specials_in_text(pre))
            segments.append(match.group(0))
            last_end = match.end()

        if last_end < len(content):
            tail = content[last_end:]
            segments.append(cls._escape_specials_in_text(tail))

        return "".join(segments)

    @staticmethod
    def _is_tabular_environment(env_name: str) -> bool:
        return any(env_name.startswith(prefix) for prefix in _TABULAR_ENV_PREFIXES)

    @staticmethod
    def _is_math_environment(env_name: str) -> bool:
        return (
            env_name in _MATH_ENVIRONMENTS
            or env_name.endswith("matrix")
            or env_name.endswith("matrix*")
        )

    @staticmethod
    def _escape_specials_in_text(text: str) -> str:
        if not text:
            return text

        def escape_line(line: str) -> str:
            stripped = line.lstrip()
            if stripped.startswith("%"):
                return line

            escaped = re.sub(r"(?<!\\)&", r"\\&", line)
            escaped = re.sub(r"(?<!\\)\$", r"\\$", escaped)
            escaped = re.sub(r"(?<!\\)#", r"\\#", escaped)
            escaped = re.sub(r"(?<!\\)_", r"\\_", escaped)
            escaped = re.sub(r"(?<![\\%])%", r"\\%", escaped)
            return escaped

        lines = re.split("(\r?\n)", text)
        escaped_lines = [
            escape_line(part) if part not in ("\n", "\r\n") else part for part in lines
        ]
        return "".join(escaped_lines)
