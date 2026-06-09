# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install dependencies
uv pip install -e .

# Start the MCP server
uv run main.py

# Run all tests
uv run pytest

# Run a single test
uv run pytest tests/test_document.py::TestBinaryDocumentToMarkdown::test_binary_document_to_markdown_with_docx
```

## Architecture

This is a Python MCP (Model Context Protocol) server built with `FastMCP`. Tools are plain Python functions in `tools/` that get registered with the MCP server in `main.py`:

```python
mcp.tool()(my_function)
```

**Adding a new tool:** define the function in `tools/`, import it in `main.py`, and register it with `mcp.tool()()`.

### Defining MCP tools

Use `pydantic.Field` for every parameter to give it a description:

```python
from pydantic import Field

def my_tool(
    param1: str = Field(description="Detailed description of this parameter"),
    param2: int = Field(description="Explain what this parameter does"),
) -> ReturnType:
    """One-line summary.

    Detailed explanation of functionality.

    When to use:
    - Describe the appropriate use case
    - Describe when NOT to use this tool

    Examples:
    >>> my_tool("foo", 42)
    expected_output
    """
```

Tool docstrings must follow this four-part structure in order:
1. **One-line summary** — appears as the tool's short description
2. **Detailed explanation** — what the tool does and how it works
3. **When to use (and when NOT to use)** — helps the AI decide whether to invoke it
4. **Usage examples** — concrete input/output pairs

The docstring is what the AI assistant sees as the tool description, so specificity and the "when not to use" guidance directly affect how reliably the tool gets invoked correctly.

### Key modules

- `tools/math.py` — example arithmetic tool (`add`)
- `tools/document.py` — `binary_document_to_markdown(binary_data: bytes, file_type: str) -> str` converts `.docx`/`.pdf` bytes to markdown via `markitdown`; accepts a file extension string (e.g. `"docx"`, `"pdf"`)
- `tests/fixtures/` — `.docx` and `.pdf` files used by the document conversion tests
