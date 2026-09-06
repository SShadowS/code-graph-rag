from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .object_extractor import ObjectRegistry
from .utils import build_al_qualified_name, object_body

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode

PROCEDURE_NODE_TYPES = frozenset(
    {
        cs.TS_AL_PROCEDURE,
        cs.TS_AL_TRIGGER_DECLARATION,
        cs.TS_AL_EVENT_DECLARATION,
        cs.TS_AL_INTERFACE_PROCEDURE,
    }
)

ACCESS_MODIFIER_MAP: dict[str, str] = {
    "local_keyword": "local",
    "internal_keyword": "internal",
    "protected_keyword": "protected",
}


def _node_text(node: ASTNode) -> str:
    return node.text.decode() if node.text else ""


def _find_child(node: ASTNode, type_name: str) -> ASTNode | None:
    for child in node.children:
        if child.type == type_name:
            return child
    return None


def _extract_name(node: ASTNode) -> str | None:
    for child in node.children:
        if child.type == "quoted_identifier":
            text = _node_text(child)
            if text.startswith('"') and text.endswith('"'):
                return text[1:-1]
            return text
        if child.type == "identifier":
            return _node_text(child)
    return None


def _extract_access_modifier(node: ASTNode) -> str | None:
    modifier_node = _find_child(node, "procedure_modifier")
    if modifier_node is None:
        return None
    for child in modifier_node.children:
        if child.type in ACCESS_MODIFIER_MAP:
            return ACCESS_MODIFIER_MAP[child.type]
    return None


def _is_event_subscriber(siblings: list[ASTNode], proc_index: int) -> bool:
    # (H) Check if previous sibling is an attribute_item with EventSubscriber
    if proc_index <= 0:
        return False
    prev_sibling = siblings[proc_index - 1]
    if prev_sibling.type != cs.TS_AL_ATTRIBUTE_ITEM:
        return False
    content = _find_child(prev_sibling, "attribute_content")
    if content is None:
        return False
    ident = _find_child(content, "identifier")
    if ident is None:
        return False
    return _node_text(ident) == "EventSubscriber"


class AlProcedureExtractor:
    __slots__ = ("ingestor",)

    def __init__(self, ingestor: IngestorProtocol) -> None:
        self.ingestor = ingestor

    def extract_procedures(self, registry: ObjectRegistry) -> dict[str, str]:
        proc_registry: dict[str, str] = {}

        for parent_qn, (
            node,
            object_type_label,
            object_name,
            object_id,
        ) in registry.entries.items():
            self._walk_object(
                node,
                parent_qn,
                object_type_label,
                object_name,
                object_id,
                proc_registry,
            )

        return proc_registry

    def _walk_object(
        self,
        node: ASTNode,
        parent_qn: str,
        object_type_label: str,
        object_name: str,
        object_id: int | None,
        proc_registry: dict[str, str],
    ) -> None:
        children = object_body(node).children
        for idx, child in enumerate(children):
            if child.type not in PROCEDURE_NODE_TYPES:
                continue

            name = _extract_name(child)
            if not name:
                continue

            qn = build_al_qualified_name(
                object_type_label, object_id, object_name, name
            )

            props: dict[str, str | int | None] = {
                cs.KEY_QUALIFIED_NAME: qn,
                cs.KEY_NAME: name,
                cs.KEY_START_LINE: child.start_point[0] + 1,
                cs.KEY_END_LINE: child.end_point[0] + 1,
                cs.KEY_PATH: "",
                cs.KEY_ABSOLUTE_PATH: "",
            }

            if child.type == cs.TS_AL_TRIGGER_DECLARATION:
                extra_labels: tuple[str, ...] = (cs.NodeLabel.TRIGGER,)
                props["trigger_type"] = name
            elif child.type == cs.TS_AL_EVENT_DECLARATION:
                extra_labels = (cs.NodeLabel.TRIGGER,)
                props["trigger_type"] = name
            elif _is_event_subscriber(children, idx):
                extra_labels = (cs.NodeLabel.EVENT_SUBSCRIBER,)
            else:
                extra_labels = (cs.NodeLabel.PROCEDURE,)

            access = _extract_access_modifier(child)
            if access:
                props["access_modifier"] = access

            self.ingestor.ensure_node_batch(
                cs.NodeLabel.FUNCTION,
                props,
                extra_labels=extra_labels,
            )

            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, parent_qn),
                cs.RelationshipType.DEFINES,
                (cs.NodeLabel.FUNCTION, cs.KEY_QUALIFIED_NAME, qn),
            )

            if child.type in (
                cs.TS_AL_TRIGGER_DECLARATION,
                cs.TS_AL_EVENT_DECLARATION,
            ):
                self.ingestor.ensure_relationship_batch(
                    (
                        cs.NodeLabel.CLASS,
                        cs.KEY_QUALIFIED_NAME,
                        parent_qn,
                    ),
                    cs.RelationshipType.HAS_TRIGGER,
                    (cs.NodeLabel.FUNCTION, cs.KEY_QUALIFIED_NAME, qn),
                )

            proc_registry[qn] = parent_qn
            logger.debug(f"AL procedure: {qn}")
