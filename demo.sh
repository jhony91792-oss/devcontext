#!/bin/bash
# DevContext Demo Script
# Shows how DevContext works with a sample project

set -e

echo "=========================================="
echo "DevContext Demo"
echo "=========================================="
echo ""

# Create a sample project
DEMO_DIR=$(mktemp -d)
echo "📁 Creating demo project in $DEMO_DIR"

mkdir -p "$DEMO_DIR/src"
mkdir -p "$DEMO_DIR/tests"

# Create sample Python files
cat > "$DEMO_DIR/README.md" << 'EOF'
# Demo Project

A sample project to demonstrate DevContext.
EOF

cat > "$DEMO_DIR/main.py" << 'EOF'
"""Main application module."""

import sys
from src.auth import login, logout
from src.database import Database

def main():
    """Entry point."""
    db = Database()
    user = login(sys.argv[1], sys.argv[2])
    print(f"Welcome, {user.name}!")
    logout(user)

if __name__ == "__main__":
    main()
EOF

cat > "$DEMO_DIR/src/__init__.py" << 'EOF'
"""Source package."""
EOF

cat > "$DEMO_DIR/src/auth.py" << 'EOF'
"""Authentication module."""

class User:
    """User class."""
    
    def __init__(self, name, email):
        self.name = name
        self.email = email
    
    def is_admin(self):
        return self.email.endswith('@admin.com')

def login(username, password):
    """Authenticate user."""
    if username and password:
        return User(username, f"{username}@example.com")
    raise ValueError("Invalid credentials")

def logout(user):
    """Log out user."""
    print(f"Goodbye, {user.name}")
EOF

cat > "$DEMO_DIR/src/database.py" << 'EOF'
"""Database module."""

class Database:
    """Simple database wrapper."""
    
    def __init__(self, path=":memory:"):
        self.path = path
        self.connected = True
    
    def query(self, sql):
        """Execute SQL query."""
        return []
    
    def close(self):
        self.connected = False
EOF

cat > "$DEMO_DIR/tests/test_auth.py" << 'EOF'
"""Tests for auth module."""

def test_login():
    user = login("test", "pass")
    assert user.name == "test"

def test_user_is_admin():
    user = User("admin", "admin@admin.com")
    assert user.is_admin() == True
EOF

echo ""
echo "📋 Sample project created:"
echo ""

# Show tree
echo "Project structure:"
find "$DEMO_DIR" -type f -name "*.py" -o -name "*.md" | while read f; do
    echo "  $f"
done

echo ""
echo "🚀 Running devcontext..."
echo ""

# Run devcontext
cd "$DEMO_DIR"
python3 -c "
import sys
sys.path.insert(0, '/home/node/devcontext/src')
from devcontext.cli import generate_context
from pathlib import Path
import json

ctx = generate_context(Path('.'))
print(json.dumps(ctx['summary'], indent=2))
"

echo ""
echo "✅ Demo complete!"
echo ""
echo "Try it yourself:"
echo "  pip install devcontext"
echo "  devcontext generate ."
echo ""

# Cleanup
rm -rf "$DEMO_DIR"