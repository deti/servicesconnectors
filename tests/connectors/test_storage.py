import tempfile
from pathlib import Path
from unittest import mock

from src.connectors.storage import Storage


def test_storage_write_creates_file():
    """Test storage write"""
    tmp_path = Path(tempfile.TemporaryDirectory().name)
    with mock.patch("src.connectors.storage.STORAGE_PATH", tmp_path):
        storage = Storage()
        storage.write({"test": "test"}, "test")

    assert (tmp_path / "test.json").exists()


def test_storage_read_returns_none_if_file_not_exists():
    """Test storage read"""
    tmp_path = Path(tempfile.TemporaryDirectory().name)

    with mock.patch("src.connectors.storage.STORAGE_PATH", tmp_path):
        storage = Storage()
        data = storage.read("test")

    assert data is None


def test_storage_read_returns_file_as_json():
    """Test storage read"""
    tmp_path = Path(tempfile.TemporaryDirectory().name)

    with mock.patch("src.connectors.storage.STORAGE_PATH", tmp_path):
        storage = Storage()
        storage.write({"test": "test"}, "test")
        data = storage.read("test")

    assert data == {"test": "test"}


def test_storage_delete_removes_file():
    """Test storage delete"""
    tmp_path = Path(tempfile.TemporaryDirectory().name)

    with mock.patch("src.connectors.storage.STORAGE_PATH", tmp_path):
        storage = Storage()
        storage.write({"test": "test"}, "test")
        storage.delete("test")

    assert not (tmp_path / "test.json").exists()


def test_storage_delete_does_not_fail_if_file_not_exists():
    """Test storage delete"""
    tmp_path = Path(tempfile.TemporaryDirectory().name)

    assert not (tmp_path / "test.json").exists()

    with mock.patch("src.connectors.storage.STORAGE_PATH", tmp_path):
        storage = Storage()
        storage.delete("test")

    assert not (tmp_path / "test.json").exists()
