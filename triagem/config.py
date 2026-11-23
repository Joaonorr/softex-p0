"""Configuração lida de variáveis de ambiente e, opcionalmente, de um arquivo .env.

Credenciais e endereços nunca ficam no código: vêm de variáveis de ambiente.
Variáveis já definidas no ambiente têm prioridade sobre o arquivo .env.
"""

import os
from dataclasses import dataclass, field
from pathlib import Path

DEFAULT_BASE_URL = "http://localhost:11434"
DEFAULT_MODEL = "qwen2.5:7b-instruct"
DEFAULT_TIMEOUT_SECONDS = 30.0


def carregar_arquivo_env(caminho: Path) -> None:
    """Carrega pares CHAVE=VALOR de um arquivo .env sem sobrescrever o ambiente."""
    if not caminho.is_file():
        return
    for linha in caminho.read_text(encoding="utf-8").splitlines():
        linha = linha.strip()
        if not linha or linha.startswith("#") or "=" not in linha:
            continue
        chave, valor = linha.split("=", 1)
        valor = valor.strip().strip('"').strip("'")
        os.environ.setdefault(chave.strip(), valor)


@dataclass(frozen=True)
class Settings:
    base_url: str
    model: str
    # repr=False: o token nunca aparece em logs, reprs ou mensagens de erro.
    api_key: str = field(repr=False)
    timeout_seconds: float = DEFAULT_TIMEOUT_SECONDS

    @classmethod
    def from_env(cls, arquivo_env: Path = Path(".env")) -> "Settings":
        carregar_arquivo_env(arquivo_env)
        return cls(
            base_url=os.environ.get("LLM_BASE_URL", DEFAULT_BASE_URL).rstrip("/"),
            model=os.environ.get("LLM_MODEL", DEFAULT_MODEL),
            api_key=os.environ.get("LLM_API_KEY", ""),
            timeout_seconds=float(os.environ.get("LLM_TIMEOUT_SECONDS", DEFAULT_TIMEOUT_SECONDS)),
        )
