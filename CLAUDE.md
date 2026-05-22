# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

```bash
# Install runtime deps
pip install -r requirements.txt

# Install dev/test deps (includes runtime)
pip install -r requirements-dev.txt

# Run all tests
pytest tests/ -v

# Run a single test file
pytest tests/test_function_tools.py -v

# Run a single test by name
pytest tests/test_api_tools.py::test_detect_objects_posts_to_detect_endpoint -v

# Run server (stdio mode — default for local dev)
python server.py

# Run server (HTTP mode)
TRANSPORT=http python server.py

# Copy env template
cp .env.example .env
```

## Architecture

A single FastMCP server that registers tools from two modules. Business logic lives at **module level** (outside `register()`), so tools can be unit-tested by importing them directly without going through the MCP protocol.

### Adding a tool — the only pattern used here

1. Write a function at module level in the appropriate `tools/` file
2. Add `mcp.tool()(your_function)` inside that file's `register(mcp)` function
3. If creating a new file, also import and call its `register` in `server.py`

**Function tool** (pure Python, no HTTP):
```python
# tools/function_tools/image_utils.py
def my_tool(param: str) -> dict:
    """One-line description.

    Args:
        param: What this parameter does
    """
    ...

def register(mcp: FastMCP) -> None:
    mcp.tool()(my_tool)
```

**API tool** (calls REST endpoint):
```python
# tools/api_tools/image_platform.py
async def my_api_tool(param: str) -> dict:
    """One-line description.

    Args:
        param: What this parameter does
    """
    async with get_client() as client:
        r = await client.post("/endpoint", json={"param": param})
        r.raise_for_status()
        return r.json()

def register(mcp: FastMCP) -> None:
    mcp.tool()(my_api_tool)
```

### Key files

| File | Role |
|------|------|
| `server.py` | Creates `FastMCP` app, calls all `register()` functions — only wiring, no logic |
| `config.py` | All env vars (`IMAGE_API_BASE_URL`, `IMAGE_API_KEY`, `TRANSPORT`, etc.) — single source of truth |
| `tools/api_tools/client.py` | `get_client()` factory — the only place auth headers are set |
| `tools/function_tools/image_utils.py` | Function tools: `get_image_metadata`, `resize_image` |
| `tools/api_tools/image_platform.py` | API tools: `detect_objects`, `classify_image` |
| `tools/function_tools/math_utils.py` | Function tools: `compound_interest`, `convert_units` |
| `tools/api_tools/math_platform.py` | API tools: `calculate_statistics`, `amortize_loan` |

### Config

Settings are loaded from `.env` via `pydantic-settings`. `TRANSPORT` is `Literal["stdio", "http"]` — pydantic rejects any other value at startup. Add new env vars to `config.py` **and** `.env.example`.

### Testing patterns

- **Function tools**: import and call directly — no mocking needed unless using I/O (e.g. mock `PIL.Image.open` for image tools)
- **API tools**: use `pytest-httpx`'s `HTTPXMock` fixture — mock by full URL (`http://localhost:8080/endpoint`)
- `asyncio_mode = "auto"` in `pyproject.toml` — no need for `@pytest.mark.asyncio` decorators (though they still work)
- Default `IMAGE_API_BASE_URL` is `http://localhost:8080` — match this in mock URLs
- Test files: `test_function_tools.py`, `test_api_tools.py`, `test_math_function_tools.py`, `test_math_api_tools.py`

### Tool docstrings matter

The MCP client (AI agent) reads the docstring to decide which tool to call. Every tool **must** have a one-line summary and an `Args:` section describing each parameter.
