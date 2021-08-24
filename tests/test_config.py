from math_notes.configs import config

from pathlib import Path

def test_paths():
    """Test that paths exist."""
    assert Path.exists(config.app_id_path) == True
    assert Path.exists(config.app_key_path) == True

def test_not_empty_keys():
    """Test that keys loaded are not empty."""
    assert config.APP_ID != ""
    assert config.APP_KEY != ""
