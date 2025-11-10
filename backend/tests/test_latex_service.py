import textwrap

from app.infrastructure.latex.latex_sanitizer import LatexSanitizer


def _dedent(latex: str) -> str:
    return textwrap.dedent(latex).lstrip()


def test_sanitizer_escapes_plain_text_and_preserves_comments():
    latex = _dedent(
        r"""
        \documentclass{article}
        %---------- Packages ----------
        \begin{document}
        Skills: Data & Analytics 100% accurate
        % comment with & and %
        \end{document}
        """
    )

    sanitized = LatexSanitizer.sanitize_content(latex)

    assert "Data \\& Analytics 100\\% accurate" in sanitized
    assert "%---------- Packages ----------" in sanitized
    assert r"\%---------- Packages ----------" not in sanitized
    assert "% comment with & and %" in sanitized
    assert r"\% comment with \& and \%" not in sanitized


def test_sanitizer_preserves_tabular_ampersand():
    latex = _dedent(
        r"""
        \documentclass{article}
        \begin{document}
        \begin{tabular}{ll}
        Key & Value \\
        \end{tabular}
        \end{document}
        """
    )

    sanitized = LatexSanitizer.sanitize_content(latex)

    assert "Key & Value" in sanitized
    assert "Key \\& Value" not in sanitized


def test_sanitizer_preserves_verb_macro():
    latex = _dedent(
        r"""
        \documentclass{article}
        \begin{document}
        \verb|A&B|
        \end{document}
        """
    )

    sanitized = LatexSanitizer.sanitize_content(latex)
    assert r"\verb|A&B|" in sanitized


def test_sanitizer_handles_href_arguments():
    latex = _dedent(
        r"""
        \documentclass{article}
        \begin{document}
        \href{https://example.com/?q=1&lang=en}{Data & Analytics}
        \end{document}
        """
    )

    sanitized = LatexSanitizer.sanitize_content(latex)

    assert "{https://example.com/?q=1\\&lang=en}" in sanitized
    assert "{Data \\& Analytics}" in sanitized


def test_sanitize_tex_file_updates_disk(tmp_path):
    source = _dedent(
        r"""
        \documentclass{article}
        \begin{document}
        Skills: Data & Analytics 100% accurate
        \begin{tabular}{ll}
        Key & Value \\
        \end{tabular}
        \verb|A&B|
        \end{document}
        """
    )

    tex_path = tmp_path / "sample.tex"
    tex_path.write_text(source, encoding="utf-8")

    LatexSanitizer.sanitize_file(tex_path)

    updated = tex_path.read_text(encoding="utf-8")
    assert "Data \\& Analytics 100\\% accurate" in updated
    assert "Key & Value" in updated
    assert r"\verb|A&B|" in updated
