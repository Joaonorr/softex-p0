"""Exceções da aplicação. As mensagens são seguras para exibir ao usuário."""


class TriagemError(Exception):
    """Erro esperado; a mensagem explica ao usuário o que fazer."""


class LLMError(TriagemError):
    """Falha ao obter uma resposta válida do LLM."""


class RespostaLLMInvalidaError(LLMError):
    """O LLM respondeu, mas fora do formato esperado."""
