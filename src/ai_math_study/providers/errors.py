class LLMProviderError(RuntimeError):
    """Base error for an LLM call. Providers never silently fall back."""


class MissingAPIKeyError(LLMProviderError):
    pass


class ModelUnavailableError(LLMProviderError):
    pass


class ResponseIncompleteError(LLMProviderError):
    pass


class ResponseRefusedError(LLMProviderError):
    pass


class ResponseSchemaError(LLMProviderError):
    pass


class CallBudgetExhaustedError(LLMProviderError):
    pass


class LocalOnlyError(LLMProviderError):
    pass
