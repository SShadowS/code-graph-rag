from __future__ import annotations

from pathlib import Path
from typing import TYPE_CHECKING

from .call_resolver import AlCallResolver
from .field_extractor import AlFieldExtractor
from .object_extractor import AlObjectExtractor
from .procedure_extractor import AlProcedureExtractor
from .property_reader import AlPropertyReader
from .relationship_extractor import AlRelationshipExtractor

if TYPE_CHECKING:
    from ...services import IngestorProtocol
    from ...types_defs import ASTNode


class AlParser:
    __slots__ = (
        "object_extractor",
        "field_extractor",
        "procedure_extractor",
        "property_reader",
        "relationship_extractor",
        "call_resolver",
    )

    def __init__(self, ingestor: IngestorProtocol, repo_path: Path) -> None:
        self.object_extractor = AlObjectExtractor(ingestor, repo_path)
        self.field_extractor = AlFieldExtractor(ingestor)
        self.procedure_extractor = AlProcedureExtractor(ingestor)
        self.property_reader = AlPropertyReader(ingestor)
        self.relationship_extractor = AlRelationshipExtractor(ingestor)
        self.call_resolver = AlCallResolver(ingestor)

    def process(self, root_node: ASTNode, file_path: Path, module_qn: str) -> None:
        registry = self.object_extractor.extract_objects(
            root_node, file_path, module_qn
        )
        self.field_extractor.extract_fields(registry)
        proc_registry = self.procedure_extractor.extract_procedures(registry)
        self.property_reader.read_properties(registry)
        self.relationship_extractor.extract_relationships(
            registry, root_node, module_qn
        )
        self.call_resolver.resolve_calls(registry, proc_registry)
