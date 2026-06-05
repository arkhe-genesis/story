import pytest
from fordefi_bridge import FordefiBridge

def test_fordefi_bridge_initialization():
    bridge = FordefiBridge("test_api_key")
    assert bridge.base_url == "https://api.fordefi.com/api/v1"
    assert bridge.api_key == "test_api_key"
