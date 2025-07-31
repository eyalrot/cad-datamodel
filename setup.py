#!/usr/bin/env python
"""Legacy setup.py for compatibility with older tools."""

from setuptools import setup

# All package metadata is now in pyproject.toml
# This file exists only for backward compatibility
if __name__ == "__main__":
    setup()