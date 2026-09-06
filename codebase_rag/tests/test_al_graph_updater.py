from pathlib import Path
from unittest.mock import MagicMock

from codebase_rag import constants as cs
from codebase_rag.graph_updater import GraphUpdater
from codebase_rag.parser_loader import load_parsers

PAGE_AL = """page 50107 LinkPage
{
    SourceTable = Customer;
    layout { area(Content) { field(Name; Rec.Name) { } } }
}
"""


def _run(repo: Path, ingestor: MagicMock) -> list[str]:
    parsers, queries = load_parsers()
    GraphUpdater(
        ingestor=ingestor, repo_path=repo, parsers=parsers, queries=queries
    ).run()
    return [c.args[0] for c in ingestor.execute_write.call_args_list]


def test_al_run_links_displayed_fields(
    temp_repo: Path, mock_ingestor: MagicMock
) -> None:
    (temp_repo / "page.al").write_text(PAGE_AL, encoding="utf-8")
    assert cs.CYPHER_LINK_AL_DISPLAYED_FIELDS in _run(temp_repo, mock_ingestor)


def test_non_al_run_skips_the_link_pass(
    temp_repo: Path, mock_ingestor: MagicMock
) -> None:
    (temp_repo / "mod.py").write_text("def f():\n    pass\n", encoding="utf-8")
    assert cs.CYPHER_LINK_AL_DISPLAYED_FIELDS not in _run(temp_repo, mock_ingestor)
