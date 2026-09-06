from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor
from codebase_rag.parsers.al.procedure_extractor import AlProcedureExtractor

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

SAMPLE_AL = b"""
codeunit 50100 "MyCodeunit"
{
    local procedure LocalProc()
    begin
    end;

    procedure PublicProc()
    begin
    end;

    trigger OnRun()
    begin
    end;
}

table 50101 "MyTable"
{
    trigger OnInsert()
    begin
    end;

    trigger OnModify()
    begin
    end;
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


def _build_registry():
    root = _parse()
    ingestor = MockIngestor()
    obj_extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = obj_extractor.extract_objects(root, Path("/repo/test.al"), "test")
    return root, ingestor, registry


def test_procedure_nodes_created():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    proc_nodes = [
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.FUNCTION and n[1] == (cs.NodeLabel.PROCEDURE,)
    ]
    names = {n[2][cs.KEY_NAME] for n in proc_nodes}
    assert names == {"LocalProc", "PublicProc"}


def test_trigger_nodes_created():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    trigger_nodes = [
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.FUNCTION and n[1] == (cs.NodeLabel.TRIGGER,)
    ]
    names = {n[2][cs.KEY_NAME] for n in trigger_nodes}
    assert names == {"OnRun", "OnInsert", "OnModify"}


def test_trigger_has_trigger_type():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    trigger_nodes = [
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.FUNCTION and n[1] == (cs.NodeLabel.TRIGGER,)
    ]
    for tn in trigger_nodes:
        assert "trigger_type" in tn[2]
        assert tn[2]["trigger_type"] == tn[2][cs.KEY_NAME]


def test_defines_relationships():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    defines_rels = [
        r
        for r in ingestor.relationships
        if r[1] == cs.RelationshipType.DEFINES and r[2][0] == cs.NodeLabel.FUNCTION
    ]
    assert len(defines_rels) == 5


def test_has_trigger_relationships():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    trigger_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_TRIGGER
    ]
    assert len(trigger_rels) == 3
    trigger_qns = {r[2][2] for r in trigger_rels}
    assert "Codeunit.50100.MyCodeunit.OnRun" in trigger_qns
    assert "Table.50101.MyTable.OnInsert" in trigger_qns
    assert "Table.50101.MyTable.OnModify" in trigger_qns


def test_procedure_qualified_names():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_extractor.extract_procedures(registry)

    func_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.FUNCTION]
    qns = {n[2][cs.KEY_QUALIFIED_NAME] for n in func_nodes}
    assert "Codeunit.50100.MyCodeunit.LocalProc" in qns
    assert "Codeunit.50100.MyCodeunit.PublicProc" in qns
    assert "Codeunit.50100.MyCodeunit.OnRun" in qns
    assert "Table.50101.MyTable.OnInsert" in qns
    assert "Table.50101.MyTable.OnModify" in qns


def test_procedure_registry_returned():
    _root, ingestor, registry = _build_registry()
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_registry = proc_extractor.extract_procedures(registry)

    assert isinstance(proc_registry, dict)
    assert len(proc_registry) == 5
    assert (
        proc_registry["Codeunit.50100.MyCodeunit.LocalProc"]
        == "Codeunit.50100.MyCodeunit"
    )
    assert proc_registry["Table.50101.MyTable.OnInsert"] == "Table.50101.MyTable"


BODYLESS_PROCEDURES_AL = b"""
interface "My Iface"
{
    procedure Foo();
    procedure Bar(x: Integer): Boolean;
}

controladdin "My Addin"
{
    procedure Ping();
}

codeunit 50200 "Empty CU"
{
}
"""


def _procedures_for(src: bytes):
    root = _parse(src)
    ingestor = MockIngestor()
    registry = AlObjectExtractor(ingestor, Path("/repo")).extract_objects(
        root, Path("/repo/test.al"), "test"
    )
    proc_registry = AlProcedureExtractor(ingestor).extract_procedures(registry)
    return ingestor, proc_registry


def test_interface_procedures_extracted():
    _ingestor, proc_registry = _procedures_for(BODYLESS_PROCEDURES_AL)
    assert "Interface.0.My Iface.Foo" in proc_registry
    assert "Interface.0.My Iface.Bar" in proc_registry


def test_controladdin_procedures_extracted():
    _ingestor, proc_registry = _procedures_for(BODYLESS_PROCEDURES_AL)
    assert "ControlAddin.0.My Addin.Ping" in proc_registry


def test_empty_object_yields_no_procedures():
    _ingestor, proc_registry = _procedures_for(BODYLESS_PROCEDURES_AL)
    assert not [qn for qn in proc_registry if qn.startswith("Codeunit.50200")]
