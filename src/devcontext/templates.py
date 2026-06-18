# Templates for common project structures

TEMPLATES = {
    "python-cli": {
        "name": "Python CLI Application",
        "description": "Template for a Python CLI tool like devcontext",
        "structure": {
            "src/{package}/__init__.py": "Package init",
            "src/{package}/cli.py": "CLI entry point",
            "src/{package}/core.py": "Core functionality",
            "tests/test_{package}.py": "Tests",
            "pyproject.toml": "Project config",
            "README.md": "Documentation",
        }
    },
    "javascript-lib": {
        "name": "JavaScript Library",
        "description": "Template for a JavaScript/TypeScript library",
        "structure": {
            "src/index.ts": "Main entry",
            "src/{lib}.ts": "Library code",
            "tests/{lib}.test.ts": "Tests",
            "package.json": "Package config",
            "README.md": "Documentation",
        }
    },
    "web-app": {
        "name": "Web Application",
        "description": "Template for a web application",
        "structure": {
            "src/index.html": "HTML entry",
            "src/app.js": "Main app code",
            "src/styles.css": "Styles",
            "package.json": "Dependencies",
            "README.md": "Documentation",
        }
    }
}


def get_template(name: str) -> dict:
    """Get template by name."""
    return TEMPLATES.get(name)


def list_templates() -> list:
    """List all available templates."""
    return [
        {"name": name, **template}
        for name, template in TEMPLATES.items()
    ]


def apply_template(template_name: str, package_name: str = "mypackage") -> dict:
    """Apply template with package name substitution."""
    template = get_template(template_name)
    if not template:
        return None
    
    result = {}
    for path, content in template["structure"].items():
        # Replace {package} placeholder
        path = path.replace("{package}", package_name)
        # Replace {lib} with package name (lowercase, no spaces)
        lib_name = package_name.lower().replace("-", "").replace("_", "")
        path = path.replace("{lib}", lib_name)
        result[path] = content
    
    return result