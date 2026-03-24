from __future__ import annotations

from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .object_extractor import ObjectRegistry
from .utils import (
    build_al_qualified_name,
    extract_extends_target,
    extract_implements_list,
)

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode

EXTENSION_TO_BASE_TYPE: dict[str, str] = {
    cs.NodeLabel.TABLE_EXTENSION: cs.NodeLabel.TABLE,
    cs.NodeLabel.PAGE_EXTENSION: cs.NodeLabel.PAGE,
    cs.NodeLabel.REPORT_EXTENSION: cs.NodeLabel.REPORT,
    cs.NodeLabel.ENUM_EXTENSION: cs.NodeLabel.ENUM,
}


class AlRelationshipExtractor:
    __slots__ = ("ingestor",)

    def __init__(self, ingestor: IngestorProtocol) -> None:
        self.ingestor = ingestor

    def extract_relationships(
        self, registry: ObjectRegistry, root_node: ASTNode, module_qn: str
    ) -> None:
        self._extract_extends(registry)
        self._extract_implements(registry)
        self._extract_using_imports(root_node, module_qn)

    def _extract_extends(self, registry: ObjectRegistry) -> None:
        for qn, (node, type_label, _name, _obj_id) in registry.entries.items():
            extends_target = extract_extends_target(node)
            if not extends_target:
                continue

            base_qn = self._find_object_by_name(registry, extends_target)
            if base_qn is None:
                base_type = EXTENSION_TO_BASE_TYPE.get(type_label, type_label)
                base_qn = build_al_qualified_name(base_type, 0, extends_target)
                self.ingestor.ensure_node_batch(
                    cs.NodeLabel.CLASS,
                    {
                        cs.KEY_QUALIFIED_NAME: base_qn,
                        cs.KEY_NAME: extends_target,
                        "is_stub": True,
                    },
                    extra_labels=(base_type, cs.NodeLabel.EXTERNAL_OBJECT),
                )
                logger.info(f"AL stub node: {base_type} {base_qn}")

            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, qn),
                cs.RelationshipType.EXTENDS,
                (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, base_qn),
            )
            logger.info(f"AL EXTENDS: {qn} -> {base_qn}")

    def _extract_implements(self, registry: ObjectRegistry) -> None:
        for qn, (node, _type_label, _name, _obj_id) in registry.entries.items():
            iface_names = extract_implements_list(node)
            for iface_name in iface_names:
                iface_qn = self._find_object_by_name(registry, iface_name)
                if iface_qn is None:
                    iface_qn = build_al_qualified_name(
                        cs.NodeLabel.INTERFACE, 0, iface_name
                    )
                    self.ingestor.ensure_node_batch(
                        cs.NodeLabel.CLASS,
                        {
                            cs.KEY_QUALIFIED_NAME: iface_qn,
                            cs.KEY_NAME: iface_name,
                            "is_stub": True,
                        },
                        extra_labels=(
                            cs.NodeLabel.INTERFACE,
                            cs.NodeLabel.EXTERNAL_OBJECT,
                        ),
                    )
                    logger.info(f"AL stub interface: {iface_qn}")

                self.ingestor.ensure_relationship_batch(
                    (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, qn),
                    cs.RelationshipType.IMPLEMENTS,
                    (cs.NodeLabel.CLASS, cs.KEY_QUALIFIED_NAME, iface_qn),
                )
                logger.info(f"AL IMPLEMENTS: {qn} -> {iface_qn}")

    def _extract_using_imports(
        self, root_node: ASTNode, module_qn: str
    ) -> None:
        for child in root_node.children:
            if child.type != "using_statement":
                continue

            ns_name: str | None = None
            for sub in child.children:
                if sub.type == "namespace_name":
                    ns_name = sub.text.decode() if sub.text else None
                    break

            if not ns_name:
                continue

            self.ingestor.ensure_node_batch(
                cs.NodeLabel.EXTERNAL_PACKAGE,
                {cs.KEY_NAME: ns_name},
            )

            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.MODULE, cs.KEY_QUALIFIED_NAME, module_qn),
                cs.RelationshipType.IMPORTS,
                (cs.NodeLabel.EXTERNAL_PACKAGE, cs.KEY_NAME, ns_name),
            )
            logger.info(f"AL IMPORTS: {module_qn} -> {ns_name}")

    @staticmethod
    def _find_object_by_name(
        registry: ObjectRegistry, name: str
    ) -> str | None:
        for qn, (_node, _type_label, obj_name, _obj_id) in registry.entries.items():
            if obj_name == name:
                return qn
        return None
