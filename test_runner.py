#!/usr/bin/env python3
"""Test runner for DevContext - no pytest needed."""

import sys
import os
import tempfile
from pathlib import Path

# Find src directory relative to this script
script_dir = Path(__file__).parent.resolve()
src_path = script_dir / 'src'
sys.path.insert(0, str(src_path))
os.chdir(script_dir)

from devcontext.tree import FileTree, scan_directory
from devcontext.parser import detect_language, extract_structure, parse_file
from devcontext.output import format_json, format_markdown, format_compact

print("=" * 50)
print("DevContext Test Suite")
print("=" * 50)

passed = 0
failed = 0

def test(name, cond):
    global passed, failed
    if cond:
        print(f"✅ {name}")
        passed += 1
    else:
        print(f"❌ {name}")
        failed += 1

# Test language detection
test("Python detection", detect_language('test.py') == 'python')
test("JavaScript detection", detect_language('test.js') == 'javascript')
test("TypeScript detection", detect_language('test.ts') == 'typescript')
test("Go detection", detect_language('test.go') == 'go')
test("Rust detection", detect_language('test.rs') == 'rust')
test("Unknown detection", detect_language('test.xyz') == 'unknown')

# Test parser
code = '''
def hello():
    return "Hi"

class Greeter:
    def greet(self, name):
        return f"Hello, {name}!"

def goodbye():
    pass
'''
result = extract_structure(code, 'python')
test("Function extraction", 'hello' in result['functions'] and 'goodbye' in result['functions'])
test("Class extraction", 'Greeter' in result['classes'])

# Test tree
with tempfile.TemporaryDirectory() as tmp:
    tmp_path = Path(tmp)
    (tmp_path / "README.md").write_text("# Test")
    (tmp_path / "main.py").write_text("print('hello')")
    subdir = tmp_path / "src"
    subdir.mkdir()
    (subdir / "utils.py").write_text("def helper(): pass")
    
    tree = FileTree(tmp_path)
    nodes = tree.scan()
    paths = [n['path'] for n in nodes]
    test("Finds README.md", any('README.md' in p for p in paths))
    test("Finds main.py", any('main.py' in p for p in paths))
    test("Finds nested src/utils.py", any('utils.py' in p for p in paths))
    test("Skips __pycache__", not any('__pycache__' in p for p in paths))

# Test output
data = {'version': '0.1.0', 'project': {'name': 'test', 'file_count': 5}}
json_out = format_json(data)
test("JSON output contains version", '"version"' in json_out)
md_out = format_markdown(data)
test("Markdown output contains DevContext", 'DevContext' in md_out)

print()
print("=" * 50)
print(f"Results: {passed} passed, {failed} failed")
print("=" * 50)

sys.exit(0 if failed == 0 else 1)