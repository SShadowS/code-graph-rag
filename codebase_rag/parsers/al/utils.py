from __future__ import annotations

from typing import TYPE_CHECKING

from ... import constants as cs

if TYPE_CHECKING:
    from ...types_defs import ASTNode


def extract_object_id(node: ASTNode) -> int | None:
    for child in node.children:
        if child.type == "integer":
            text = child.text.decode() if child.text else None
            if text and text.isdigit():
                return int(text)
    return None


def extract_object_name(node: ASTNode) -> str | None:
    for child in node.children:
        if child.type == "quoted_identifier":
            text = child.text.decode() if child.text else None
            if text and text.startswith('"') and text.endswith('"'):
                return text[1:-1]
            return text
        if child.type == "identifier":
            return child.text.decode() if child.text else None
    return None


def extract_extends_target(node: ASTNode) -> str | None:
    found_extends = False
    for child in node.children:
        if child.type == "extends_keyword":
            found_extends = True
            continue
        if found_extends and child.type == "quoted_identifier":
            text = child.text.decode() if child.text else None
            if text and text.startswith('"') and text.endswith('"'):
                return text[1:-1]
            return text
    return None


def extract_implements_list(node: ASTNode) -> list[str]:
    result: list[str] = []
    for child in node.children:
        if child.type == "implements_clause":
            for impl_child in child.children:
                if impl_child.type == "identifier":
                    text = impl_child.text.decode() if impl_child.text else None
                    if text:
                        result.append(text)
                elif impl_child.type == "quoted_identifier":
                    text = impl_child.text.decode() if impl_child.text else None
                    if text and text.startswith('"') and text.endswith('"'):
                        result.append(text[1:-1])
                    elif text:
                        result.append(text)
    return result


def build_al_qualified_name(
    object_type: str,
    object_id: int | None,
    object_name: str,
    child_name: str | None = None,
) -> str:
    obj_id = object_id if object_id is not None else 0
    parts = [object_type, str(obj_id), object_name]
    if child_name:
        parts.append(child_name)
    return cs.SEPARATOR_DOT.join(parts)


def object_body(node: ASTNode) -> ASTNode:
    return node.child_by_field_name(cs.FIELD_BODY) or node


def collect_descendants(node: ASTNode, type_name: str) -> list[ASTNode]:
    result: list[ASTNode] = []
    for child in node.children:
        if child.type == type_name:
            result.append(child)
        result.extend(collect_descendants(child, type_name))
    return result


def strip_quotes(text: str) -> str:
    if text.startswith('"') and text.endswith('"'):
        return text[1:-1]
    return text


def named_field_text(node: ASTNode, field_name: str) -> str | None:
    child = node.child_by_field_name(field_name)
    if child is None or not child.text:
        return None
    return strip_quotes(child.text.decode())


def named_field_node(node: ASTNode, field_name: str) -> ASTNode | None:
    return node.child_by_field_name(field_name)
