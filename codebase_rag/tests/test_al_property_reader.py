from pathlib import Path

import tree_sitter
import tree_sitter_al

from codebase_rag import constants as cs
from codebase_rag.parsers.al.object_extractor import AlObjectExtractor
from codebase_rag.parsers.al.property_reader import AlPropertyReader

LANG = tree_sitter.Language(tree_sitter_al.language())
PARSER = tree_sitter.Parser(LANG)

PAGE_AL = b"""
page 50103 "MyPage"
{
    SourceTable = "MyTable";
    layout
    {
        area(Content)
        {
            field("No."; Rec."No.") { }
        }
    }
    actions
    {
        area(Processing)
        {
            action(DoSomething) { }
        }
    }
}
"""

REPORT_AL = b"""
report 50104 "MyReport"
{
    dataset
    {
        dataitem(Customer; "Customer")
        {
            column(No; "No.") { }
        }
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


def _build_page_registry():
    root = PARSER.parse(PAGE_AL).root_node
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = extractor.extract_objects(root, Path("/repo/page.al"), "test")
    return ingestor, registry


def _build_report_registry():
    root = PARSER.parse(REPORT_AL).root_node
    ingestor = MockIngestor()
    extractor = AlObjectExtractor(ingestor, Path("/repo"))
    registry = extractor.extract_objects(root, Path("/repo/report.al"), "test")
    return ingestor, registry


def test_binds_table_relationship():
    ingestor, registry = _build_page_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    binds_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.BINDS_TABLE
    ]
    assert len(binds_rels) == 1
    rel = binds_rels[0]
    assert rel[0] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Page.50103.MyPage",
    )
    assert rel[2] == (cs.NodeLabel.CLASS, cs.KEY_NAME, "MyTable")


def test_action_nodes_created():
    ingestor, registry = _build_page_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    action_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.ACTION]
    assert len(action_nodes) == 1
    assert action_nodes[0][2][cs.KEY_QUALIFIED_NAME] == (
        "Page.50103.MyPage.DoSomething"
    )
    assert action_nodes[0][2][cs.KEY_NAME] == "DoSomething"


def test_has_action_relationship():
    ingestor, registry = _build_page_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    action_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_ACTION
    ]
    assert len(action_rels) == 1
    rel = action_rels[0]
    assert rel[0] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Page.50103.MyPage",
    )
    assert rel[2] == (
        cs.NodeLabel.ACTION,
        cs.KEY_QUALIFIED_NAME,
        "Page.50103.MyPage.DoSomething",
    )


def test_dataitem_nodes_created():
    ingestor, registry = _build_report_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    di_nodes = [n for n in ingestor.nodes if n[0] == cs.NodeLabel.DATA_ITEM]
    assert len(di_nodes) == 1
    props = di_nodes[0][2]
    assert props[cs.KEY_QUALIFIED_NAME] == "Report.50104.MyReport.Customer"
    assert props[cs.KEY_NAME] == "Customer"
    assert props["source_table"] == "Customer"


def test_has_dataitem_relationship():
    ingestor, registry = _build_report_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    di_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_DATAITEM
    ]
    assert len(di_rels) == 1
    rel = di_rels[0]
    assert rel[0] == (
        cs.NodeLabel.CLASS,
        cs.KEY_QUALIFIED_NAME,
        "Report.50104.MyReport",
    )
    assert rel[2] == (
        cs.NodeLabel.DATA_ITEM,
        cs.KEY_QUALIFIED_NAME,
        "Report.50104.MyReport.Customer",
    )


def test_reads_table_relationship():
    ingestor, registry = _build_report_registry()
    reader = AlPropertyReader(ingestor)
    reader.read_properties(registry)

    reads_rels = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.READS_TABLE
    ]
    assert len(reads_rels) == 1
    rel = reads_rels[0]
    assert rel[0] == (
        cs.NodeLabel.DATA_ITEM,
        cs.KEY_QUALIFIED_NAME,
        "Report.50104.MyReport.Customer",
    )
    assert rel[2] == (cs.NodeLabel.CLASS, cs.KEY_NAME, "Customer")


DISPLAY_PAGE_AL = b"""
page 50105 DisplayPage
{
    SourceTable = Customer;
    layout
    {
        area(Content)
        {
            repeater(Group)
            {
                field("No."; Rec."No.") { }
                field(Name; Rec.Name) { }
                field(Addr; Address) { }
                field(Calc; CalcProc()) { }
                field(Other; OtherRec.Name) { }
            }
        }
    }
}
"""

QUERY_AL = b"""
query 50106 MyQuery
{
    elements
    {
        dataitem(Cust; Customer)
        {
            column(Name; Name) { }
            dataitem(Line; "Sales Line") { }
        }
    }
}
"""


def _read(src: bytes, filename: str):
    root = PARSER.parse(src).root_node
    ingestor = MockIngestor()
    registry = AlObjectExtractor(ingestor, Path("/repo")).extract_objects(
        root, Path(f"/repo/{filename}"), "test"
    )
    AlPropertyReader(ingestor).read_properties(registry)
    return ingestor


def test_page_records_displayed_source_fields():
    ingestor = _read(DISPLAY_PAGE_AL, "display.al")
    page_batches = [
        n
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.CLASS
        and n[2][cs.KEY_QUALIFIED_NAME] == "Page.50105.DisplayPage"
        and cs.KEY_DISPLAYED_FIELDS in n[2]
    ]
    assert len(page_batches) == 1
    assert page_batches[0][1] == (cs.NodeLabel.PAGE,)
    assert page_batches[0][2][cs.KEY_DISPLAYED_FIELDS] == ["No.", "Name", "Address"]


def test_unquoted_source_table_binds():
    ingestor = _read(DISPLAY_PAGE_AL, "display.al")
    binds = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.BINDS_TABLE
    ]
    assert [r[2][2] for r in binds] == ["Customer"]


def test_query_elements_dataitems_extracted():
    ingestor = _read(QUERY_AL, "query.al")
    items = {
        n[2][cs.KEY_NAME]: n[2]
        for n in ingestor.nodes
        if n[0] == cs.NodeLabel.DATA_ITEM
    }
    assert set(items) == {"Cust", "Line"}
    assert items["Cust"]["source_table"] == "Customer"
    assert items["Line"]["source_table"] == "Sales Line"
    reads = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.READS_TABLE
    ]
    assert {r[2][2] for r in reads} == {"Customer", "Sales Line"}
    has = [
        r for r in ingestor.relationships if r[1] == cs.RelationshipType.HAS_DATAITEM
    ]
    assert {r[2][2] for r in has} == {
        "ALQuery.50106.MyQuery.Cust",
        "ALQuery.50106.MyQuery.Line",
    }
