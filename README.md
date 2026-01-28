# PRP - Python Registry Provider (Python包索引提供商)

## 目录 (Table of Contents)
- [简介](#prp---python-registry-provider-python包索引提供商)
- [功能](#功能)
- [安装](#安装)
- [使用方法](#使用方法)
- [可用索引源](#可用索引源)
- [贡献](#贡献)
- [许可证](#许可证)

PRP (Python Registry Provider) 是一个用于管理Python包索引源的命令行工具，类似于npm的nrm。它允许您轻松切换不同的Python包索引，如PyPI、TUNA、阿里云等。
PRP (Python Registry Provider) is a command-line tool for managing Python package index sources, similar to `nrm` for npm. It allows you to easily switch between different Python package indexes such as PyPI, TUNA, Aliyun, and more.

## 功能 (Features)

- 列出所有可用包索引源 (List all available package index sources)
- 一键切换包索引源 (Switch between package index sources with a single command)
- 添加自定义包索引源 (Add custom package index sources)
- 删除包索引源 (Remove package index sources)
- 测试包索引源速度 (Test package index source speeds)
- 查看当前包索引源 (View current package index source)

## 安装 (Installation)

```bash
pip install xiaobai-prp
```

## 使用方法 (Usage)

### 列出所有包索引源 (List all package index sources)
```bash
prp ls
```

### 切换到指定包索引源 (Switch to a package index source)
```bash
prp use tuna
```

### 添加自定义包索引源 (Add a custom package index source)
```bash
prp add myregistry https://myregistry.example.com/simple/
```

### 删除包索引源 (Delete a package index source)
```bash
prp del myregistry
```

### 测试包索引源速度 (Test package index source speeds)
```bash
prp test
```

### 显示当前包索引源 (Show current package index source)
```bash
prp current
```

## 可用索引源 (Available Registries)

- pypi - 官方PyPI仓库 (Official PyPI repository)
- tuna - 清华大学镜像 (Tsinghua University mirror)
- aliyun - 阿里云镜像 (Alibaba Cloud mirror)
- douban - 豆瓣镜像 (Douban mirror)
- huawei - 华为云镜像 (Huawei Cloud mirror)
- ustc - 中国科学技术大学镜像 (University of Science and Technology of China mirror)

## 贡献 (Contributing)

欢迎贡献！请随时提交Pull Request。
Contributions are welcome! Please feel free to submit a Pull Request.

## 许可证 (License)

本项目采用GPLv3许可证 - 详见LICENSE文件。
This project is licensed under the GNU General Public License v3 (GPLv3) License - see the LICENSE file for details.