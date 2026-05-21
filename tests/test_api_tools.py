import json
import pytest
from pytest_httpx import HTTPXMock


@pytest.mark.asyncio
async def test_detect_objects_posts_to_detect_endpoint(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/detect",
        json={"objects": [{"label": "car", "confidence": 0.95, "bbox": [10, 20, 100, 200]}]},
    )

    from tools.api_tools.image_platform import detect_objects
    result = await detect_objects("http://example.com/img.jpg", model="yolo")

    assert result == {"objects": [{"label": "car", "confidence": 0.95, "bbox": [10, 20, 100, 200]}]}


@pytest.mark.asyncio
async def test_detect_objects_sends_correct_payload(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/detect",
        json={"objects": []},
    )

    from tools.api_tools.image_platform import detect_objects
    await detect_objects("http://example.com/img.jpg", model="faster-rcnn")

    request = httpx_mock.get_requests()[0]
    body = json.loads(request.content)
    assert body["image_url"] == "http://example.com/img.jpg"
    assert body["model"] == "faster-rcnn"


@pytest.mark.asyncio
async def test_classify_image_posts_to_classify_endpoint(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/classify",
        json={"predictions": [{"class": "cat", "confidence": 0.92}]},
    )

    from tools.api_tools.image_platform import classify_image
    result = await classify_image("http://example.com/cat.jpg", top_k=1)

    assert result == {"predictions": [{"class": "cat", "confidence": 0.92}]}


@pytest.mark.asyncio
async def test_detect_objects_raises_on_http_error(httpx_mock: HTTPXMock):
    httpx_mock.add_response(
        method="POST",
        url="http://localhost:8080/detect",
        status_code=500,
    )

    from tools.api_tools.image_platform import detect_objects
    with pytest.raises(Exception):
        await detect_objects("http://example.com/img.jpg")
