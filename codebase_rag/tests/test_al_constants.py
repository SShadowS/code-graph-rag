from codebase_rag import constants as cs
from codebase_rag.types_defs import NODE_SCHEMAS, RELATIONSHIP_SCHEMAS


def test_al_node_schemas_registered():
    schema_labels = {s.label for s in NODE_SCHEMAS}
    for label in [cs.NodeLabel.TABLE, cs.NodeLabel.CODEUNIT, cs.NodeLabel.FIELD]:
        assert label in schema_labels, f"{label} not in NODE_SCHEMAS"


def test_al_relationship_schemas_registered():
    schema_types = {s.rel_type for s in RELATIONSHIP_SCHEMAS}
    for rel in [cs.RelationshipType.HAS_FIELD, cs.RelationshipType.EXTENDS]:
        assert rel in schema_types, f"{rel} not in RELATIONSHIP_SCHEMAS"


def test_al_in_supported_language():
    assert hasattr(cs.SupportedLanguage, "AL")
    assert cs.SupportedLanguage.AL == "al"


def test_al_in_tree_sitter_module():
    assert hasattr(cs.TreeSitterModule, "AL")
    assert cs.TreeSitterModule.AL == "tree_sitter_al"


def test_al_node_labels_exist():
    for name in [
        "TABLE",
        "TABLE_EXTENSION",
        "PAGE",
        "PAGE_EXTENSION",
        "CODEUNIT",
        "REPORT",
        "REPORT_EXTENSION",
        "ENUM_EXTENSION",
        "AL_QUERY",
        "XMLPORT",
        "CONTROL_ADDIN",
        "PERMISSION_SET",
        "ENTITLEMENT",
        "PROFILE",
        "PROCEDURE",
        "TRIGGER",
        "EVENT_SUBSCRIBER",
        "FIELD",
        "KEY",
        "ACTION",
        "DATA_ITEM",
        "EXTERNAL_OBJECT",
    ]:
        assert hasattr(cs.NodeLabel, name), f"NodeLabel.{name} missing"


def test_al_relationship_types_exist():
    for name in [
        "EXTENDS",
        "SUBSCRIBES_TO",
        "BINDS_TABLE",
        "HAS_FIELD",
        "HAS_KEY",
        "HAS_TRIGGER",
        "HAS_ACTION",
        "HAS_DATAITEM",
        "READS_TABLE",
        "DISPLAYS_FIELD",
    ]:
        assert hasattr(cs.RelationshipType, name), f"RelationshipType.{name} missing"


def test_al_file_extension():
    assert cs.EXT_AL == ".al"
    assert cs.AL_EXTENSIONS == (".al",)


def test_al_language_metadata():
    assert cs.SupportedLanguage.AL in cs.LANGUAGE_METADATA
