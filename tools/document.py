from markitdown import MarkItDown, StreamInfo
from io import BytesIO
from pathlib import Path
from pydantic import Field


def binary_document_to_markdown(binary_data: bytes, file_type: str) -> str:
    """Converts binary document data to markdown-formatted text."""
    md = MarkItDown()
    file_obj = BytesIO(binary_data)
    stream_info = StreamInfo(extension=file_type)
    result = md.convert(file_obj, stream_info=stream_info)
    return result.text_content


def document_path_to_markdown(
    file_path: str = Field(description="Absolute or relative path to a .docx or .pdf file"),
) -> str:
    """Convert a document file on disk to markdown-formatted text.

    Reads a .docx or .pdf file from the given path, determines the file type
    from its extension, and returns the document's content as markdown.

    When to use:
    - When you have a local file path to a document and need its text content
    - When processing a single document file for analysis or summarization

    When NOT to use:
    - When you already have the binary data in memory; use binary_document_to_markdown instead
    - For file types other than .docx and .pdf

    Examples:
    >>> document_path_to_markdown("/tmp/report.pdf")
    "# Report Title\\n\\nContent here..."
    >>> document_path_to_markdown("notes.docx")
    "# Notes\\n\\n- Item one..."
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")
    file_type = path.suffix.lstrip(".")
    binary_data = path.read_bytes()
    return binary_document_to_markdown(binary_data, file_type)
