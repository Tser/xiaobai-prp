import pytest

from prp.main import PRP


def test_add_registry():
    """
    测试添加索引源
    """
    prp = PRP()
    prp.add_registry("pypi", "")
    assert prp.list_registries() == [
        {"name": "pypi", "url": "", "home": ""}
    ]

def test_delete_registry():
    """
    测试删除索引源
    """
    prp = PRP()
    prp.add_registry("pypi", "")
    prp.delete_registry("pypi")
    assert prp.list_registries() == []

def test_use_registry():
    """
    测试使用索引源
    """
    prp = PRP()
    prp.add_registry("pypi", "")
    prp.use_registry("pypi")
    assert prp.current_registry_info() == {
        "name": "pypi", "url": "", "home": ""
    }