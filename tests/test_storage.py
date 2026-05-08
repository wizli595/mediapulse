import pytest

from shared.exceptions import StorageError


def test_write_and_read(tmp_storage):
    tmp_storage.write("bronze", "test.json", b'{"hello": "world"}')
    data = tmp_storage.read("bronze", "test.json")
    assert data == b'{"hello": "world"}'


def test_read_nonexistent(tmp_storage):
    with pytest.raises(StorageError):
        tmp_storage.read("bronze", "nope.json")


def test_exists(tmp_storage):
    assert not tmp_storage.exists("bronze", "x.json")
    tmp_storage.write("bronze", "x.json", b"data")
    assert tmp_storage.exists("bronze", "x.json")


def test_list_keys(tmp_storage):
    tmp_storage.write("silver", "a/1.json", b"1")
    tmp_storage.write("silver", "a/2.json", b"2")
    tmp_storage.write("silver", "b/3.json", b"3")

    keys = tmp_storage.list_keys("silver")
    assert len(keys) == 3


def test_list_keys_with_prefix(tmp_storage):
    tmp_storage.write("silver", "hespress/2025/01/abc.json", b"1")
    tmp_storage.write("silver", "bbc/2025/01/def.json", b"2")

    keys = tmp_storage.list_keys("silver", "hespress/")
    assert len(keys) == 1
    assert keys[0].startswith("hespress/")


def test_list_keys_empty_layer(tmp_storage):
    assert tmp_storage.list_keys("gold") == []


def test_delete(tmp_storage):
    tmp_storage.write("bronze", "del.json", b"x")
    assert tmp_storage.exists("bronze", "del.json")
    tmp_storage.delete("bronze", "del.json")
    assert not tmp_storage.exists("bronze", "del.json")


def test_nested_keys(tmp_storage):
    tmp_storage.write("bronze", "a/b/c/deep.json", b"deep")
    assert tmp_storage.read("bronze", "a/b/c/deep.json") == b"deep"
