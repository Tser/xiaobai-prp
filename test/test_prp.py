import pytest
import sys
import os

# 添加项目根目录到Python路径，以便正确导入prp模块
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from prp.main import PRP

def test_add_registry():
    """
    测试添加索引源
    """
    prp = PRP()
    # 修复测试：添加有效的注册表
    prp.add_registry("test_registry", "https://test.registry.com/simple/", "https://test.registry.com/")
    # 检查注册表是否被正确添加
    assert "test_registry" in prp.registries

def test_delete_registry():
    """
    测试删除索引源
    """
    prp = PRP()
    # 先添加一个注册表
    prp.add_registry("temp_registry", "https://temp.registry.com/simple/", "https://temp.registry.com/")
    # 确认注册表存在
    assert "temp_registry" in prp.registries
    # 删除注册表
    prp.delete_registry("temp_registry")
    # 检查注册表是否被删除
    assert "temp_registry" not in prp.registries

def test_use_registry():
    """
    测试使用索引源
    """
    prp = PRP()
    # 添加一个注册表用于测试
    prp.add_registry("test_registry", "https://test.registry.com/simple/", "https://test.registry.com/")
    # 切换到该注册表
    result = prp.use_registry("test_registry")
    # 检查是否切换成功
    assert result is True
    assert prp.current_registry == "test_registry"

def test_list_registries(capsys):
    """
    测试列出所有索引源
    """
    prp = PRP()
    # 调用list_registries方法
    prp.list_registries()
    # 捕获输出
    captured = capsys.readouterr()
    # 检查输出是否包含注册表列表
    assert "Available Registries:" in captured.out

def test_current_registry_info(capsys):
    """
    测试显示当前索引源信息
    """
    prp = PRP()
    # 调用current_registry_info方法
    prp.current_registry_info()
    # 捕获输出
    captured = capsys.readouterr()
    # 检查输出是否包含当前注册表信息
    assert "Current registry:" in captured.out