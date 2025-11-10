from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Optional

from app.application.contracts.latex_compiler import LatexCompiler, CompilationResult
from app.application.contracts.output_packager import OutputPackager
from app.application.exceptions import ApplicationError
from app.domain.value_objects.file_descriptor import FileDescriptor
from app.utils.logger import get_logger
from app.config import settings

logger = get_logger(__name__)


@dataclass(frozen=True)
class SaveAndCompileResult:
    tex_path: str
    pdf_path: Optional[str]
    tex_relative_path: str
    pdf_relative_path: Optional[str]
    clean_tex_filename: str
    clean_pdf_filename: Optional[str]


class SaveAndCompileUseCase:
    """Persist enhanced LaTeX, then compile to PDF."""

    def __init__(self, *, compiler: LatexCompiler, packager: OutputPackager) -> None:
        self._compiler = compiler
        self._packager = packager

    def execute(
        self,
        *,
        latex_content: str,
        original_filename: Optional[str],
        job_title: str,
        company_name: Optional[str],
        output_root: Optional[Path] = None,
        use_subfolder: bool = False,
    ) -> SaveAndCompileResult:
        base_dir = Path(output_root or settings.SESSION_OUTPUT_DIR)
        base_dir.mkdir(parents=True, exist_ok=True)

        target_dir = base_dir
        if use_subfolder:
            target_dir = self._packager.create_job_subfolder(
                base_dir, company_name or "", job_title
            )

        if original_filename:
            tex_name, pdf_name = (
                self._packager.build_result_filenames_with_original_name(
                    original_filename, company_name or "", job_title
                )
            )
        else:
            tex_name, pdf_name = self._packager.build_result_filenames(
                "cv", company_name or "", job_title
            )

        tex_path = target_dir / tex_name

        try:
            tex_path.write_text(latex_content, encoding="utf-8")
        except Exception as exc:  # noqa: BLE001
            raise ApplicationError(f"Failed to save result: {exc}") from exc

        descriptor = FileDescriptor(tex_path)
        result: Optional[CompilationResult] = self._compiler.compile(descriptor)
        pdf_path = result.pdf_path if result and result.pdf_path.exists() else None

        try:
            self._compiler.cleanup(descriptor)
        except Exception:  # noqa: BLE001
            pass

        tex_relative = os.path.relpath(tex_path, settings.SESSION_OUTPUT_DIR)
        pdf_relative = (
            os.path.relpath(pdf_path, settings.SESSION_OUTPUT_DIR) if pdf_path else None
        )

        clean_pdf = pdf_name if pdf_path else None
        return SaveAndCompileResult(
            tex_path=str(tex_path),
            pdf_path=str(pdf_path) if pdf_path else None,
            tex_relative_path=tex_relative,
            pdf_relative_path=pdf_relative,
            clean_tex_filename=tex_name,
            clean_pdf_filename=clean_pdf,
        )
