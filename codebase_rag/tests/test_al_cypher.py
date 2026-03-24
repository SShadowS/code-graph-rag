from codebase_rag.cypher_queries import (
    CYPHER_DELETE_PROJECT,
    CYPHER_PRUNE_ORPHAN_STUBS,
    build_create_node_query,
    build_merge_node_query,
)


def test_merge_node_query_no_extra_labels():
    query = build_merge_node_query("Class", "qualified_name")
    assert query == "MERGE (n:Class {qualified_name: row.id})\nSET n += row.props"


def test_merge_node_query_with_extra_labels():
    query = build_merge_node_query("Class", "qualified_name", extra_labels=("Table",))
    assert "SET n:Table" in query
    assert "MERGE (n:Class {qualified_name: row.id})" in query
    assert query.endswith("SET n += row.props")


def test_merge_node_query_multiple_extra_labels():
    query = build_merge_node_query(
        "Class", "qualified_name", extra_labels=("Table", "ExternalObject")
    )
    assert "SET n:Table" in query
    assert "SET n:ExternalObject" in query


def test_create_node_query_no_extra_labels():
    query = build_create_node_query("Field", "qualified_name")
    assert query == "CREATE (n:Field {qualified_name: row.id})\nSET n += row.props"


def test_create_node_query_with_extra_labels():
    query = build_create_node_query(
        "Class", "qualified_name", extra_labels=("Codeunit",)
    )
    assert "SET n:Codeunit" in query


def test_delete_project_includes_al_relationships():
    for rel in [
        "HAS_FIELD",
        "HAS_KEY",
        "HAS_TRIGGER",
        "HAS_ACTION",
        "HAS_DATAITEM",
        "READS_TABLE",
        "DISPLAYS_FIELD",
    ]:
        assert rel in CYPHER_DELETE_PROJECT, f"{rel} missing from delete query"


def test_prune_orphan_stubs_query():
    assert "ExternalObject" in CYPHER_PRUNE_ORPHAN_STUBS
    assert "EXTENDS" in CYPHER_PRUNE_ORPHAN_STUBS
