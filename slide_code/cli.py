from typing import Annotated
import pyperclip
import black
import typer
from pygments import highlight
from pygments.lexers import PythonLexer
from pygments.formatters import RtfFormatter


app = typer.Typer()


def format_code(code: str, line_length: int) -> str:
    try:
        return str(black.format_str(code, mode=black.FileMode(line_length=line_length)))
    except black.InvalidInput:
        return code


def highlight_code(code: str, style: str, fontface: str, fontsize: int) -> str:
    return highlight(
        code,
        PythonLexer(),
        RtfFormatter(
            style=style,
            fontface=fontface,
            fontsize=fontsize,
        ),
    )


def copy_code_to_clipboard(code: str):
    pyperclip.copy(code)


def get_code_from_clipboard() -> str:
    return pyperclip.paste()


@app.command()
def main(
    line_length: Annotated[int, typer.Option(help="max characters per line")] = 70,
    style: Annotated[
        str, typer.Option(help="syntax hightlight style to use")
    ] = "borland",
    fontface: Annotated[str, typer.Option(help="Font face to use")] = "Inconsolata",
    fontsize: Annotated[int, typer.Option(help="Font size to use")] = 48,
) -> None:
    code = get_code_from_clipboard()
    formatted_code = format_code(code, line_length)
    highlighted_code = highlight_code(
        code=formatted_code,
        style=style,
        fontface=fontface,
        fontsize=fontsize,
    )
    copy_code_to_clipboard(highlighted_code)


if __name__ == "__main__":
    app()
