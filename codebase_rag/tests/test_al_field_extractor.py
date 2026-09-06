from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.field_extractor import AlFieldExtractor
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

TABLE_AL = b"""
table 50101 "MyTable"
{
    fields
    {
        field(1; "No."; Code[20]) { }
        field(2; "Name"; Text[100]) { }
    }
    keys
    {
        key(PK; "No.") { Clustered = true; }
        key(SK; "Name") { }
    }
}
"""


class MockIngestor:
    def __init__(self):
        self.nodes = []
        self.relationships = []

    def ensure_node_batch(self, label, properties, extra_labels=None):
        self.nodes.append((label, extra_labels, properties))

    def ensure_relationship_batch(self, from_spec, rel_type, to_spec, properties=None):
        self.relationships.append((from_spec, rel_type, to_spec, properties))

    def flush_all(self):
        pass


def _parse_and_extract(src=TABLE_AL):
    root = PARSER.parse(src).root_node
    ingestor = MockIngestor()
    obj_extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = obj_extractor.extract_objects(root, Path("/repo/test.al"), "test")
    field_extractor = AlFieldExtractor(ingestor)
    field_extractor.extract_fields(registry)
    return ingestor, registry


def test_field_nodes_created():
    ingestor, _ = _parse_and_extract()
    field_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.FIELD]
    assert len(field_nodes) == 2
    names = {n[2][cs.KEY_NAME] for n in field_nodes}
    assert names == {"No.", "Name"}


def test_field_properties():
    ingestor, _ = _parse_and_extract()
    no_field = next(
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.FIELD and n[2][cs.KEY_NAME] == "No."
    )
    assert no_field[2]["field_id"] == 1
    assert "field_type" in no_field[2]


def test_field_qualified_name():
    ingestor, _ = _parse_and_extract()
    no_field = next(
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.FIELD and n[2][cs.KEY_NAME] == "No."
    )
    assert no_field[2][cs.KEY_QUALIFIED_NAME] == "Table.50101.MyTable.No."


def test_key_nodes_created():
    ingestor, _ = _parse_and_extract()
    key_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.KEY]
    assert len(key_nodes) == 2


def test_key_fields_property():
    ingestor, _ = _parse_and_extract()
    pk = next(
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.KEY and n[2][cs.KEY_NAME] == "PK"
    )
    assert pk[2]["fields"] == ["No."]


def test_has_field_relationships():
    ingestor, _ = _parse_and_extract()
    has_field = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_FIELD
    ]
    assert len(has_field) == 2


def test_has_key_relationships():
    ingestor, _ = _parse_and_extract()
    has_key = [r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_KEY]
    assert len(has_key) == 2


UNQUOTED_TABLE_AL = b"""
table 50102 "Mixed Names"
{
    fields
    {
        field(1; "No."; Code[20]) { }
        field(2; Name; Text[50]) { }
    }
    keys
    {
        key(PK; "No.") { Clustered = true; }
        key(K2; "No.", Name) { }
    }
}
"""


def test_unquoted_field_name_extracted():
    ingestor, _ = _parse_and_extract(UNQUOTED_TABLE_AL)
    names = {n[2][cs.KEY_NAME] for n in ingestor.nodes if n[0] == cs.NodeLabel.FIELD}
    assert names == {"No.", "Name"}


def test_key_field_list_keeps_unquoted_names():
    ingestor, _ = _parse_and_extract(UNQUOTED_TABLE_AL)
    keys = {
        n[2][cs.KEY_NAME]: n[2]["fields"]
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.KEY
    }
    assert keys["K2"] == ["No.", "Name"]
