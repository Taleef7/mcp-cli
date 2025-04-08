#!/usr/bin/env python3
"""
Setup file for the MCP CLI package.
"""

from setuptools import setup, find_packages

setup(
    name="mcp-cli",
    version="0.1.0",
    description="Graphical User Interface and CLI for MCP",
    author="MCP Team",
    packages=find_packages(include=['mcp_cli', 'mcp_cli.*']),
    install_requires=[
        "openai>=1.0.0",
        "aiohttp>=3.8.0",
        "python-dotenv>=1.0.0",
        "pyyaml>=6.0",
        "mcp-use>=0.1.0",
        "langchain-openai>=0.0.1",
        "PyQt5>=5.15.0",
        "Flask>=2.0.0",
        "Flask-CORS>=3.0.10",
    ],
    entry_points={
        "console_scripts": [
            "mcp-gui=mcp_cli.gui.app:main",
            "mcp=mcp_cli.cli:main",
            "mcp-server=mcp_cli.api.server:main",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
) 