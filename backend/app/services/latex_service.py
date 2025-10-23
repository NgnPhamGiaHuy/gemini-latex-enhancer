"""
LaTeX Service for compiling LaTeX to PDF.

This module wraps interactions with the system LaTeX toolchain (LuaLaTeX) and
adds defensive checks to improve reliability when running in different
environments (local dev, containers, CI).
"""

import subprocess
import os
import signal
from typing import Optional
import re
from app.config import settings
from app.utils.logger import get_logger

logger = get_logger(__name__)


class LatexService:
    """Service for validating and compiling LaTeX content to PDF."""

    @staticmethod
    def validate_latex_content(latex_content: str) -> bool:
        """Check whether LaTeX contains essential document structure.

        This validator performs inexpensive checks to catch common issues early
        (such as markdown code fences, missing document markers, or undefined
        control sequences) before invoking the LaTeX toolchain.

        Args:
            latex_content: Candidate LaTeX source string.

        Returns:
            True when content looks valid; False otherwise.
        """
        try:
            # Check for basic LaTeX structure
            if not latex_content.strip().startswith("\\documentclass"):
                logger.error("LaTeX content does not start with \\documentclass")
                return False

            if not latex_content.strip().endswith("\\end{document}"):
                logger.error("LaTeX content does not end with \\end{document}")
                return False

            # Check for common issues
            if "```" in latex_content:
                logger.error("LaTeX content contains markdown code blocks")
                return False

            # Check for undefined control sequences that commonly cause compilation errors
            undefined_sequences = [
                "\\textasciimdash",
                "\\textasciitilde",
                "\\textasciicircum",
            ]

            for sequence in undefined_sequences:
                if sequence in latex_content:
                    logger.error(
                        f"LaTeX content contains undefined control sequence: {sequence}"
                    )
                    return False

            # Check for regex artifacts that cause undefined control sequences
            if re.search(r"\\[0-9]+", latex_content):
                logger.error("LaTeX content contains regex artifacts (\\1, \\2, etc.)")
                return False

            logger.info("LaTeX content validation passed")
            return True

        except Exception as e:
            logger.error(f"LaTeX validation failed: {str(e)}")
            return False

    @staticmethod
    def compile_to_pdf(tex_path: str) -> Optional[str]:
        """Compile a `.tex` file into a PDF using lualatex.

        The method prefers running in the file's output directory, falls back
        to an alternative approach when necessary, and returns the absolute
        path to the generated PDF on success.

        Args:
            tex_path: Absolute or relative path to the `.tex` file.

        Returns:
            Absolute path to the produced PDF, or None on failure.
        """
        try:
            # Ensure output directory exists
            output_dir = os.path.dirname(tex_path)
            tex_filename = os.path.basename(tex_path)

            logger.info(f"LaTeX file path: {tex_path}")
            logger.info(f"Output directory: {output_dir}")
            logger.info(f"LaTeX filename: {tex_filename}")

            # Check if output directory is writable
            if not os.access(output_dir, os.W_OK):
                logger.error(f"Output directory is not writable: {output_dir}")
                return None

            # Check if LaTeX file exists
            if not os.path.exists(tex_path):
                logger.error(f"LaTeX file does not exist: {tex_path}")
                return None

            logger.info(f"✅ LaTeX file exists and output directory is writable")

            # Run lualatex (supports fontspec and modern fonts)
            # Use absolute path to avoid working directory issues
            abs_tex_path = os.path.abspath(tex_path)
            base_without_ext = os.path.splitext(os.path.basename(abs_tex_path))[0]
            safe_jobname = re.sub(r"[^A-Za-z0-9._-]+", "_", base_without_ext)
            cmd = [
                "lualatex",
                "-interaction=nonstopmode",
                "-output-directory",
                output_dir,
                "-jobname",
                safe_jobname,
                "-halt-on-error",
                abs_tex_path,
            ]

            logger.info(f"Compiling LaTeX: {' '.join(cmd)}")
            logger.info(f"Working directory: {output_dir}")

            # Run with timeout from the output directory
            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.LATEX_TIMEOUT,
                cwd=output_dir,
            )

            if process.returncode != 0:
                logger.error(
                    f"LaTeX compilation failed with return code: {process.returncode}"
                )
                logger.error(f"LaTeX stderr: {process.stderr}")
                logger.error(f"LaTeX stdout: {process.stdout}")

                # Try alternative approach - run from current directory
                logger.info("Trying alternative compilation approach...")
                return LatexService._try_alternative_compilation(tex_path)

            # Check if PDF was created (respecting custom jobname)
            pdf_path = os.path.join(output_dir, f"{safe_jobname}.pdf")
            if os.path.exists(pdf_path):
                logger.info(f"PDF created successfully: {pdf_path}")
                return pdf_path
            else:
                logger.error("PDF file was not created")
                return None

        except subprocess.TimeoutExpired:
            logger.error("LaTeX compilation timed out")
            return None
        except FileNotFoundError:
            logger.error(
                "lualatex not found. Please install LaTeX distribution with LuaTeX support."
            )
            return None
        except Exception as e:
            logger.error(f"LaTeX compilation error: {str(e)}")
            return None

    @staticmethod
    def _try_alternative_compilation(tex_path: str) -> Optional[str]:
        """Fallback compilation strategy when the primary run fails.

        Runs lualatex from the project root to mitigate cwd/path edge cases.

        Args:
            tex_path: Path to the `.tex` source file.

        Returns:
            Absolute path to the produced PDF, or None if compilation fails.
        """
        try:
            logger.info("=== ALTERNATIVE COMPILATION STARTED ===")

            # Get absolute path
            abs_tex_path = os.path.abspath(tex_path)
            output_dir = os.path.dirname(abs_tex_path)
            tex_filename = os.path.basename(abs_tex_path)
            base_without_ext = os.path.splitext(tex_filename)[0]
            safe_jobname = re.sub(r"[^A-Za-z0-9._-]+", "_", base_without_ext)

            logger.info(f"Absolute LaTeX path: {abs_tex_path}")
            logger.info(f"Output directory: {output_dir}")
            logger.info(f"LaTeX filename: {tex_filename}")

            # Try running from the project root directory
            project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
            logger.info(f"Project root: {project_root}")

            # Change to project root and run lualatex
            cmd = [
                "lualatex",
                "-interaction=nonstopmode",
                "-output-directory",
                output_dir,
                "-jobname",
                safe_jobname,
                "-halt-on-error",
                abs_tex_path,
            ]

            logger.info(f"Alternative compilation command: {' '.join(cmd)}")

            process = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=settings.LATEX_TIMEOUT,
                cwd=project_root,
            )

            if process.returncode != 0:
                logger.error(
                    f"Alternative compilation failed with return code: {process.returncode}"
                )
                logger.error(f"Alternative stderr: {process.stderr}")
                logger.error(f"Alternative stdout: {process.stdout}")
                return None

            # Check if PDF was created (respecting custom jobname)
            pdf_path = os.path.join(output_dir, f"{safe_jobname}.pdf")
            if os.path.exists(pdf_path):
                logger.info(
                    f"✅ PDF created successfully via alternative method: {pdf_path}"
                )
                return pdf_path
            else:
                logger.error("❌ PDF file was not created via alternative method")
                return None

        except Exception as e:
            logger.error(f"❌ Alternative compilation error: {str(e)}")
            return None

    @staticmethod
    def cleanup_latex_files(tex_path: str):
        """Remove common LaTeX auxiliary files for a given source path.

        This keeps the output directory tidy after compilation attempts.

        Args:
            tex_path: Path to the `.tex` source file.
        """
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
                    logger.debug(f"Cleaned up auxiliary file: {aux_file}")

        except Exception as e:
            logger.warning(f"Failed to cleanup LaTeX files: {str(e)}")
