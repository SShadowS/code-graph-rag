from collections import defaultdict
from unittest.mock import MagicMock

from codebase_rag.services.graph_service import MemgraphIngestor


def _make_ingestor() -> MemgraphIngestor:
    ingestor = MemgraphIngestor.__new__(MemgraphIngestor)
    ingestor.node_buffer = []
    ingestor.batch_size = 100
    ingestor._use_merge = True
    ingestor._conn_lock = MagicMock()
    ingestor._executor = None
    ingestor.conn = None
    ingestor._rel_count = 0
    ingestor._rel_groups = defaultdict(list)
    return ingestor


def test_ensure_node_batch_without_extra_labels():
    ingestor = _make_ingestor()
    ingestor.ensure_node_batch("Class", {"qualified_name": "test"})
    assert len(ingestor.node_buffer) == 1
    label, extra, props = ingestor.node_buffer[0]
    assert label == "Class"
    assert extra is None
    assert props["qualified_name"] == "test"


def test_ensure_node_batch_with_extra_labels():
    ingestor = _make_ingestor()
    ingestor.ensure_node_batch(
        "Class", {"qualified_name": "test"}, extra_labels=("Table",)
    )
    assert len(ingestor.node_buffer) == 1
    label, extra, props = ingestor.node_buffer[0]
    assert label == "Class"
    assert extra == ("Table",)


def test_flush_nodes_groups_by_extra_labels():
    ingestor = _make_ingestor()
    ingestor.ensure_node_batch("Class", {"qualified_name": "a"})
    ingestor.ensure_node_batch(
        "Class", {"qualified_name": "b"}, extra_labels=("Table",)
    )
    ingestor.ensure_node_batch(
        "Class", {"qualified_name": "c"}, extra_labels=("Table",)
    )

    nodes_by_key: defaultdict[tuple[str, tuple[str, ...] | None], list] = defaultdict(
        list
    )
    for label, extra_labels, props in ingestor.node_buffer:
        nodes_by_key[(label, extra_labels)].append(props)

    assert len(nodes_by_key) == 2
    assert len(nodes_by_key[("Class", None)]) == 1
    assert len(nodes_by_key[("Class", ("Table",))]) == 2
