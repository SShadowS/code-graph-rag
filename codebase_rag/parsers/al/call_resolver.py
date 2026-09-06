from __future__ import annotations

from collections import defaultdict
from typing import TYPE_CHECKING

from loguru import logger

from ... import constants as cs
from .object_extractor import ObjectRegistry
from .procedure_extractor import PROCEDURE_NODE_TYPES
from .utils import collect_descendants, object_body

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode


def _node_text(node: ASTNode) -> str:
    return node.text.decode() if node.text else ""


def _find_call_expressions(node: ASTNode) -> list[ASTNode]:
    results: list[ASTNode] = []
    for child in node.children:
        if child.type == cs.TS_AL_CALL_EXPRESSION:
            results.append(child)
        results.extend(_find_call_expressions(child))
    return results


def _extract_var_types(proc_node: ASTNode) -> dict[str, str]:
    var_types: dict[str, str] = {}
    for child in proc_node.children:
        if child.type == cs.TS_AL_VAR_SECTION:
            for var_decl in collect_descendants(child, cs.TS_AL_VARIABLE_DECLARATION):
                if var_decl.type == cs.TS_AL_VARIABLE_DECLARATION:
                    var_name: str | None = None
                    table_name: str | None = None
                    for vc in var_decl.children:
                        if vc.type == "identifier" and var_name is None:
                            var_name = _node_text(vc) or None
                        if vc.type == "type_specification":
                            for ts in vc.children:
                                if ts.type == "record_type":
                                    for rt in ts.children:
                                        if rt.type == "quoted_identifier":
                                            text = _node_text(rt)
                                            if text.startswith('"') and text.endswith(
                                                '"'
                                            ):
                                                table_name = text[1:-1]
                    if var_name and table_name:
                        var_types[var_name] = table_name
    return var_types


def _extract_proc_name(proc_node: ASTNode) -> str | None:
    for child in proc_node.children:
        if child.type == "quoted_identifier":
            text = _node_text(child)
            if text.startswith('"') and text.endswith('"'):
                return text[1:-1]
            return text
        if child.type == "identifier":
            return _node_text(child)
    return None


class AlCallResolver:
    __slots__ = ("ingestor",)

    def __init__(self, ingestor: IngestorProtocol) -> None:
        self.ingestor = ingestor

    def resolve_calls(
        self,
        registry: ObjectRegistry,
        procedure_registry: dict[str, str],
    ) -> None:
        parent_to_procs: dict[str, list[str]] = defaultdict(list)
        for proc_qn, parent_qn in procedure_registry.items():
            parent_to_procs[parent_qn].append(proc_qn)

        for parent_qn, (
            node,
            object_type_label,
            object_name,
            object_id,
        ) in registry.entries.items():
            sibling_procs = parent_to_procs.get(parent_qn, [])
            self._process_object(
                node,
                parent_qn,
                sibling_procs,
                procedure_registry,
            )

    def _process_object(
        self,
        node: ASTNode,
        parent_qn: str,
        sibling_procs: list[str],
        procedure_registry: dict[str, str],
    ) -> None:
        for child in object_body(node).children:
            if child.type not in PROCEDURE_NODE_TYPES:
                continue

            proc_name = _extract_proc_name(child)
            if not proc_name:
                continue

            caller_qn = f"{parent_qn}.{proc_name}"
            if caller_qn not in procedure_registry:
                continue

            var_types = _extract_var_types(child)
            code_block = None
            for cc in child.children:
                if cc.type == "code_block":
                    code_block = cc
                    break

            if code_block is None:
                continue

            call_exprs = _find_call_expressions(code_block)
            for call_expr in call_exprs:
                self._resolve_call(
                    call_expr,
                    caller_qn,
                    parent_qn,
                    sibling_procs,
                    var_types,
                    procedure_registry,
                )

    def _resolve_call(
        self,
        call_expr: ASTNode,
        caller_qn: str,
        parent_qn: str,
        sibling_procs: list[str],
        var_types: dict[str, str],
        procedure_registry: dict[str, str],
    ) -> None:
        first_named = None
        for ch in call_expr.children:
            if ch.is_named:
                first_named = ch
                break

        if first_named is None:
            return

        if first_named.type == "identifier":
            self._resolve_direct_call(
                _node_text(first_named),
                caller_qn,
                parent_qn,
                sibling_procs,
            )
        elif first_named.type == cs.TS_AL_MEMBER_EXPRESSION:
            self._resolve_member_call(
                first_named,
                caller_qn,
                var_types,
                procedure_registry,
            )

    def _resolve_direct_call(
        self,
        func_name: str,
        caller_qn: str,
        parent_qn: str,
        sibling_procs: list[str],
    ) -> None:
        target_qn = f"{parent_qn}.{func_name}"
        if target_qn in sibling_procs:
            self._create_calls_relationship(caller_qn, target_qn)

    def _resolve_member_call(
        self,
        member_node: ASTNode,
        caller_qn: str,
        var_types: dict[str, str],
        procedure_registry: dict[str, str],
    ) -> None:
        identifiers: list[str] = []
        for ch in member_node.children:
            if ch.type == "identifier":
                identifiers.append(_node_text(ch))

        if len(identifiers) < 2:
            return

        obj_name = identifiers[0]
        method_name = identifiers[1]

        table_name = var_types.get(obj_name)
        if table_name is None:
            logger.debug(
                f"Cannot resolve variable '{obj_name}' in call {obj_name}.{method_name}"
            )
            return

        for proc_qn, proc_parent in procedure_registry.items():
            if proc_qn.endswith(f".{method_name}") and table_name in proc_parent:
                self._create_calls_relationship(caller_qn, proc_qn)
                return

        logger.debug(f"Cannot resolve method '{method_name}' on '{table_name}'")

    def _create_calls_relationship(self, caller_qn: str, target_qn: str) -> None:
        self.ingestor.ensure_relationship_batch(
            (cs.NodeLabel.FUNCTION, cs.KEY_QUALIFIED_NAME, caller_qn),
            cs.RelationshipType.CALLS,
            (cs.NodeLabel.FUNCTION, cs.KEY_QUALIFIED_NAME, target_qn),
        )
        logger.debug(f"AL CALLS: {caller_qn} -> {target_qn}")
