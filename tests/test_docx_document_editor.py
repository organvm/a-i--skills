import importlib
import re
import sys
import types
from pathlib import Path

import pytest


DOCX_ROOT = Path(__file__).resolve().parents[1] / "document-skills" / "docx"
WORD_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _install_docx_dependency_stubs():
    ooxml_pkg = types.ModuleType("ooxml")
    ooxml_pkg.__path__ = []
    scripts_pkg = types.ModuleType("ooxml.scripts")
    scripts_pkg.__path__ = []
    validation_pkg = types.ModuleType("ooxml.scripts.validation")
    validation_pkg.__path__ = []

    pack_mod = types.ModuleType("ooxml.scripts.pack")
    pack_mod.pack_document = lambda *args, **kwargs: None

    class PassingValidator:
        def __init__(self, *args, **kwargs):
            pass

        def validate(self):
            return True

    docx_mod = types.ModuleType("ooxml.scripts.validation.docx")
    docx_mod.DOCXSchemaValidator = PassingValidator
    redlining_mod = types.ModuleType("ooxml.scripts.validation.redlining")
    redlining_mod.RedliningValidator = PassingValidator

    sys.modules.update(
        {
            "ooxml": ooxml_pkg,
            "ooxml.scripts": scripts_pkg,
            "ooxml.scripts.pack": pack_mod,
            "ooxml.scripts.validation": validation_pkg,
            "ooxml.scripts.validation.docx": docx_mod,
            "ooxml.scripts.validation.redlining": redlining_mod,
        }
    )


@pytest.fixture(scope="module")
def document_module():
    _install_docx_dependency_stubs()
    sys.path.insert(0, str(DOCX_ROOT))
    try:
        yield importlib.import_module("scripts.document")
    finally:
        sys.path.remove(str(DOCX_ROOT))


@pytest.fixture
def editor(document_module, tmp_path):
    xml_path = tmp_path / "document.xml"
    xml_path.write_text(
        f"""<?xml version="1.0" encoding="utf-8"?>
<w:document xmlns:w="{WORD_NS}">
  <w:body>
    <w:p>
      <w:r w:rsidR="11111111"><w:t>Hello</w:t></w:r>
    </w:p>
  </w:body>
</w:document>
""",
        encoding="utf-8",
    )
    return document_module.DocxXMLEditor(
        xml_path, rsid="ABCDEF12", author="Ada", initials="AL"
    )


def first(editor, tag):
    return editor.dom.getElementsByTagName(tag)[0]


def text_of(node):
    parts = []
    for child in node.childNodes:
        if child.nodeType == child.TEXT_NODE:
            parts.append(child.data)
        elif child.nodeType == child.ELEMENT_NODE:
            parts.append(text_of(child))
    return "".join(parts)


def assert_wml_timestamp(value):
    assert re.fullmatch(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z", value)


def test_inserted_paragraph_gets_word_metadata_and_preserves_spaced_text(editor):
    body = first(editor, "w:body")

    inserted = editor.append_to(
        body,
        '<w:p><w:r><w:t> leading and trailing </w:t></w:r></w:p>',
    )[0]

    assert inserted.getAttribute("w:rsidR") == "ABCDEF12"
    assert inserted.getAttribute("w:rsidRDefault") == "ABCDEF12"
    assert inserted.getAttribute("w:rsidP") == "ABCDEF12"
    assert re.fullmatch(r"[0-7][0-9A-F]{7}", inserted.getAttribute("w14:paraId"))
    assert re.fullmatch(r"[0-7][0-9A-F]{7}", inserted.getAttribute("w14:textId"))
    assert editor.dom.documentElement.getAttribute("xmlns:w14").endswith(
        "/wordml"
    )

    inserted_run = inserted.getElementsByTagName("w:r")[0]
    inserted_text = inserted.getElementsByTagName("w:t")[0]
    assert inserted_run.getAttribute("w:rsidR") == "ABCDEF12"
    assert inserted_text.getAttribute("xml:space") == "preserve"


def test_suggest_deletion_wraps_run_and_converts_text(editor):
    run = first(editor, "w:r")

    deletion = editor.suggest_deletion(run)

    assert deletion.tagName == "w:del"
    assert deletion.getAttribute("w:id") == "0"
    assert deletion.getAttribute("w:author") == "Ada"
    assert_wml_timestamp(deletion.getAttribute("w:date"))
    assert deletion.getAttribute("w16du:dateUtc") == deletion.getAttribute("w:date")
    assert editor.dom.documentElement.hasAttribute("xmlns:w16du")

    deleted_run = deletion.getElementsByTagName("w:r")[0]
    assert deleted_run.getAttribute("w:rsidDel") == "11111111"
    assert not deleted_run.hasAttribute("w:rsidR")
    assert text_of(deletion.getElementsByTagName("w:delText")[0]) == "Hello"
    assert not deletion.getElementsByTagName("w:t")


def test_revert_deletion_creates_insertion_after_original_deletion(editor):
    para = first(editor, "w:p")
    deletion = editor.suggest_deletion(first(editor, "w:r"))

    _, insertion = editor.revert_deletion(deletion)

    assert insertion.tagName == "w:ins"
    assert insertion.getAttribute("w:id") == "1"
    assert insertion.getAttribute("w:author") == "Ada"
    assert insertion.previousSibling is deletion

    restored_run = insertion.getElementsByTagName("w:r")[0]
    assert restored_run.getAttribute("w:rsidR") == "11111111"
    assert not restored_run.hasAttribute("w:rsidDel")
    assert text_of(insertion.getElementsByTagName("w:t")[0]) == "Hello"
    assert list(para.childNodes).index(insertion) > list(para.childNodes).index(
        deletion
    )


def test_revert_insertion_wraps_inserted_content_as_deletion(editor):
    body = first(editor, "w:body")
    insertion = editor.append_to(
        body,
        '<w:ins w:id="4"><w:r w:rsidR="22222222"><w:t>Added</w:t></w:r></w:ins>',
    )[0]

    result = editor.revert_insertion(insertion)

    assert result == [insertion]
    nested_deletion = insertion.getElementsByTagName("w:del")[0]
    assert nested_deletion.getAttribute("w:id") == "5"
    assert nested_deletion.getAttribute("w:author") == "Ada"

    reverted_run = nested_deletion.getElementsByTagName("w:r")[0]
    assert reverted_run.getAttribute("w:rsidDel") == "22222222"
    assert not reverted_run.hasAttribute("w:rsidR")
    assert text_of(nested_deletion.getElementsByTagName("w:delText")[0]) == "Added"


def test_revert_operations_reject_nodes_without_matching_tracked_changes(editor):
    paragraph = first(editor, "w:p")

    with pytest.raises(ValueError, match="contains no insertions"):
        editor.revert_insertion(paragraph)

    with pytest.raises(ValueError, match="contains no deletions"):
        editor.revert_deletion(paragraph)


def test_suggest_paragraph_marks_properties_and_wraps_content(document_module):
    xml = (
        "<w:p>"
        "<w:pPr><w:rPr><w:b/></w:rPr></w:pPr>"
        "<w:r><w:t>One</w:t></w:r>"
        "<w:r><w:t>Two</w:t></w:r>"
        "</w:p>"
    )

    transformed = document_module.DocxXMLEditor.suggest_paragraph(xml)

    assert "<w:rPr><w:ins/><w:b/></w:rPr>" in transformed
    assert transformed.count("<w:ins") == 2
    assert "<w:ins><w:r><w:t>One</w:t></w:r><w:r><w:t>Two</w:t></w:r></w:ins>" in transformed
