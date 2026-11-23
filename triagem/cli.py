"""Interface de linha de comando: `python -m triagem "texto da solicitação"`."""

import argparse
import sys

from triagem.classifier import classificar
from triagem.config import Settings
from triagem.llm import OllamaClient

MENSAGEM_VAZIA = (
    "Mensagem vazia. Informe o texto da solicitação, por exemplo:\n"
    '  python -m triagem "O botão de login retorna erro 500"\n'
    "ou envie o texto pela entrada padrão:\n"
    '  echo "Gostaria de exportar em PDF" | python -m triagem'
)


def montar_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="triagem",
        description="Classifica uma solicitação como problema, duvida, sugestao ou outro, com resumo.",
    )
    parser.add_argument(
        "mensagem",
        nargs="?",
        help="texto da solicitação (se omitido, lê da entrada padrão)",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = montar_parser().parse_args(argv)

    if args.mensagem is not None:
        texto = args.mensagem
    elif not sys.stdin.isatty():
        texto = sys.stdin.read()
    else:
        texto = ""
    texto = texto.strip()
    if not texto:
        print(MENSAGEM_VAZIA, file=sys.stderr)
        return 2

    settings = Settings.from_env()
    resultado = classificar(texto, OllamaClient(settings))

    print(f"Categoria: {resultado.categoria}")
    print(f"Resumo: {resultado.resumo}")
    return 0
