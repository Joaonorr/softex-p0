"""Cliente HTTP para o Ollama (API /api/chat), usando apenas a biblioteca padrão."""

import json
import urllib.request

from triagem.config import Settings


class OllamaClient:
    def __init__(self, settings: Settings) -> None:
        self._settings = settings

    def chat(self, messages: list[dict], schema: dict) -> str:
        """Envia as mensagens e devolve o conteúdo textual da resposta do modelo.

        `schema` é um JSON Schema usado pelo Ollama para restringir a saída ao formato pedido.
        """
        corpo = {
            "model": self._settings.model,
            "messages": messages,
            "stream": False,
            "format": schema,
            "options": {"temperature": 0},
        }
        requisicao = urllib.request.Request(
            f"{self._settings.base_url}/api/chat",
            data=json.dumps(corpo).encode("utf-8"),
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {self._settings.api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(requisicao, timeout=self._settings.timeout_seconds) as resposta:
            dados = json.load(resposta)
        return dados["message"]["content"]
