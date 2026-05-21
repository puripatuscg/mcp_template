from unittest.mock import patch, MagicMock


def test_get_image_metadata_returns_size_and_format():
    mock_img = MagicMock()
    mock_img.width = 1920
    mock_img.height = 1080
    mock_img.format = "JPEG"

    with patch("PIL.Image.open", return_value=mock_img):
        from tools.function_tools.image_utils import get_image_metadata
        result = get_image_metadata("test.jpg")

    assert result == {"width": 1920, "height": 1080, "format": "JPEG"}


def test_get_image_metadata_works_with_png():
    mock_img = MagicMock()
    mock_img.width = 512
    mock_img.height = 512
    mock_img.format = "PNG"

    with patch("PIL.Image.open", return_value=mock_img):
        from tools.function_tools.image_utils import get_image_metadata
        result = get_image_metadata("icon.png")

    assert result["format"] == "PNG"


def test_resize_image_calls_resize_and_save():
    mock_img = MagicMock()
    mock_resized = MagicMock()
    mock_img.resize.return_value = mock_resized

    with patch("PIL.Image.open", return_value=mock_img):
        from tools.function_tools.image_utils import resize_image
        result = resize_image("input.jpg", 800, 600, "output.jpg")

    mock_img.resize.assert_called_once_with((800, 600))
    mock_resized.save.assert_called_once_with("output.jpg")
    assert result == "output.jpg"


def test_resize_image_returns_output_path():
    mock_img = MagicMock()
    mock_img.resize.return_value = MagicMock()

    with patch("PIL.Image.open", return_value=mock_img):
        from tools.function_tools.image_utils import resize_image
        result = resize_image("a.jpg", 100, 100, "/tmp/resized.jpg")

    assert result == "/tmp/resized.jpg"
