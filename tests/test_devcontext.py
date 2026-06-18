"""Tests for DevContext."""

import pytest
from pathlib import Path
from devcontext.tree import FileTree, scan_directory
from devcontext.parser import detect_language, extract_structure, parse_file
from devcontext.output import format_json, format_markdown, detect_language_from_path


def test_detect_language():
    """Test language detection."""
    assert detect_language('test.py') == 'python'
    assert detect_language('test.js') == 'javascript'
    assert detect_language('test.ts') == 'typescript'
    assert detect_language('test.go') == 'go'
    assert detect_language('test.rs') == 'rust'
    assert detect_language('test.unknown') == 'unknown'


def test_detect_language_from_path():
    """Test path-based language detection."""
    assert detect_language_from_path('main.py') == 'Python'
    assert detect_language_from_path('index.js') == 'JavaScript'
    assert detect_language_from_path('lib.ts') == 'TypeScript'


def test_extract_structure_python():
    """Test Python code structure extraction."""
    code = '''
def hello():
    """Say hello."""
    print("Hello")

class Greeter:
    def __init__(self, name):
        self.name = name
    
    def greet(self):
        return f"Hi, {self.name}!"

def goodbye():
    pass
'''
    result = extract_structure(code, 'python')
    assert 'hello' in result['functions']
    assert 'Greeter' in result['classes']
    assert len(result['functions']) == 2


def test_extract_structure_go():
    """Test Go code structure extraction."""
    code = '''
package main

import "fmt"

func main() {
    fmt.Println("Hello")
}

type Person struct {
    Name string
}

func (p Person) Greet() string {
    return "Hi, " + p.Name
}
'''
    result = extract_structure(code, 'go')
    assert 'main' in result['functions']
    assert 'Person' in result['structs']


def test_file_tree_basic(tmp_path):
    """Test file tree generation with basic structure."""
    # Create test files
    (tmp_path / "README.md").write_text("# Test Project")
    (tmp_path / "main.py").write_text("print('hello')")
    subdir = tmp_path / "src"
    subdir.mkdir()
    (subdir / "utils.py").write_text("def helper(): pass")
    
    tree = FileTree(tmp_path)
    nodes = tree.scan()
    
    paths = [n['path'] for n in nodes]
    assert any('README.md' in p for p in paths)
    assert any('main.py' in p for p in paths)
    assert any('src/' in p and 'utils.py' in p for p in paths)


def test_file_tree_skip_dirs(tmp_path):
    """Test that skip directories are excluded."""
    (tmp_path / "main.py").write_text("print('hello')")
    (tmp_path / "__pycache__").mkdir()
    ((tmp_path / "__pycache__") / "cache.pyc").write_text("fake")
    (tmp_path / "node_modules").mkdir()
    ((tmp_path / "node_modules") / "pkg").write_text("fake")
    
    tree = FileTree(tmp_path)
    nodes = tree.scan()
    paths = [n['path'] for n in nodes]
    
    assert any('main.py' in p for p in paths)
    assert not any('__pycache__' in p for p in paths)
    assert not any('node_modules' in p for p in paths)


def test_scan_directory(tmp_path):
    """Test scan_directory convenience function."""
    (tmp_path / "main.py").write_text("def main(): pass")
    (tmp_path / "utils").mkdir()
    ((tmp_path / "utils") / "__init__.py").write_text("")
    
    nodes = scan_directory(tmp_path)
    assert len(nodes) > 0


def test_parse_file_python(tmp_path):
    """Test parsing a Python file."""
    code = '''
"""Example module."""

def add(a, b):
    """Add two numbers."""
    return a + b

class Calculator:
    """Simple calculator."""
    
    def multiply(self, x, y):
        return x * y
'''
    test_file = tmp_path / "calc.py"
    test_file.write_text(code)
    
    result = parse_file(test_file)
    
    assert result['language'] == 'python'
    assert 'add' in result['functions']
    assert 'Calculator' in result['classes']
    assert result['lines'] > 5


def test_parse_file_creates_structure(tmp_path):
    """Test that parse_file returns proper structure."""
    test_file = tmp_path / "test.py"
    test_file.write_text("def foo(): pass\ndef bar(): pass\n")
    
    result = parse_file(test_file)
    
    assert 'path' in result
    assert 'language' in result
    assert 'functions' in result
    assert 'classes' in result
    assert 'lines' in result


def test_format_json(tmp_path):
    """Test JSON output formatting."""
    data = {
        'version': '0.1.0',
        'project': {'name': 'test'},
        'file_tree': [],
    }
    
    output = format_json(data)
    assert '"version"' in output
    assert '"project"' in output


def test_format_markdown(tmp_path):
    """Test Markdown output formatting."""
    data = {
        'version': '0.1.0',
        'project': {'name': 'test', 'file_count': 5},
        'file_tree': [
            {'path': 'main.py', 'type': 'file', 'depth': 0},
            {'path': 'utils/', 'type': 'dir', 'depth': 0},
        ],
    }
    
    output = format_markdown(data)
    assert '#' in output
    assert 'main.py' in output
    assert 'DevContext' in output


def test_format_markdown_with_structure(tmp_path):
    """Test Markdown output with code structure."""
    data = {
        'version': '0.1.0',
        'structure': {
            'main.py': {
                'language': 'python',
                'functions': ['main', 'init'],
                'classes': ['App'],
                'imports': ['os', 'sys'],
            }
        }
    }
    
    output = format_markdown(data)
    assert 'main.py' in output
    assert 'main' in output
    assert 'App' in output


def test_multiple_files_parsing(tmp_path):
    """Test parsing multiple files."""
    files = [
        ('main.py', 'def main(): pass\nclass App: pass'),
        ('utils.py', 'def helper(): pass\nclass Helper: pass'),
        ('config.py', 'DEBUG = True\n'),
    ]
    
    for fname, content in files:
        (tmp_path / fname).write_text(content)
    
    nodes = scan_directory(tmp_path)
    parsed_count = 0
    for node in nodes:
        if node['type'] == 'file':
            fpath = tmp_path / node['path']
            result = parse_file(fpath)
            if 'functions' in result:
                parsed_count += 1
    
    assert parsed_count == 3