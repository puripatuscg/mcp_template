# Image Platform MCP Server Template

MCP server template สำหรับทีม data science ที่ทำ image platform

## Quickstart

```bash
cp .env.example .env
# แก้ .env ใส่ IMAGE_API_BASE_URL และ IMAGE_API_KEY

pip install -r requirements.txt
python server.py
```

## Running Modes

| Mode | Command | Use case |
|------|---------|----------|
| stdio | `python server.py` | Claude Desktop / Claude Code (local dev) |
| HTTP | `TRANSPORT=http python server.py` | Production, multi-client |
| Docker | `docker build -t mcp . && docker run -p 8000:8000 --env-file .env mcp` | Container deploy |

## Claude Desktop Config (stdio mode)

เพิ่มใน `~/Library/Application Support/Claude/claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "image-platform": {
      "command": "python",
      "args": ["/absolute/path/to/mcp_template/server.py"],
      "env": {
        "IMAGE_API_BASE_URL": "http://your-api",
        "IMAGE_API_KEY": "your-key"
      }
    }
  }
}
```

## Available Tools

| Tool | Type | Description |
|------|------|-------------|
| `get_image_metadata` | Function | Get width, height, format ของ local image |
| `resize_image` | Function | Resize และ save local image |
| `detect_objects` | REST API | Detect objects ผ่าน image platform API |
| `classify_image` | REST API | Classify image ผ่าน image platform API |

## Adding New Tools

ดู `docs/adding-tools-guide.md` — มีตัวอย่าง code พร้อม TDD step-by-step

## Running Tests

```bash
pip install -r requirements-dev.txt
pytest tests/ -v
```

## Project Structure

```
├── server.py                    ← entry point
├── config.py                    ← env vars (แก้ที่นี่ที่เดียว)
├── tools/
│   ├── function_tools/
│   │   └── image_utils.py       ← Type 1: Python logic tools
│   └── api_tools/
│       ├── client.py            ← shared HTTP client (auth อยู่ตรงนี้)
│       └── image_platform.py   ← Type 2: REST API wrapper tools
├── tests/                       ← unit tests
└── docs/
    └── adding-tools-guide.md   ← how to add tools
```
