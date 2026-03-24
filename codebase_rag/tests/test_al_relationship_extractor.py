from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor
from codebase_rag.parsers.al.relationship_extractor import AlRelationshipExtractor

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

AL_SRC = b"""
namespace MyCompany.MyApp;

using Microsoft.Sales.Customer;

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
"""

AL_STUB_SRC = b"""
tableextension 50200 "CustExt" extends "Customer"
{
}
"""


def _parse(src: bytes = AL_SRC):
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


def _build_registry(ingestor, src=AL_SRC):
    root = _parse(src)
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = extractor.extract_objects(root, Path("/repo/test.al"), "test")
    return root, registry


def test_extends_relationship_resolved():
    ingestor = MockIngestor()
    root, registry = _build_registry(ingestor)

    rel_extractor = AlRelationshipExtractor(ingestor)
    rel_extractor.extract_relationships(registry, root, "test")

    extends_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.EXTENDS
    ]
    assert len(extends_rels) == 1
    rel = extends_rels[0]
    assert rel[0] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "TableExtension.50102.MyTableExt",
    )
    assert rel[2] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Table.50101.MyTable",
    )


def test_extends_stub_created():
    ingestor = MockIngestor()
    root, registry = _build_registry(ingestor, AL_STUB_SRC)

    rel_extractor = AlRelationshipExtractor(ingestor)
    rel_extractor.extract_relationships(registry, root, "test")

    stub_nodes = [n for n in ingestor.nodes if n[2].get("is_stub") is True]
    assert len(stub_nodes) == 1
    stub = stub_nodes[0]
    assert stub[0] == cs.NodeLabel.CLASS
    assert cs.NodeLabel.EXTERNAL_OBJECT in stub[1]
    assert stub[2][cs.KEY_NAME] == "Customer"
    assert stub[2][cs.KEY_QUALIFIED_NAME] == "Table.0.Customer"


def test_extends_stub_has_correct_type():
    ingestor = MockIngestor()
    root, registry = _build_registry(ingestor, AL_STUB_SRC)

    rel_extractor = AlRelationshipExtractor(ingestor)
    rel_extractor.extract_relationships(registry, root, "test")

    stub_nodes = [n for n in ingestor.nodes if n[2].get("is_stub") is True]
    assert len(stub_nodes) == 1
    stub = stub_nodes[0]
    assert cs.NodeLabel.TABLE in stub[1]


def test_implements_relationship():
    ingestor = MockIngestor()
    root, registry = _build_registry(ingestor)

    rel_extractor = AlRelationshipExtractor(ingestor)
    rel_extractor.extract_relationships(registry, root, "test")

    impl_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.IMPLEMENTS
    ]
    assert len(impl_rels) == 1
    rel = impl_rels[0]
    assert rel[0] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Codeunit.50100.MyCodeunit",
    )
    assert rel[2] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Interface.0.IMyInterface",
    )


def test_using_creates_imports():
    ingestor = MockIngestor()
    root, registry = _build_registry(ingestor)

    rel_extractor = AlRelationshipExtractor(ingestor)
    rel_extractor.extract_relationships(registry, root, "test")

    import_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.IMPORTS
    ]
    assert len(import_rels) == 1
    rel = import_rels[0]
    assert rel[0] == (
        cs.NodeLabel.MODULE,
        cs.KEY_QUALIFIED_NAME,
        "test",
    )
    assert rel[2] == (
        cs.NodeLabel.EXTERNAL_PACKAGE,
        cs.KEY_NAME,
        "Microsoft.Sales.Customer",
    )

    # Check that ExternalPackage node was created
    ext_pkg_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.EXTERNAL_PACKAGE]
    assert len(ext_pkg_nodes) == 1
    assert ext_pkg_nodes[0][2][cs.KEY_NAME] == "Microsoft.Sales.Customer"
