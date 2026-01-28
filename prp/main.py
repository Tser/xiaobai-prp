#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PRP - Python Registry Provider
A tool for managing Python package index sources similar to nrm for npm.
"""

import os
import sys
import json
import time
import argparse
from urllib.parse import urlparse
import urllib.request
import urllib.error


class PRP:
    def __init__(self):
        self.config_file = os.path.expanduser("~/.prp/config.json")
        # 设置pip配置文件的正确路径
        if sys.platform.startswith("win"):
            # Windows系统的pip配置文件路径
            self.pip_config_file = os.path.expandvars("%APPDATA%/pip/pip.ini")
        else:
            # Mac/Linux系统的pip配置文件路径
            self.pip_config_file = os.path.expanduser("~/.config/pip/pip.conf")
        self.ensure_config_exists()
        self.load_registries()

    def ensure_config_exists(self):
        """确保配置文件存在"""
        config_dir = os.path.dirname(self.config_file)
        if not os.path.exists(config_dir):
            os.makedirs(config_dir)
        
        if not os.path.exists(self.config_file):
            # 创建默认配置
            default_config = {
                "registries": {
                    "pypi": {
                        "url": "https://pypi.org/simple/",
                        "home": "https://pypi.org",
                        "name": "pypi"
                    },
                    "tuna": {
                        "url": "https://pypi.tuna.tsinghua.edu.cn/simple/",
                        "home": "https://pypi.tuna.tsinghua.edu.cn",
                        "name": "tuna"
                    },
                    "aliyun": {
                        "url": "https://mirrors.aliyun.com/pypi/simple/",
                        "home": "https://mirrors.aliyun.com",
                        "name": "aliyun"
                    },
                    "douban": {
                        "url": "https://pypi.douban.com/simple/",
                        "home": "https://pypi.douban.com",
                        "name": "douban"
                    },
                    "huawei": {
                        "url": "https://mirrors.huaweicloud.com/repository/pypi/simple/",
                        "home": "https://mirrors.huaweicloud.com/",
                        "name": "huawei"
                    },
                    "ustc": {
                        "url": "https://pypi.mirrors.ustc.edu.cn/simple/",
                        "home": "https://mirrors.ustc.edu.cn/",
                        "name": "ustc"
                    }
                },
                "current_registry": "pypi"
            }
            
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(default_config, f, indent=2, ensure_ascii=False)
    
    def load_registries(self):
        """加载包索引源配置"""
        with open(self.config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
            self.registries = config['registries']
            self.current_registry = config.get('current_registry', 'pypi')

    def save_config(self):
        """保存配置"""
        config = {
            'registries': self.registries,
            'current_registry': self.current_registry
        }
        with open(self.config_file, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2, ensure_ascii=False)

    def list_registries(self):
        """列出所有包索引源"""
        current_name = self.current_registry
        print("\nAvailable Registries:")
        for name, info in self.registries.items():
            marker = " * " if name == current_name else "   "
            print(f"{marker} {name:<10} {info['url']}")
        print("\n* Current Registry\n")

    def add_registry(self, name, url, home=None):
        """添加新的包索引源"""
        if not url.endswith('/'):
            url += '/'
        if home is None:
            # 尝试从URL推断主页
            parsed = urlparse(url)
            home = f"{parsed.scheme}://{parsed.netloc}"
        
        self.registries[name] = {
            "url": url,
            "home": home,
            "name": name
        }
        self.save_config()
        print(f"Registry '{name}' added successfully.")

    def delete_registry(self, name):
        """删除包索引源"""
        if name not in self.registries:
            print(f"Registry '{name}' does not exist.")
            return
        
        if len(self.registries) <= 1:
            print("Cannot delete the last registry.")
            return
            
        del self.registries[name]
        if self.current_registry == name:
            self.current_registry = next(iter(self.registries))  # 设置为第一个可用的
        self.save_config()
        print(f"Registry '{name}' deleted successfully.")

    def use_registry(self, name):
        """切换到指定包索引源并更新pip配置"""
        if name not in self.registries:
            print(f"Registry '{name}' does not exist.")
            return False
        
        self.current_registry = name
        self.save_config()
        
        # 更新pip配置文件
        success = self.update_pip_config()
        if success:
            registry_url = self.registries[name]['url']
            print(f"Successfully switched to registry '{name}': {registry_url}")
            print("pip will now use this registry by default.")
            return True
        else:
            print(f"Failed to update pip configuration for registry '{name}'.")
            return False

    def update_pip_config(self):
        """更新pip配置文件以使用当前选定的包索引源"""
        registry_url = self.registries[self.current_registry]['url']
        
        # 确保目录存在
        pip_config_dir = os.path.dirname(self.pip_config_file)
        if not os.path.exists(pip_config_dir):
            os.makedirs(pip_config_dir)
        
        # 读取现有配置
        config_content = ""
        if os.path.exists(self.pip_config_file):
            with open(self.pip_config_file, 'r', encoding='utf-8') as f:
                config_content = f.read()
        
        # 解析现有配置，保留其他设置
        lines = config_content.splitlines()
        new_lines = []
        found_global_section = False
        replaced_index_url = False
        
        for line in lines:
            stripped = line.strip()
            if stripped == "[global]" and not found_global_section:
                new_lines.append(line)
                # 在[global]部分添加或替换index-url
                new_lines.append(f"index-url = {registry_url}")
                found_global_section = True
                replaced_index_url = True
            elif stripped.startswith("index-url = ") and found_global_section:
                # 跳过旧的index-url行，因为我们已经在[global]后添加了新的
                continue
            else:
                new_lines.append(line)
        
        # 如果没有找到[global]部分，则添加
        if not found_global_section:
            if new_lines and new_lines[-1] != "":
                new_lines.append("")
            new_lines.append("[global]")
            new_lines.append(f"index-url = {registry_url}")
        elif not replaced_index_url:
            # 如果找到了[global]但没有替换index-url（因为不在第一行）
            idx = -1
            for i, line in enumerate(new_lines):
                if line.strip() == "[global]":
                    idx = i
                    break
            if idx != -1:
                new_lines.insert(idx + 1, f"index-url = {registry_url}")
        
        # 写入更新后的配置
        with open(self.pip_config_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(new_lines))
        
        return True

    def test_registry_speed(self, name=None):
        """测试包索引源速度"""
        if name:
            registries_to_test = {name: self.registries[name]} if name in self.registries else {}
        else:
            registries_to_test = self.registries

        print(f"\nTesting registry speeds...")
        results = []
        
        for reg_name, info in registries_to_test.items():
            url = info['url']
            start_time = time.time()
            try:
                # 使用urllib替换requests
                req = urllib.request.Request(url, method="HEAD")
                req.add_header('User-Agent', 'Mozilla/5.0 (PRP Test)')
                
                # 发起请求并计算响应时间
                response = urllib.request.urlopen(req, timeout=5)
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 2)
                
                # 检查是否可以访问
                status = "OK" if response.getcode() in [200, 403] else str(response.getcode())
                results.append((reg_name, response_time, status))
                
            except urllib.error.HTTPError as e:
                # 处理HTTP错误
                end_time = time.time()
                response_time = round((end_time - start_time) * 1000, 2)
                results.append((reg_name, response_time, f"Error: {e.code}"))
            except urllib.error.URLError as e:
                # 处理URL错误（如连接失败）
                results.append((reg_name, float('inf'), f"Error: {str(e.reason)}"))
            except Exception as e:
                # 处理其他异常
                results.append((reg_name, float('inf'), f"Error: {str(e)}"))
        
        # 按响应时间排序
        results.sort(key=lambda x: x[1] if isinstance(x[1], (int, float)) else float('inf'))
        
        print(f"\n{'Registry':<10} {'Response Time (ms)':<20} {'Status':<10}")
        print("-" * 45)
        for name, response_time, status in results:
            rt_str = f"{response_time}ms" if isinstance(response_time, (int, float)) else "N/A"
            print(f"{name:<10} {rt_str:<20} {status:<10}")

    def current_registry_info(self):
        """显示当前包索引源信息"""
        # 首先检查pip配置文件中的实际设置
        actual_source = self.get_current_source_from_pip_config()
        
        if actual_source:
            # 查找匹配的索引名称
            matched_registry_name = None
            matched_registry_info = None
            for name, info in self.registries.items():
                if info['url'].rstrip('/') == actual_source.rstrip('/'):
                    matched_registry_name = name
                    matched_registry_info = info
                    break
            
            if matched_registry_name:
                print(f"Current registry: {matched_registry_name}")
                print(f"URL: {actual_source}")
                print("(Detected from pip configuration)")
            else:
                # 如果不在索引中，自动添加
                auto_name = self.generate_auto_registry_name(actual_source)
                self.registries[auto_name] = {
                    "url": actual_source,
                    "home": self.extract_homepage(actual_source),
                    "name": auto_name
                }
                self.save_config()
                
                print(f"Current registry: {auto_name}")
                print(f"URL: {actual_source}")
                print(f"(Automatically added from pip configuration as {auto_name})")
        else:
            # 如果无法从pip配置中获取，使用内部配置
            if self.current_registry in self.registries:
                info = self.registries[self.current_registry]
                print(f"Current registry: {self.current_registry}")
                print(f"URL: {info['url']}")
            else:
                print("No current registry set.")
        
        print(f"Configured in pip: {self.pip_config_file}")

    def extract_homepage(self, url):
        """从URL提取主页地址"""
        parsed = urlparse(url)
        return f"{parsed.scheme}://{parsed.netloc}"

    def generate_auto_registry_name(self, url):
        """从URL中提取合适的名称，通过分割域名的方式"""

        # 解析URL获取主机名
        parsed = urlparse(url)
        hostname = parsed.netloc.lower()
        
        # 按照点分割域名
        parts = hostname.split('.')
        
        # 定义需要忽略的关键词
        skip_parts = {'pypi', 'mirror', 'mirrors'}
        
        # 按照默认顺序查找第一个不是skip_parts中的部分
        candidate_name = None
        for part in parts:
            if part not in skip_parts:
                candidate_name = part.replace('pypi', '').replace('mirror', '').replace('mirrors', '')
                break
        
        # 如果仍然找不到合适的名称，使用整个主机名作为基础
        if not candidate_name:
            candidate_name = hostname.replace('.', '_')
        
        # 确保名称不与现有名称冲突
        final_name = candidate_name
        counter = 0
        while final_name in self.registries:
            final_name = f"{candidate_name}{counter}"
            counter += 1
            
        return final_name

    def get_current_source_from_pip_config(self):
        """从pip配置文件中获取当前设置的索引源"""
        if not os.path.exists(self.pip_config_file):
            return None
        
        try:
            with open(self.pip_config_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            in_global_section = False
            for line in lines:
                line = line.strip()
                
                # 检查是否进入[global]部分
                if line == '[global]':
                    in_global_section = True
                    continue
                
                # 如果在[global]部分，查找index-url
                if in_global_section and line.startswith('index-url = '):
                    url = line.split('=', 1)[1].strip()
                    return url
            
            return None
        except Exception:
            # 如果读取配置文件出现问题，返回None
            return None


def main():
    parser = argparse.ArgumentParser(
        prog='prp',
        description='Python Registry Provider - 管理Python包索引源(Manage Python package index sources)\n  by 807447312@qq.com'
    )
    
    subparsers = parser.add_subparsers(dest='command', help='可用命令(Available commands)')
    
    # List command
    subparsers.add_parser('ls', help='列出所有包索引源(List all registries)')
    
    # Add command
    add_parser = subparsers.add_parser('add', help='添加新的包索引源(Add a new registry)')
    add_parser.add_argument('name', help='包索引源名称(Registry name)')
    add_parser.add_argument('url', help='包索引源URL(Registry URL)')
    add_parser.add_argument('home', nargs='?', help='包索引源主页(可选)(Registry homepage (optional))')
    
    # Delete command
    del_parser = subparsers.add_parser('del', help='删除包索引源(Delete a registry)')
    del_parser.add_argument('name', help='要删除的包索引源名称(Registry name to delete)')
    
    # Use command
    use_parser = subparsers.add_parser('use', help='切换到指定包索引源(Switch to a registry)')
    use_parser.add_argument('name', help='要切换到的包索引源名称(Registry name to switch to)')
    
    # Test command
    test_parser = subparsers.add_parser('test', help='测试包索引源速度(Test registry speed)')
    test_parser.add_argument('name', nargs='?', help='要测试的特定包索引源名称(可选)(Specific registry name to test (optional))')
    
    # Current command
    subparsers.add_parser('current', help='显示当前包索引源(Show current registry)')
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        return
    
    prp = PRP()
    
    if args.command == 'ls':
        prp.list_registries()
    elif args.command == 'add':
        prp.add_registry(args.name, args.url, args.home)
    elif args.command == 'del':
        prp.delete_registry(args.name)
    elif args.command == 'use':
        prp.use_registry(args.name)
    elif args.command == 'test':
        prp.test_registry_speed(args.name)
    elif args.command == 'current':
        prp.current_registry_info()


if __name__ == '__main__':
    main()