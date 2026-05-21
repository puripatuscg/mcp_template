# วิธีเพิ่ม Tool ใหม่ / How to Add a New Tool

## ภาพรวม / Overview

Tools ใน MCP server นี้มี 2 ประเภท:
1. **Function Tool** — Python logic ล้วน (ไม่เรียก API ภายนอก)
2. **API Tool** — เรียก REST API endpoint ของ image platform

---

## เพิ่ม Function Tool

### ขั้นตอน:

**1. เขียน test ก่อน** ใน `tests/test_function_tools.py`:

```python
def test_convert_to_grayscale():
    mock_img = MagicMock()
    mock_gray = MagicMock()
    mock_img.convert.return_value = mock_gray

    with patch("PIL.Image.open", return_value=mock_img):
        from tools.function_tools.image_utils import convert_to_grayscale
        result = convert_to_grayscale("color.jpg", "gray.jpg")

    mock_img.convert.assert_called_once_with("L")
    assert result == "gray.jpg"
```

**2. เพิ่ม function** ใน `tools/function_tools/image_utils.py` — เขียน logic ที่ module level (ข้างนอก `register()`):

```python
def convert_to_grayscale(image_path: str, output_path: str) -> str:
    """Convert a color image to grayscale and save.

    Args:
        image_path: Path to the source color image
        output_path: Path to save the grayscale image
    """
    from PIL import Image
    img = Image.open(image_path).convert("L")
    img.save(output_path)
    return output_path
```

**3. ลง register** ใน `register()` ของไฟล์เดียวกัน:

```python
def register(mcp: FastMCP) -> None:
    mcp.tool()(get_image_metadata)
    mcp.tool()(resize_image)
    mcp.tool()(convert_to_grayscale)  # ← เพิ่มตรงนี้
```

**4. รัน test**: `pytest tests/test_function_tools.py -v`

> **ถ้าสร้าง file ใหม่** เช่น `tools/function_tools/color_tools.py`:
> ต้อง import และเรียก `register` ใน `server.py` ด้วย:
> ```python
> from tools.function_tools.color_tools import register as register_color_tools
> register_color_tools(mcp)
> ```

---

## เพิ่ม API Tool

### ขั้นตอน:

**1. เขียน test ก่อน** ใน `tests/test_api_tools.py`:

```python
@pytest.mark.asyncio
async def test_upload_image(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/upload",
        json={"image_id": "abc123", "status": "uploaded"},
    )

    from tools.api_tools.image_platform import upload_image
    result = await upload_image("http://example.com/photo.jpg")

    assert result["image_id"] == "abc123"
```

**2. เพิ่ม async function** ใน `tools/api_tools/image_platform.py` ที่ module level:

```python
async def upload_image(image_url: str) -> dict:
    """Upload an image URL to the image platform for processing.

    Args:
        image_url: Publicly accessible URL of the image to upload
    """
    async with get_client() as client:
        r = await client.post("/upload", json={"image_url": image_url})
        r.raise_for_status()
        return r.json()
```

**3. ลง register**:

```python
def register(mcp: FastMCP) -> None:
    mcp.tool()(detect_objects)
    mcp.tool()(classify_image)
    mcp.tool()(upload_image)  # ← เพิ่มตรงนี้
```

**4. รัน test**: `pytest tests/test_api_tools.py -v`

---

## กฎสำคัญ / Key Rules

| Rule | เหตุผล |
|------|--------|
| Docstring + `Args:` section บังคับทุก tool | AI ใช้ข้อมูลนี้ตัดสินใจว่าจะเรียก tool ไหน |
| Functions ต้องอยู่ที่ module level (ข้างนอก `register()`) | เพื่อให้ import มา test ได้โดยตรง |
| ใช้ `get_client()` จาก `client.py` เสมอ | ไม่สร้าง httpx client เองใน tool function |
| เพิ่ม env var ใหม่ → แก้ `config.py` + `.env.example` | settings อยู่ที่เดียว ไม่กระจาย |
