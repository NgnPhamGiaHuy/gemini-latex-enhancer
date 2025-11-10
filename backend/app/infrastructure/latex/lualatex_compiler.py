from __future__ import annotations

import os
import re
import subprocess
from pathlib import Path
from typing import Optional

from app.application.contracts.latex_compiler import (
    LatexCompiler,
    CompilationResult,
)
from app.domain.value_objects.file_descriptor import FileDescriptor
from app.infrastructure.latex.latex_sanitizer import LatexSanitizer
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LualatexCompiler(LatexCompiler):
    """Adapter that delegates to LuaLaTeX with preflight sanitisation."""

    def compile(self, descriptor: FileDescriptor) -> Optional[CompilationResult]:
        tex_path = descriptor.resolve()
        output_dir = tex_path.parent

        if not os.access(output_dir, os.W_OK):
            logger.error("Output directory is not writable: %s", output_dir)
            return None
        if not tex_path.exists():
            logger.error("LaTeX file does not exist: %s", tex_path)
            return None

        try:
            LatexSanitizer.sanitize_file(tex_path)
        except Exception as exc:  # noqa: BLE001
            logger.warning("Sanitization failed, continuing: %s", exc)

        safe_jobname = self._safe_jobname(tex_path.stem)

        cmd = [
            "lualatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(output_dir),
            "-jobname",
            safe_jobname,
            "-halt-on-error",
            str(tex_path),
        ]

        logger.info("Executing lualatex: %s", " ".join(cmd))
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.LATEX_TIMEOUT,
                cwd=None,
            )
        except subprocess.TimeoutExpired:
            logger.error("LaTeX compilation timed out")
            return None
        except FileNotFoundError:
            logger.error("lualatex binary not found")
            return None

        if process.returncode != 0:
            logger.error(
                "LaTeX compilation failed (return code: %s)", process.returncode
            )
            # Log first 500 chars of stderr for debugging
            if process.stderr:
                error_preview = process.stderr[:500] + (
                    "..." if len(process.stderr) > 500 else ""
                )
                logger.error("LaTeX stderr preview: %s", error_preview)
            if process.stdout:
                # Look for error patterns in stdout
                error_lines = [
                    line
                    for line in process.stdout.split("\n")
                    if "error" in line.lower() or "!" in line
                ]
                if error_lines:
                    logger.error("LaTeX error lines: %s", "\n".join(error_lines[:5]))
            return self._try_alternative(tex_path, safe_jobname)

        pdf_path = output_dir / f"{safe_jobname}.pdf"
        log_path = output_dir / f"{safe_jobname}.log"
        if not pdf_path.exists():
            logger.error("PDF file not created at %s", pdf_path)
            return None

        return CompilationResult(
            pdf_path=pdf_path, log_path=log_path if log_path.exists() else None
        )

    def cleanup(self, descriptor: FileDescriptor) -> None:
        LatexSanitizer.cleanup_aux_files(descriptor.path)

    @staticmethod
    def _safe_jobname(name: str) -> str:
        return re.sub(r"[^A-Za-z0-9._-]+", "_", name)

    def _try_alternative(
        self, tex_path: Path, safe_jobname: str
    ) -> Optional[CompilationResult]:
        """Fallback compilation strategy mirroring legacy behaviour."""
        abs_path = tex_path.resolve()
        output_dir = abs_path.parent

        project_root = Path(__file__).resolve().parents[3]
        cmd = [
            "lualatex",
            "-interaction=nonstopmode",
            "-output-directory",
            str(output_dir),
            "-jobname",
            safe_jobname,
            "-halt-on-error",
            str(abs_path),
        ]

        logger.info("Trying alternative compilation approach from %s", project_root)
        try:
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.LATEX_TIMEOUT,
                cwd=str(project_root),
            )
        except subprocess.TimeoutExpired:
            logger.error("Alternative LaTeX compilation timed out")
            return None
        except FileNotFoundError:
            logger.error("lualatex binary not found during alternative attempt")
            return None

        if process.returncode != 0:
            logger.error(
                "Alternative compilation failed (return code: %s)", process.returncode
            )
            # Log first 500 chars of stderr for debugging
            if process.stderr:
                error_preview = process.stderr[:500] + (
                    "..." if len(process.stderr) > 500 else ""
                )
                logger.error("Alternative LaTeX stderr preview: %s", error_preview)
            if process.stdout:
                # Look for error patterns in stdout
                error_lines = [
                    line
                    for line in process.stdout.split("\n")
                    if "error" in line.lower() or "!" in line
                ]
                if error_lines:
                    logger.error(
                        "Alternative LaTeX error lines: %s", "\n".join(error_lines[:5])
                    )
            return None

        pdf_path = output_dir / f"{safe_jobname}.pdf"
        log_path = output_dir / f"{safe_jobname}.log"
        if not pdf_path.exists():
            logger.error("PDF not created after alternative attempt")
            return None

        return CompilationResult(
            pdf_path=pdf_path, log_path=log_path if log_path.exists() else None
        )
