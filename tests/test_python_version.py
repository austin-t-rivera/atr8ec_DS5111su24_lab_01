import sys
import pytest

supported_python_versions = ["3.8", "3.12"]

def test_python_version():
    current_version = sys.version.split()[0]
    error_message = f"Supported Python Versions {supported_python_versions}. Current Version: {current_version}"
    assert any(current_version.startswith(py) for py in supported_python_versions), error_message
