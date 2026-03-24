from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor
from codebase_rag.parsers.al.utils import (
    build_al_qualified_name,
    extract_extends_target,
    extract_implements_list,
    extract_object_id,
    extract_object_name,
)

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

SAMPLE_AL = b"""
codeunit 50100 "MyCodeunit" implements IMyInterface
{
}

table 50101 "MyTable"
{
}

tableextension 50102 "MyTableExt" extends "MyTable"
{
}

interface "IMyInterface"
{
}

enum 50104 "MyEnum"
{
}
"""


def _parse(src: bytes = SAMPLE_AL):
    return PARSER.parse(src).root_node


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


def test_extract_object_id():
    root = _parse()
    cu = [c for c in root.children if c.type == cs.TS_AL_CODEUNIT_DECLARATION][0]
    assert extract_object_id(cu) == 50100


def test_extract_object_name():
    root = _parse()
    cu = [c for c in root.children if c.type == cs.TS_AL_CODEUNIT_DECLARATION][0]
    assert extract_object_name(cu) == "MyCodeunit"


def test_extract_extends_target():
    root = _parse()
    te = [c for c in root.children if c.type == cs.TS_AL_TABLE_EXTENSION_DECLARATION][0]
    assert extract_extends_target(te) == "MyTable"


def test_extract_extends_target_none_for_base():
    root = _parse()
    tbl = [c for c in root.children if c.type == cs.TS_AL_TABLE_DECLARATION][0]
    assert extract_extends_target(tbl) is None


def test_extract_implements_list():
    root = _parse()
    cu = [c for c in root.children if c.type == cs.TS_AL_CODEUNIT_DECLARATION][0]
    assert extract_implements_list(cu) == ["IMyInterface"]


def test_build_al_qualified_name():
    assert (
        build_al_qualified_name("Codeunit", 50100, "MyCodeunit")
        == "Codeunit.50100.MyCodeunit"
    )
    assert (
        build_al_qualified_name("Interface", None, "IMyInterface")
        == "Interface.0.IMyInterface"
    )
    assert (
        build_al_qualified_name("Codeunit", 50100, "MyCodeunit", "MyProcedure")
        == "Codeunit.50100.MyCodeunit.MyProcedure"
    )


def test_object_extractor_finds_all_objects():
    root = _parse()
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = extractor.extract_objects(root, Path("/repo/test.al"), "test")

    assert len(ingestor.nodes) == 5
    assert len(registry.entries) == 5


def test_object_extractor_codeunit_labels():
    root = _parse()
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    extractor.extract_objects(root, Path("/repo/test.al"), "test")

    cu_node = next(n for n in ingestor.nodes if n[2].get(cs.KEY_NAME) == "MyCodeunit")
    assert cu_node[0] == cs.NodeLabel.CLASS
    assert cu_node[1] == (cs.NodeLabel.CODEUNIT,)
    assert cu_node[2][cs.KEY_QUALIFIED_NAME] == "Codeunit.50100.MyCodeunit"
    assert cu_node[2]["object_id"] == 50100


def test_object_extractor_table_extension():
    root = _parse()
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    extractor.extract_objects(root, Path("/repo/test.al"), "test")

    te_node = next(n for n in ingestor.nodes if n[2].get(cs.KEY_NAME) == "MyTableExt")
    assert te_node[0] == cs.NodeLabel.CLASS
    assert te_node[1] == (cs.NodeLabel.TABLE_EXTENSION,)
    assert te_node[2]["extends_target"] == "MyTable"


def test_object_extractor_interface_no_id():
    root = _parse()
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    extractor.extract_objects(root, Path("/repo/test.al"), "test")

    iface_node = next(
        n for n in ingestor.nodes if n[2].get(cs.KEY_NAME) == "IMyInterface"
    )
    assert iface_node[2][cs.KEY_QUALIFIED_NAME] == "Interface.0.IMyInterface"
    assert "object_id" not in iface_node[2]


def test_object_extractor_defines_relationships():
    root = _parse()
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    extractor.extract_objects(root, Path("/repo/test.al"), "test")

    defines_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.DEFINES
    ]
    assert len(defines_rels) == 5
    for rel in defines_rels:
        assert rel[0][0] == cs.NodeLabel.MODULE
