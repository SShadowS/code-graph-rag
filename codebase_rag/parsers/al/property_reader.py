from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .object_extractor import ObjectRegistry
from .utils import (
    collect_descendants,
    named_field_node,
    named_field_text,
    object_body,
)

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode, PropertyDict

PAGE_TYPES = frozenset({cs.NodeLabel.PAGE, cs.NodeLabel.PAGE_EXTENSION})
REPORT_TYPES = frozenset({cs.NodeLabel.REPORT, cs.NodeLabel.REPORT_EXTENSION})
DATAITEM_BEARING_TYPES = frozenset(
    {cs.NodeLabel.REPORT, cs.NodeLabel.REPORT_EXTENSION, cs.NodeLabel.AL_QUERY}
)


def _node_text(node: ASTNode) -> str:
    return node.text.decode() if node.text else ""


def _strip_quotes(text: str) -> str:
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text


def _find_child(node: ASTNode, type_name: str) -> ASTNode | None:
    for child in node.children:
        if child.type == type_name:
            return child
    return None


def _extract_source_table(node: ASTNode) -> str | None:
    for child in object_body(node).children:
        if child.type != cs.TS_AL_PROPERTY:
            continue
        prop_name_node = _find_child(child, "property_name")
        if prop_name_node is None:
            continue
        if _node_text(prop_name_node) != "SourceTable":
            continue
        qi = _find_child(child, "quoted_identifier")
        if qi is not None:
            return _strip_quotes(_node_text(qi))
        ident = _find_child(child, "identifier")
        if ident is not None:
            return _node_text(ident)
    return None


def _displayed_source_fields(layout_section: ASTNode) -> list[str]:
    displayed: list[str] = []
    for page_field in collect_descendants(layout_section, cs.TS_AL_PAGE_FIELD):
        source = named_field_node(page_field, cs.AL_FIELD_SOURCE)
        if source is None:
            continue
        if source.type in (cs.TS_AL_IDENTIFIER, cs.TS_AL_QUOTED_IDENTIFIER):
            displayed.append(_strip_quotes(_node_text(source)))
        elif source.type == cs.TS_AL_MEMBER_EXPRESSION:
            owner = named_field_text(source, cs.FIELD_OBJECT)
            member = named_field_text(source, cs.AL_FIELD_MEMBER)
            if owner and member and owner.lower() == cs.AL_PAGE_RECORD_VARIABLE:
                displayed.append(member)
    return displayed


class AlPropertyReader:
    __slots__ = ("ingestor",)

    def __init__(self, ingestor: IngestorProtocol) -> None:
        self.ingestor = ingestor

    def read_properties(self, registry: ObjectRegistry) -> None:
        for parent_qn, (
            node,
            object_type_label,
            _object_name,
            _object_id,
        ) in registry.entries.items():
            if object_type_label in PAGE_TYPES:
                self._process_page(node, parent_qn, object_type_label)
            if object_type_label in DATAITEM_BEARING_TYPES:
                self._process_dataitems(node, parent_qn)

    def _process_page(
        self, node: ASTNode, parent_qn: str, object_type_label: str
    ) -> None:
        source_table = _extract_source_table(node)
        if source_table:
            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
                cs.RelationshipType.BINDS_TABLE,
                (cs.NodeLabel.TABLE, cs.KEY_NAME, source_table),
            )
            logger.debug(f"AL BINDS_TABLE: {parent_qn} -> {source_table}")

        layout_section = _find_child(object_body(node), cs.TS_AL_LAYOUT_SECTION)
        if layout_section:
            displayed = _displayed_source_fields(layout_section)
            if displayed:
                self.ingestor.ensure_node_batch(
                    cs.NodeLabel.CLASS,
                    {
                        cs.KEY_QUALIFIED_NAME: parent_qn,
                        cs.KEY_DISPLAYED_FIELDS: displayed,
                    },
                    extra_labels=(object_type_label,),
                )
                logger.debug(f"AL page fields: {parent_qn} displays {displayed}")

        actions_section = _find_child(object_body(node), cs.TS_AL_ACTIONS_SECTION)
        if actions_section:
            action_nodes = collect_descendants(
                actions_section, cs.TS_AL_ACTION_DECLARATION
            )
            for action_node in action_nodes:
                self._process_action(action_node, parent_qn)

    def _process_action(self, action_node: ASTNode, parent_qn: str) -> None:
        ident = _find_child(action_node, "identifier")
        if ident is None:
            return
        action_name = _node_text(ident)
        action_qn = f"{parent_qn}{cs.SEPARATOR_DOT}{action_name}"

        self.ingestor.ensure_node_batch(
            cs.NodeLabel.ACTION,
            {
                cs.KEY_QUALIFIED_NAME: action_qn,
                cs.KEY_NAME: action_name,
                cs.KEY_START_LINE: action_node.start_point[0] + 1,
                cs.KEY_END_LINE: action_node.end_point[0] + 1,
            },
        )

        self.ingestor.ensure_relationship_batch(
            (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
            cs.RelationshipType.HAS_ACTION,
            (cs.NodeLabel.ACTION, cs.KEY_QUALIFIED_NAME, action_qn),
        )

        logger.debug(f"AL action: {action_qn}")

    def _process_dataitems(self, node: ASTNode, parent_qn: str) -> None:
        body = object_body(node)
        sections = [
            section
            for section_type in (cs.TS_AL_DATASET_SECTION, cs.TS_AL_ELEMENTS_SECTION)
            if (section := _find_child(body, section_type)) is not None
        ]
        dataitem_types = (cs.TS_AL_REPORT_DATAITEM, cs.TS_AL_QUERY_DATAITEM)
        for section in sections:
            for dt in dataitem_types:
                for di_node in collect_descendants(section, dt):
                    self._process_dataitem(di_node, parent_qn)

    def _process_dataitem(self, di_node: ASTNode, parent_qn: str) -> None:
        dataitem_name = named_field_text(di_node, cs.FIELD_NAME)
        if dataitem_name is None:
            return
        source_table = named_field_text(di_node, cs.AL_FIELD_TABLE_NAME) or ""

        dataitem_qn = f"{parent_qn}{cs.SEPARATOR_DOT}{dataitem_name}"

        props: PropertyDict = {
            cs.KEY_QUALIFIED_NAME: dataitem_qn,
            cs.KEY_NAME: dataitem_name,
            cs.KEY_START_LINE: di_node.start_point[0] + 1,
            cs.KEY_END_LINE: di_node.end_point[0] + 1,
        }
        if source_table:
            props["source_table"] = source_table

        self.ingestor.ensure_node_batch(cs.NodeLabel.DATA_ITEM, props)

        self.ingestor.ensure_relationship_batch(
            (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
            cs.RelationshipType.HAS_DATAITEM,
            (cs.NodeLabel.DATA_ITEM, cs.KEY_QUALIFIED_NAME, dataitem_qn),
        )

        if source_table:
            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.DATA_ITEM, cs.KEY_QUALIFIED_NAME, dataitem_qn),
                cs.RelationshipType.READS_TABLE,
                (cs.NodeLabel.TABLE, cs.KEY_NAME, source_table),
            )

        logger.debug(f"AL dataitem: {dataitem_qn}")
