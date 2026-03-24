from codebase_rag import constants as cs
from codebase_rag.language_spec import LANGUAGE_FQN_SPECS, LANGUAGE_SPECS
from codebase_rag.parsers.handlers.registry import get_handler


def test_al_language_spec_exists():
    assert cs.SupportedLanguage.AL in LANGUAGE_SPECS
    spec = LANGUAGE_SPECS[cs.SupportedLanguage.AL]
    assert spec.language == cs.SupportedLanguage.AL
    assert ".al" in spec.file_extensions


def test_al_fqn_spec_exists():
    assert cs.SupportedLanguage.AL in LANGUAGE_FQN_SPECS


def test_al_handler_registered():
    handler = get_handler(cs.SupportedLanguage.AL)
    assert handler is not None
