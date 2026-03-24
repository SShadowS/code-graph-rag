from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.parser import AlParser

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

FULL_AL = b"""
namespace MyCompany.MyApp;

using Microsoft.Sales.Customer;

codeunit 50100 "MyCodeunit" implements IMyInterface
{
    procedure CallerProc()
    begin
        TargetProc();
    end;

    procedure TargetProc()
    begin
    end;

    trigger OnRun()
    begin
    end;
}

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
    }
}

tableextension 50102 "MyTableExt" extends "MyTable"
{
    fields
    {
        field(50100; "CustomField"; Text[50]) { }
    }
}

page 50103 "MyPage"
{
    SourceTable = "MyTable";
    actions
    {
        area(Processing)
        {
            action(DoSomething) { }
        }
    }
}

enum 50104 "MyEnum"
{
}

interface "IMyInterface"
{
    procedure DoSomething();
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


def test_full_pipeline():
    root = PARSER.parse(FULL_AL).root_node
    ingestor = MockIngestor()
    parser = AlParser(ingestor, Path("/repo"))
    parser.process(root, Path("/repo/test.al"), "test")

    object_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.CLASS]
    assert len(object_nodes) >= 6

    field_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.FIELD]
    assert len(field_nodes) >= 2

    func_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.FUNCTION]
    assert len(func_nodes) >= 3

    action_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.ACTION]
    assert len(action_nodes) >= 1


def test_relationship_types_present():
    root = PARSER.parse(FULL_AL).root_node
    ingestor = MockIngestor()
    parser = AlParser(ingestor, Path("/repo"))
    parser.process(root, Path("/repo/test.al"), "test")

    rel_types = {r[1] for r in ingestor.relationships}

    assert cs.RelationshipType.DEFINES in rel_types
    assert cs.RelationshipType.HAS_FIELD in rel_types
    assert cs.RelationshipType.HAS_KEY in rel_types
    assert cs.RelationshipType.EXTENDS in rel_types
    assert cs.RelationshipType.IMPLEMENTS in rel_types
    assert cs.RelationshipType.BINDS_TABLE in rel_types
    assert cs.RelationshipType.HAS_ACTION in rel_types
    assert cs.RelationshipType.CALLS in rel_types
    assert cs.RelationshipType.IMPORTS in rel_types


def test_extends_relationship():
    root = PARSER.parse(FULL_AL).root_node
    ingestor = MockIngestor()
    parser = AlParser(ingestor, Path("/repo"))
    parser.process(root, Path("/repo/test.al"), "test")

    extends = [r for r in ingestor.relationships if r[1] == cs.RelationshipType.EXTENDS]
    assert len(extends) == 1
    assert "MyTableExt" in extends[0][0][2]
    assert "MyTable" in extends[0][2][2]
