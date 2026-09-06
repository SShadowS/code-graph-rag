from google.protobuf import struct_pb2 as _struct_pb2
from google.protobuf.internal import containers as _containers
from google.protobuf.internal import enum_type_wrapper as _enum_type_wrapper
from google.protobuf import descriptor as _descriptor
from google.protobuf import message as _message
from collections.abc import Iterable as _Iterable, Mapping as _Mapping
from typing import ClassVar as _ClassVar, Optional as _Optional, Union as _Union

DESCRIPTOR: _descriptor.FileDescriptor

class GraphCodeIndex(_message.Message):
    __slots__ = ("nodes", "relationships")
    NODES_FIELD_NUMBER: _ClassVar[int]
    RELATIONSHIPS_FIELD_NUMBER: _ClassVar[int]
    nodes: _containers.RepeatedCompositeFieldContainer[Node]
    relationships: _containers.RepeatedCompositeFieldContainer[Relationship]
    def __init__(self, nodes: _Optional[_Iterable[_Union[Node, _Mapping]]] = ..., relationships: _Optional[_Iterable[_Union[Relationship, _Mapping]]] = ...) -> None: ...

class Node(_message.Message):
    __slots__ = ("project", "package", "folder", "module", "class_node", "function", "method", "file", "external_package", "module_implementation", "module_interface", "interface_node", "enum_node", "type_node", "union_node", "external_module", "resource", "section", "pattern", "code_smell", "security_issue", "field", "key", "action", "data_item", "table", "table_extension", "page", "page_extension", "codeunit", "report", "report_extension", "enum_extension", "al_query", "xmlport", "control_addin", "permission_set", "entitlement", "profile", "procedure", "trigger", "event_subscriber", "external_object")
    PROJECT_FIELD_NUMBER: _ClassVar[int]
    PACKAGE_FIELD_NUMBER: _ClassVar[int]
    FOLDER_FIELD_NUMBER: _ClassVar[int]
    MODULE_FIELD_NUMBER: _ClassVar[int]
    CLASS_NODE_FIELD_NUMBER: _ClassVar[int]
    FUNCTION_FIELD_NUMBER: _ClassVar[int]
    METHOD_FIELD_NUMBER: _ClassVar[int]
    FILE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_PACKAGE_FIELD_NUMBER: _ClassVar[int]
    MODULE_IMPLEMENTATION_FIELD_NUMBER: _ClassVar[int]
    MODULE_INTERFACE_FIELD_NUMBER: _ClassVar[int]
    INTERFACE_NODE_FIELD_NUMBER: _ClassVar[int]
    ENUM_NODE_FIELD_NUMBER: _ClassVar[int]
    TYPE_NODE_FIELD_NUMBER: _ClassVar[int]
    UNION_NODE_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_MODULE_FIELD_NUMBER: _ClassVar[int]
    RESOURCE_FIELD_NUMBER: _ClassVar[int]
    SECTION_FIELD_NUMBER: _ClassVar[int]
    PATTERN_FIELD_NUMBER: _ClassVar[int]
    CODE_SMELL_FIELD_NUMBER: _ClassVar[int]
    SECURITY_ISSUE_FIELD_NUMBER: _ClassVar[int]
    FIELD_FIELD_NUMBER: _ClassVar[int]
    KEY_FIELD_NUMBER: _ClassVar[int]
    ACTION_FIELD_NUMBER: _ClassVar[int]
    DATA_ITEM_FIELD_NUMBER: _ClassVar[int]
    TABLE_FIELD_NUMBER: _ClassVar[int]
    TABLE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    PAGE_FIELD_NUMBER: _ClassVar[int]
    PAGE_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    CODEUNIT_FIELD_NUMBER: _ClassVar[int]
    REPORT_FIELD_NUMBER: _ClassVar[int]
    REPORT_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    ENUM_EXTENSION_FIELD_NUMBER: _ClassVar[int]
    AL_QUERY_FIELD_NUMBER: _ClassVar[int]
    XMLPORT_FIELD_NUMBER: _ClassVar[int]
    CONTROL_ADDIN_FIELD_NUMBER: _ClassVar[int]
    PERMISSION_SET_FIELD_NUMBER: _ClassVar[int]
    ENTITLEMENT_FIELD_NUMBER: _ClassVar[int]
    PROFILE_FIELD_NUMBER: _ClassVar[int]
    PROCEDURE_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_FIELD_NUMBER: _ClassVar[int]
    EVENT_SUBSCRIBER_FIELD_NUMBER: _ClassVar[int]
    EXTERNAL_OBJECT_FIELD_NUMBER: _ClassVar[int]
    project: Project
    package: Package
    folder: Folder
    module: Module
    class_node: Class
    function: Function
    method: Method
    file: File
    external_package: ExternalPackage
    module_implementation: ModuleImplementation
    module_interface: ModuleInterface
    interface_node: Interface
    enum_node: Enum
    type_node: Type
    union_node: Union
    external_module: ExternalModule
    resource: Resource
    section: Section
    pattern: Pattern
    code_smell: CodeSmell
    security_issue: SecurityIssue
    field: Field
    key: Key
    action: Action
    data_item: DataItem
    table: Table
    table_extension: TableExtension
    page: Page
    page_extension: PageExtension
    codeunit: Codeunit
    report: Report
    report_extension: ReportExtension
    enum_extension: EnumExtension
    al_query: ALQuery
    xmlport: Xmlport
    control_addin: ControlAddin
    permission_set: PermissionSet
    entitlement: Entitlement
    profile: Profile
    procedure: Procedure
    trigger: Trigger
    event_subscriber: EventSubscriber
    external_object: ExternalObject
    def __init__(self, project: _Optional[_Union[Project, _Mapping]] = ..., package: _Optional[_Union[Package, _Mapping]] = ..., folder: _Optional[_Union[Folder, _Mapping]] = ..., module: _Optional[_Union[Module, _Mapping]] = ..., class_node: _Optional[_Union[Class, _Mapping]] = ..., function: _Optional[_Union[Function, _Mapping]] = ..., method: _Optional[_Union[Method, _Mapping]] = ..., file: _Optional[_Union[File, _Mapping]] = ..., external_package: _Optional[_Union[ExternalPackage, _Mapping]] = ..., module_implementation: _Optional[_Union[ModuleImplementation, _Mapping]] = ..., module_interface: _Optional[_Union[ModuleInterface, _Mapping]] = ..., interface_node: _Optional[_Union[Interface, _Mapping]] = ..., enum_node: _Optional[_Union[Enum, _Mapping]] = ..., type_node: _Optional[_Union[Type, _Mapping]] = ..., union_node: _Optional[_Union[Union, _Mapping]] = ..., external_module: _Optional[_Union[ExternalModule, _Mapping]] = ..., resource: _Optional[_Union[Resource, _Mapping]] = ..., section: _Optional[_Union[Section, _Mapping]] = ..., pattern: _Optional[_Union[Pattern, _Mapping]] = ..., code_smell: _Optional[_Union[CodeSmell, _Mapping]] = ..., security_issue: _Optional[_Union[SecurityIssue, _Mapping]] = ..., field: _Optional[_Union[Field, _Mapping]] = ..., key: _Optional[_Union[Key, _Mapping]] = ..., action: _Optional[_Union[Action, _Mapping]] = ..., data_item: _Optional[_Union[DataItem, _Mapping]] = ..., table: _Optional[_Union[Table, _Mapping]] = ..., table_extension: _Optional[_Union[TableExtension, _Mapping]] = ..., page: _Optional[_Union[Page, _Mapping]] = ..., page_extension: _Optional[_Union[PageExtension, _Mapping]] = ..., codeunit: _Optional[_Union[Codeunit, _Mapping]] = ..., report: _Optional[_Union[Report, _Mapping]] = ..., report_extension: _Optional[_Union[ReportExtension, _Mapping]] = ..., enum_extension: _Optional[_Union[EnumExtension, _Mapping]] = ..., al_query: _Optional[_Union[ALQuery, _Mapping]] = ..., xmlport: _Optional[_Union[Xmlport, _Mapping]] = ..., control_addin: _Optional[_Union[ControlAddin, _Mapping]] = ..., permission_set: _Optional[_Union[PermissionSet, _Mapping]] = ..., entitlement: _Optional[_Union[Entitlement, _Mapping]] = ..., profile: _Optional[_Union[Profile, _Mapping]] = ..., procedure: _Optional[_Union[Procedure, _Mapping]] = ..., trigger: _Optional[_Union[Trigger, _Mapping]] = ..., event_subscriber: _Optional[_Union[EventSubscriber, _Mapping]] = ..., external_object: _Optional[_Union[ExternalObject, _Mapping]] = ...) -> None: ...

class Relationship(_message.Message):
    __slots__ = ("type", "source_id", "target_id", "properties", "source_label", "target_label")
    class RelationshipType(int, metaclass=_enum_type_wrapper.EnumTypeWrapper):
        __slots__ = ()
        RELATIONSHIP_TYPE_UNSPECIFIED: _ClassVar[Relationship.RelationshipType]
        CONTAINS_PACKAGE: _ClassVar[Relationship.RelationshipType]
        CONTAINS_FOLDER: _ClassVar[Relationship.RelationshipType]
        CONTAINS_FILE: _ClassVar[Relationship.RelationshipType]
        CONTAINS_MODULE: _ClassVar[Relationship.RelationshipType]
        DEFINES: _ClassVar[Relationship.RelationshipType]
        DEFINES_METHOD: _ClassVar[Relationship.RelationshipType]
        IMPORTS: _ClassVar[Relationship.RelationshipType]
        INHERITS: _ClassVar[Relationship.RelationshipType]
        OVERRIDES: _ClassVar[Relationship.RelationshipType]
        CALLS: _ClassVar[Relationship.RelationshipType]
        DEPENDS_ON_EXTERNAL: _ClassVar[Relationship.RelationshipType]
        IMPLEMENTS_MODULE: _ClassVar[Relationship.RelationshipType]
        IMPLEMENTS: _ClassVar[Relationship.RelationshipType]
        EXPORTS: _ClassVar[Relationship.RelationshipType]
        EXPORTS_MODULE: _ClassVar[Relationship.RelationshipType]
        READS_FROM: _ClassVar[Relationship.RelationshipType]
        WRITES_TO: _ClassVar[Relationship.RelationshipType]
        CONTAINS_SECTION: _ClassVar[Relationship.RelationshipType]
        EXPOSES: _ClassVar[Relationship.RelationshipType]
        FLOWS_TO: _ClassVar[Relationship.RelationshipType]
        HAS_SMELL: _ClassVar[Relationship.RelationshipType]
        HAS_VULNERABILITY: _ClassVar[Relationship.RelationshipType]
        IMPLEMENTS_PATTERN: _ClassVar[Relationship.RelationshipType]
        INSTANTIATES: _ClassVar[Relationship.RelationshipType]
        LINKS_TO: _ClassVar[Relationship.RelationshipType]
        REFERENCES: _ClassVar[Relationship.RelationshipType]
        RESOLVES_TO: _ClassVar[Relationship.RelationshipType]
        RETURNS: _ClassVar[Relationship.RelationshipType]
        ACCEPTS: _ClassVar[Relationship.RelationshipType]
        EXTENDS: _ClassVar[Relationship.RelationshipType]
        SUBSCRIBES_TO: _ClassVar[Relationship.RelationshipType]
        BINDS_TABLE: _ClassVar[Relationship.RelationshipType]
        HAS_FIELD: _ClassVar[Relationship.RelationshipType]
        HAS_KEY: _ClassVar[Relationship.RelationshipType]
        HAS_TRIGGER: _ClassVar[Relationship.RelationshipType]
        HAS_ACTION: _ClassVar[Relationship.RelationshipType]
        HAS_DATAITEM: _ClassVar[Relationship.RelationshipType]
        READS_TABLE: _ClassVar[Relationship.RelationshipType]
        DISPLAYS_FIELD: _ClassVar[Relationship.RelationshipType]
    RELATIONSHIP_TYPE_UNSPECIFIED: Relationship.RelationshipType
    CONTAINS_PACKAGE: Relationship.RelationshipType
    CONTAINS_FOLDER: Relationship.RelationshipType
    CONTAINS_FILE: Relationship.RelationshipType
    CONTAINS_MODULE: Relationship.RelationshipType
    DEFINES: Relationship.RelationshipType
    DEFINES_METHOD: Relationship.RelationshipType
    IMPORTS: Relationship.RelationshipType
    INHERITS: Relationship.RelationshipType
    OVERRIDES: Relationship.RelationshipType
    CALLS: Relationship.RelationshipType
    DEPENDS_ON_EXTERNAL: Relationship.RelationshipType
    IMPLEMENTS_MODULE: Relationship.RelationshipType
    IMPLEMENTS: Relationship.RelationshipType
    EXPORTS: Relationship.RelationshipType
    EXPORTS_MODULE: Relationship.RelationshipType
    READS_FROM: Relationship.RelationshipType
    WRITES_TO: Relationship.RelationshipType
    CONTAINS_SECTION: Relationship.RelationshipType
    EXPOSES: Relationship.RelationshipType
    FLOWS_TO: Relationship.RelationshipType
    HAS_SMELL: Relationship.RelationshipType
    HAS_VULNERABILITY: Relationship.RelationshipType
    IMPLEMENTS_PATTERN: Relationship.RelationshipType
    INSTANTIATES: Relationship.RelationshipType
    LINKS_TO: Relationship.RelationshipType
    REFERENCES: Relationship.RelationshipType
    RESOLVES_TO: Relationship.RelationshipType
    RETURNS: Relationship.RelationshipType
    ACCEPTS: Relationship.RelationshipType
    EXTENDS: Relationship.RelationshipType
    SUBSCRIBES_TO: Relationship.RelationshipType
    BINDS_TABLE: Relationship.RelationshipType
    HAS_FIELD: Relationship.RelationshipType
    HAS_KEY: Relationship.RelationshipType
    HAS_TRIGGER: Relationship.RelationshipType
    HAS_ACTION: Relationship.RelationshipType
    HAS_DATAITEM: Relationship.RelationshipType
    READS_TABLE: Relationship.RelationshipType
    DISPLAYS_FIELD: Relationship.RelationshipType
    TYPE_FIELD_NUMBER: _ClassVar[int]
    SOURCE_ID_FIELD_NUMBER: _ClassVar[int]
    TARGET_ID_FIELD_NUMBER: _ClassVar[int]
    PROPERTIES_FIELD_NUMBER: _ClassVar[int]
    SOURCE_LABEL_FIELD_NUMBER: _ClassVar[int]
    TARGET_LABEL_FIELD_NUMBER: _ClassVar[int]
    type: Relationship.RelationshipType
    source_id: str
    target_id: str
    properties: _struct_pb2.Struct
    source_label: str
    target_label: str
    def __init__(self, type: _Optional[_Union[Relationship.RelationshipType, str]] = ..., source_id: _Optional[str] = ..., target_id: _Optional[str] = ..., properties: _Optional[_Union[_struct_pb2.Struct, _Mapping]] = ..., source_label: _Optional[str] = ..., target_label: _Optional[str] = ...) -> None: ...

class Project(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Package(_message.Message):
    __slots__ = ("qualified_name", "name", "path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class Folder(_message.Message):
    __slots__ = ("path", "name")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class File(_message.Message):
    __slots__ = ("path", "name", "extension")
    PATH_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    EXTENSION_FIELD_NUMBER: _ClassVar[int]
    path: str
    name: str
    extension: str
    def __init__(self, path: _Optional[str] = ..., name: _Optional[str] = ..., extension: _Optional[str] = ...) -> None: ...

class Module(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "decorators", "rust_cfg_test_mods", "rust_ungated_mods", "flow_covered", "generated", "generator", "front_matter")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    DECORATORS_FIELD_NUMBER: _ClassVar[int]
    RUST_CFG_TEST_MODS_FIELD_NUMBER: _ClassVar[int]
    RUST_UNGATED_MODS_FIELD_NUMBER: _ClassVar[int]
    FLOW_COVERED_FIELD_NUMBER: _ClassVar[int]
    GENERATED_FIELD_NUMBER: _ClassVar[int]
    GENERATOR_FIELD_NUMBER: _ClassVar[int]
    FRONT_MATTER_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    decorators: _containers.RepeatedScalarFieldContainer[str]
    rust_cfg_test_mods: _containers.RepeatedScalarFieldContainer[str]
    rust_ungated_mods: _containers.RepeatedScalarFieldContainer[str]
    flow_covered: bool
    generated: bool
    generator: str
    front_matter: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., decorators: _Optional[_Iterable[str]] = ..., rust_cfg_test_mods: _Optional[_Iterable[str]] = ..., rust_ungated_mods: _Optional[_Iterable[str]] = ..., flow_covered: bool = ..., generated: bool = ..., generator: _Optional[str] = ..., front_matter: _Optional[_Iterable[str]] = ...) -> None: ...

class ExternalModule(_message.Message):
    __slots__ = ("qualified_name", "name", "path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class ModuleImplementation(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "implements_module")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    IMPLEMENTS_MODULE_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    implements_module: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., implements_module: _Optional[str] = ...) -> None: ...

class ModuleInterface(_message.Message):
    __slots__ = ("qualified_name", "name", "path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ...) -> None: ...

class ExternalPackage(_message.Message):
    __slots__ = ("name",)
    NAME_FIELD_NUMBER: _ClassVar[int]
    name: str
    def __init__(self, name: _Optional[str] = ...) -> None: ...

class Pattern(_message.Message):
    __slots__ = ("qualified_name", "name", "message", "start_line", "end_line", "path", "snippet")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    message: str
    start_line: int
    end_line: int
    path: str
    snippet: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., message: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., path: _Optional[str] = ..., snippet: _Optional[str] = ...) -> None: ...

class CodeSmell(_message.Message):
    __slots__ = ("qualified_name", "name", "message", "start_line", "end_line", "path", "snippet")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    message: str
    start_line: int
    end_line: int
    path: str
    snippet: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., message: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., path: _Optional[str] = ..., snippet: _Optional[str] = ...) -> None: ...

class SecurityIssue(_message.Message):
    __slots__ = ("qualified_name", "name", "message", "start_line", "end_line", "path", "snippet")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    MESSAGE_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    SNIPPET_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    message: str
    start_line: int
    end_line: int
    path: str
    snippet: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., message: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., path: _Optional[str] = ..., snippet: _Optional[str] = ...) -> None: ...

class Field(_message.Message):
    __slots__ = ("qualified_name", "name", "field_id", "field_type")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELD_ID_FIELD_NUMBER: _ClassVar[int]
    FIELD_TYPE_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    field_id: int
    field_type: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., field_id: _Optional[int] = ..., field_type: _Optional[str] = ...) -> None: ...

class Key(_message.Message):
    __slots__ = ("qualified_name", "name", "fields")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    FIELDS_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    fields: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., fields: _Optional[_Iterable[str]] = ...) -> None: ...

class Action(_message.Message):
    __slots__ = ("qualified_name", "name", "start_line", "end_line")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    start_line: int
    end_line: int
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ...) -> None: ...

class DataItem(_message.Message):
    __slots__ = ("qualified_name", "name", "source_table", "start_line", "end_line")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    SOURCE_TABLE_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    source_table: str
    start_line: int
    end_line: int
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., source_table: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ...) -> None: ...

class Table(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class TableExtension(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "extends_target", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_TARGET_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    extends_target: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., extends_target: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Page(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class PageExtension(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "extends_target", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_TARGET_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    extends_target: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., extends_target: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Codeunit(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Report(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class ReportExtension(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "extends_target", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_TARGET_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    extends_target: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., extends_target: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class EnumExtension(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "extends_target", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    EXTENDS_TARGET_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    extends_target: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., extends_target: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class ALQuery(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Xmlport(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class ControlAddin(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class PermissionSet(_message.Message):
    __slots__ = ("qualified_name", "name", "object_id", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    OBJECT_ID_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    object_id: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., object_id: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Entitlement(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Profile(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Procedure(_message.Message):
    __slots__ = ("qualified_name", "name", "access_modifier", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    ACCESS_MODIFIER_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    access_modifier: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., access_modifier: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Trigger(_message.Message):
    __slots__ = ("qualified_name", "name", "trigger_type", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    TRIGGER_TYPE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    trigger_type: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., trigger_type: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class EventSubscriber(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class ExternalObject(_message.Message):
    __slots__ = ("qualified_name", "name", "is_stub")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    IS_STUB_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    is_stub: bool
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., is_stub: bool = ...) -> None: ...

class Resource(_message.Message):
    __slots__ = ("qualified_name", "name", "kind")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    KIND_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    kind: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., kind: _Optional[str] = ...) -> None: ...

class Section(_message.Message):
    __slots__ = ("qualified_name", "name", "heading_level", "start_line", "end_line", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    HEADING_LEVEL_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    heading_level: int
    start_line: int
    end_line: int
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., heading_level: _Optional[int] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Function(_message.Message):
    __slots__ = ("qualified_name", "name", "docstring", "start_line", "end_line", "decorators", "is_exported", "ast_fingerprint", "ast_fingerprint_nodes", "ast_branch_fingerprints", "return_type", "param_types")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOCSTRING_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    DECORATORS_FIELD_NUMBER: _ClassVar[int]
    IS_EXPORTED_FIELD_NUMBER: _ClassVar[int]
    AST_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    AST_FINGERPRINT_NODES_FIELD_NUMBER: _ClassVar[int]
    AST_BRANCH_FINGERPRINTS_FIELD_NUMBER: _ClassVar[int]
    RETURN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAM_TYPES_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    docstring: str
    start_line: int
    end_line: int
    decorators: _containers.RepeatedScalarFieldContainer[str]
    is_exported: bool
    ast_fingerprint: str
    ast_fingerprint_nodes: int
    ast_branch_fingerprints: _containers.RepeatedScalarFieldContainer[str]
    return_type: str
    param_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., docstring: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., decorators: _Optional[_Iterable[str]] = ..., is_exported: bool = ..., ast_fingerprint: _Optional[str] = ..., ast_fingerprint_nodes: _Optional[int] = ..., ast_branch_fingerprints: _Optional[_Iterable[str]] = ..., return_type: _Optional[str] = ..., param_types: _Optional[_Iterable[str]] = ...) -> None: ...

class Method(_message.Message):
    __slots__ = ("qualified_name", "name", "docstring", "start_line", "end_line", "decorators", "ast_fingerprint", "ast_fingerprint_nodes", "ast_branch_fingerprints", "return_type", "param_types")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOCSTRING_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    DECORATORS_FIELD_NUMBER: _ClassVar[int]
    AST_FINGERPRINT_FIELD_NUMBER: _ClassVar[int]
    AST_FINGERPRINT_NODES_FIELD_NUMBER: _ClassVar[int]
    AST_BRANCH_FINGERPRINTS_FIELD_NUMBER: _ClassVar[int]
    RETURN_TYPE_FIELD_NUMBER: _ClassVar[int]
    PARAM_TYPES_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    docstring: str
    start_line: int
    end_line: int
    decorators: _containers.RepeatedScalarFieldContainer[str]
    ast_fingerprint: str
    ast_fingerprint_nodes: int
    ast_branch_fingerprints: _containers.RepeatedScalarFieldContainer[str]
    return_type: str
    param_types: _containers.RepeatedScalarFieldContainer[str]
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., docstring: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., decorators: _Optional[_Iterable[str]] = ..., ast_fingerprint: _Optional[str] = ..., ast_fingerprint_nodes: _Optional[int] = ..., ast_branch_fingerprints: _Optional[_Iterable[str]] = ..., return_type: _Optional[str] = ..., param_types: _Optional[_Iterable[str]] = ...) -> None: ...

class Class(_message.Message):
    __slots__ = ("qualified_name", "name", "docstring", "start_line", "end_line", "decorators", "is_exported")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    DOCSTRING_FIELD_NUMBER: _ClassVar[int]
    START_LINE_FIELD_NUMBER: _ClassVar[int]
    END_LINE_FIELD_NUMBER: _ClassVar[int]
    DECORATORS_FIELD_NUMBER: _ClassVar[int]
    IS_EXPORTED_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    docstring: str
    start_line: int
    end_line: int
    decorators: _containers.RepeatedScalarFieldContainer[str]
    is_exported: bool
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., docstring: _Optional[str] = ..., start_line: _Optional[int] = ..., end_line: _Optional[int] = ..., decorators: _Optional[_Iterable[str]] = ..., is_exported: bool = ...) -> None: ...

class Interface(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Enum(_message.Message):
    __slots__ = ("qualified_name", "name", "path", "absolute_path")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    PATH_FIELD_NUMBER: _ClassVar[int]
    ABSOLUTE_PATH_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    path: str
    absolute_path: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ..., path: _Optional[str] = ..., absolute_path: _Optional[str] = ...) -> None: ...

class Type(_message.Message):
    __slots__ = ("qualified_name", "name")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...

class Union(_message.Message):
    __slots__ = ("qualified_name", "name")
    QUALIFIED_NAME_FIELD_NUMBER: _ClassVar[int]
    NAME_FIELD_NUMBER: _ClassVar[int]
    qualified_name: str
    name: str
    def __init__(self, qualified_name: _Optional[str] = ..., name: _Optional[str] = ...) -> None: ...
