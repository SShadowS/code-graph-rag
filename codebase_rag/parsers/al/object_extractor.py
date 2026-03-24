from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .utils import (
    build_al_qualified_name,
    extract_extends_target,
    extract_object_id,
    extract_object_name,
)

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode


OBJECT_TYPE_TO_LABELS: dict[str, tuple[str, tuple[str, ...]]] = {
    cs.TS_AL_CODEUNIT_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.CODEUNIT,),
    ),
    cs.TS_AL_TABLE_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.TABLE,),
    ),
    cs.TS_AL_TABLE_EXTENSION_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.TABLE_EXTENSION,),
    ),
    cs.TS_AL_PAGE_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.PAGE,),
    ),
    cs.TS_AL_PAGE_EXTENSION_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.PAGE_EXTENSION,),
    ),
    cs.TS_AL_REPORT_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.REPORT,),
    ),
    cs.TS_AL_REPORT_EXTENSION_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.REPORT_EXTENSION,),
    ),
    cs.TS_AL_QUERY_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.AL_QUERY,),
    ),
    cs.TS_AL_XMLPORT_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.XMLPORT,),
    ),
    cs.TS_AL_ENUM_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.ENUM,),
    ),
    cs.TS_AL_ENUM_EXTENSION_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.ENUM_EXTENSION,),
    ),
    cs.TS_AL_INTERFACE_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.INTERFACE,),
    ),
    cs.TS_AL_CONTROL_ADDIN_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.CONTROL_ADDIN,),
    ),
    cs.TS_AL_PERMISSION_SET_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.PERMISSION_SET,),
    ),
    cs.TS_AL_ENTITLEMENT_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.ENTITLEMENT,),
    ),
    cs.TS_AL_PROFILE_DECLARATION: (
        cs.NodeLabel.CLASS,
        (cs.NodeLabel.PROFILE,),
    ),
}


class ObjectRegistry:
    __slots__ = ("entries",)

    def __init__(self) -> None:
        self.entries: dict[str, tuple[ASTNode, str, str, int | None]] = {}
        # (H) entries maps qualified_name -> (node, object_type_label, object_name, object_id)

    def register(
        self,
        qn: str,
        node: ASTNode,
        type_label: str,
        name: str,
        obj_id: int | None,
    ) -> None:
        self.entries[qn] = (node, type_label, name, obj_id)


class AlObjectExtractor:
    __slots__ = ("ingestor", "repo_path")

    def __init__(self, ingestor: IngestorProtocol, repo_path: Path) -> None:
        self.ingestor = ingestor
        self.repo_path = repo_path

    def extract_objects(
        self, root_node: ASTNode, file_path: Path, module_qn: str
    ) -> ObjectRegistry:
        registry = ObjectRegistry()

        for child in root_node.children:
            if child.type not in OBJECT_TYPE_TO_LABELS:
                continue

            primary_label, extra_labels = OBJECT_TYPE_TO_LABELS[child.type]
            obj_name = extract_object_name(child)
            if not obj_name:
                continue

            obj_id = extract_object_id(child)
            object_type_str = extra_labels[0]
            qn = build_al_qualified_name(object_type_str, obj_id, obj_name)

            rel_path = file_path.relative_to(self.repo_path).as_posix()
            abs_path = file_path.resolve().as_posix()

            props = {
                cs.KEY_QUALIFIED_NAME: qn,
                cs.KEY_NAME: obj_name,
                cs.KEY_START_LINE: child.start_point[0] + 1,
                cs.KEY_END_LINE: child.end_point[0] + 1,
                cs.KEY_PATH: rel_path,
                cs.KEY_ABSOLUTE_PATH: abs_path,
            }

            if obj_id is not None:
                props["object_id"] = obj_id

            extends_target = extract_extends_target(child)
            if extends_target:
                props["extends_target"] = extends_target

            self.ingestor.ensure_node_batch(
                primary_label, props, extra_labels=extra_labels
            )

            self.ingestor.ensure_relationship_batch(
                (cs.NodeLabel.MODULE, cs.KEY_QUALIFIED_NAME, module_qn),
                cs.RelationshipType.DEFINES,
                (primary_label, cs.KEY_QUALIFIED_NAME, qn),
            )

            registry.register(qn, child, object_type_str, obj_name, obj_id)

            logger.info(f"AL object: {object_type_str} {qn}")

        return registry
