import os
import pytest
from unittest.mock import patch


def test_default_settings():
    from config import Settings
    s = Settings()
    assert s.IMAGE_API_BASE_URL == "http://localhost:8080"
    assert s.IMAGE_API_KEY == ""
    assert s.TRANSPORT == "stdio"
    assert s.HOST == "0.0.0.0"
    assert s.PORT == 8000
    assert s.LOG_LEVEL == "INFO"


def test_settings_read_from_env():
    with patch.dict(os.environ, {"IMAGE_API_KEY": "test-key-123", "PORT": "9000"}):
        from importlib import reload
        import config
        reload(config)
        s = config.Settings()
    assert s.IMAGE_API_KEY == "test-key-123"
    assert s.PORT == 9000


def test_invalid_transport_raises():
    with pytest.raises(Exception):
        from config import Settings
        Settings(TRANSPORT="invalid")
