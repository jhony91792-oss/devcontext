"""Tests for DevContext."""

import pytest
from pathlib import Path
from devcontext.cli import get_file_tree, extract_key_content, generate_context


def test_get_file_tree(tmp_path):
    """Test file tree generation."""
    # Create a minimal test structure
    (tmp_path / "README.md").write_text("# Test")
    (tmp_path / "main.py").write_text("print('hello')")
    
    tree = get_file_tree(tmp_path)
    paths = [f["path"] for f in tree]
    
    assert any("README.md" in p for p in paths)
    assert any("main.py" in p for p in paths)


def test_generate_context(tmp_path):
    """Test context generation."""
    (tmp_path / "README.md").write_text("# My Project")
    (tmp_path / "main.py").write_text("def main(): pass")
    
    ctx = generate_context(tmp_path)
    
    assert ctx["tool"] == "DevContext"
    assert ctx["version"] == "0.1.0"
    assert "file_tree" in ctx
    assert "key_content" in ctx