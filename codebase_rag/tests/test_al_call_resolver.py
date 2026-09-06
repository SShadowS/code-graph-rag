from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.call_resolver import AlCallResolver
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor
from codebase_rag.parsers.al.procedure_extractor import AlProcedureExtractor

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

AL_CALLS = b"""
codeunit 50100 "MyCU"
{
    procedure CallerProc()
    begin
        TargetProc();
    end;

    procedure TargetProc()
    begin
    end;
}
"""

AL_UNRESOLVED = b"""
codeunit 50200 "OtherCU"
{
    procedure DoStuff()
    begin
        Message('hello');
        UnknownFunc();
    end;
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


def _setup(src: bytes):
    root = PARSER.parse(src).root_node
    ingestor = MockIngestor()
    obj_extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = obj_extractor.extract_objects(root, Path("/repo/test.al"), "test")
    proc_extractor = AlProcedureExtractor(ingestor)
    proc_registry = proc_extractor.extract_procedures(registry)
    return ingestor, registry, proc_registry


def test_direct_call_within_object():
    ingestor, registry, proc_registry = _setup(AL_CALLS)
    resolver = AlCallResolver(ingestor)
    resolver.resolve_calls(registry, proc_registry)

    calls_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.CALLS
    ]
    assert len(calls_rels) == 1
    rel = calls_rels[0]
    assert rel[0][2] == "Codeunit.50100.MyCU.CallerProc"
    assert rel[2][2] == "Codeunit.50100.MyCU.TargetProc"


def test_call_relationship_created():
    ingestor, registry, proc_registry = _setup(AL_CALLS)
    resolver = AlCallResolver(ingestor)
    resolver.resolve_calls(registry, proc_registry)

    calls_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.CALLS
    ]
    assert len(calls_rels) == 1
    from_spec = calls_rels[0][0]
    to_spec = calls_rels[0][2]
    assert from_spec[0] == cs.NodeLabel.FUNCTION
    assert from_spec[1] == cs.KEY_QUALIFIED_NAME
    assert to_spec[0] == cs.NodeLabel.FUNCTION
    assert to_spec[1] == cs.KEY_QUALIFIED_NAME


def test_unresolved_calls_ignored():
    ingestor, registry, proc_registry = _setup(AL_UNRESOLVED)
    resolver = AlCallResolver(ingestor)
    resolver.resolve_calls(registry, proc_registry)

    calls_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.CALLS
    ]
    assert len(calls_rels) == 0


AL_MEMBER_CALL = b"""
table 50300 "Customer"
{
    fields { field(1; "No."; Code[20]) { } }

    procedure Bar()
    begin
    end;
}

codeunit 50301 "MemberCU"
{
    procedure UseIt()
    var
        Cust: Record "Customer";
    begin
        Cust.Bar();
    end;
}
"""


def test_member_call_resolved_through_record_variable():
    ingestor, registry, proc_registry = _setup(AL_MEMBER_CALL)
    resolver = AlCallResolver(ingestor)
    resolver.resolve_calls(registry, proc_registry)

    calls_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.CALLS
    ]
    assert len(calls_rels) == 1
    assert calls_rels[0][0][2] == "Codeunit.50301.MemberCU.UseIt"
    assert calls_rels[0][2][2] == "Table.50300.Customer.Bar"


AL_MEMBER_CALL_UNQUOTED = b"""
table 50302 Customer
{
    fields { field(1; "No."; Code[20]) { } }

    procedure Bar()
    begin
    end;
}

codeunit 50303 "MemberCU2"
{
    procedure UseIt()
    var
        Cust: Record Customer;
    begin
        Cust.Bar();
    end;
}
"""


def test_member_call_resolved_through_unquoted_record_type():
    ingestor, registry, proc_registry = _setup(AL_MEMBER_CALL_UNQUOTED)
    resolver = AlCallResolver(ingestor)
    resolver.resolve_calls(registry, proc_registry)

    calls_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.CALLS
    ]
    assert len(calls_rels) == 1
    assert calls_rels[0][2][2] == "Table.50302.Customer.Bar"
