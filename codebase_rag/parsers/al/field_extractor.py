from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .object_extractor import ObjectRegistry
from .utils import collect_descendants, object_body

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode

FIELD_BEARING_TYPES = frozenset({cs.NodeLabel.TABLE, cs.NodeLabel.TABLE_EXTENSION})


def _strip_quotes(text: str) -> str:
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text


def _node_text(node: ASTNode) -> str:
    return node.text.decode() if node.text else ""


def _find_child(node: ASTNode, type_name: str) -> ASTNode | None:
    for child in node.children:
        if child.type == type_name:
            return child
    return None


def _find_children(node: ASTNode, type_name: str) -> list[ASTNode]:
    return [child for child in node.children if child.type == type_name]


class AlFieldExtractor:
    __slots__ = ("ingestor",)

    def __init__(self, ingestor: IngestorProtocol) -> None:
        self.ingestor = ingestor

    def extract_fields(self, registry: ObjectRegistry) -> None:
        for qn, (node, object_type_label, _name, _obj_id) in registry.entries.items():
            if object_type_label not in FIELD_BEARING_TYPES:
                continue
            self._extract_field_section(node, qn)
            self._extract_key_section(node, qn)

    def _extract_field_section(self, node: ASTNode, parent_qn: str) -> None:
        fields_section = _find_child(object_body(node), cs.TS_AL_FIELDS_SECTION)
        if fields_section is None:
            return

        for field_decl in collect_descendants(
            fields_section, cs.TS_AL_FIELD_DECLARATION
        ):
            self._process_field(field_decl, parent_qn)

    def _process_field(self, field_decl: ASTNode, parent_qn: str) -> None:
        integer_node = _find_child(field_decl, "integer")
        quoted_id_node = _find_child(field_decl, "quoted_identifier")
        type_spec_node = _find_child(field_decl, "type_specification")

        if quoted_id_node is None:
            return

        field_name = _strip_quotes(_node_text(quoted_id_node))
        field_id = (
            int(_node_text(integer_node))
            if integer_node and _node_text(integer_node).isdigit()
            else None
        )
        field_type = _node_text(type_spec_node) if type_spec_node else ""

        field_qn = f"{parent_qn}{cs.SEPARATOR_DOT}{field_name}"

        props: dict[str, str | int | None] = {
            cs.KEY_QUALIFIED_NAME: field_qn,
            cs.KEY_NAME: field_name,
            "field_type": field_type,
        }
        if field_id is not None:
            props["field_id"] = field_id

        self.ingestor.ensure_node_batch(cs.NodeLabel.FIELD, props)

        self.ingestor.ensure_relationship_batch(
            (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
            cs.RelationshipType.HAS_FIELD,
            (cs.NodeLabel.FIELD, cs.KEY_QUALIFIED_NAME, field_qn),
        )

        logger.debug(f"AL field: {field_qn}")

    def _extract_key_section(self, node: ASTNode, parent_qn: str) -> None:
        keys_section = _find_child(object_body(node), cs.TS_AL_KEYS_SECTION)
        if keys_section is None:
            return

        for key_decl in collect_descendants(keys_section, cs.TS_AL_KEY_DECLARATION):
            self._process_key(key_decl, parent_qn)

    def _process_key(self, key_decl: ASTNode, parent_qn: str) -> None:
        id_node = _find_child(key_decl, "identifier")
        if id_node is None:
            return

        key_name = _node_text(id_node)
        field_list_node = _find_child(key_decl, "field_list")
        fields: list[str] = []
        if field_list_node is not None:
            for qi in _find_children(field_list_node, "quoted_identifier"):
                fields.append(_strip_quotes(_node_text(qi)))

        key_qn = f"{parent_qn}{cs.SEPARATOR_DOT}{key_name}"

        props: dict[str, str | int | list[str]] = {
            cs.KEY_QUALIFIED_NAME: key_qn,
            cs.KEY_NAME: key_name,
            "fields": fields,
        }

        self.ingestor.ensure_node_batch(cs.NodeLabel.KEY, props)

        self.ingestor.ensure_relationship_batch(
            (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
            cs.RelationshipType.HAS_KEY,
            (cs.NodeLabel.KEY, cs.KEY_QUALIFIED_NAME, key_qn),
        )

        logger.debug(f"AL key: {key_qn}")
