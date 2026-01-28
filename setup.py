import importlib.util

# Check if setuptools is available
if importlib.util.find_spec("setuptools") is None:
    raise ImportError("setuptools is not installed. Please install it before running this setup.")

try:
    from setuptools import setup, find_packages
except ImportError as e:
    raise ImportError(f"Failed to import setuptools: {e}")

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="xiaobai-prp",
    version="1.0.10",
    author="Tser",
    author_email="807447312@qq.com",
    description="Python Registry Provider - A tool for managing Python package index sources similar to nrm for npm",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Tser/xiaobai-prp",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: 3.14",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "prp=prp.main:main",
        ],
    },
    install_requires=[
    ],
)