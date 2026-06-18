# Template engine for DevContext

import os
import json
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable


class Template:
    """A context template."""
    
    def __init__(self, name: str, description: str, template: Dict[str, Any]):
        self.name = name
        self.description = description
        self.template = template
    
    def render(self, context: Dict[str, Any]) -> str:
        """Render template with context."""
        output = self.description + "\n\n"
        
        meta = context.get("metadata", {})
        files = context.get("files", {})
        
        output += f"# {meta.get('name', 'Project')}\n\n"
        output += f"Files: {meta.get('total_files', len(files))}\n"
        output += f"Languages: {', '.join(meta.get('languages', []))}\n\n"
        
        output += "## Structure\n"
        
        for path in sorted(files.keys())[:20]:
            output += f"- `{path}`\n"
        
        if len(files) > 20:
            output += f"\n... and {len(files) - 20} more files\n"
        
        return output


BUILT_IN_TEMPLATES = {
    "minimal": Template(
        "minimal",
        "Minimal context for quick AI prompts",
        {"max_files": 10, "include_functions": True}
    ),
    "standard": Template(
        "standard", 
        "Standard context for general use",
        {"max_files": 50, "include_functions": True, "include_classes": True}
    ),
    "detailed": Template(
        "detailed",
        "Detailed context with full analysis",
        {"max_files": 100, "include_all": True}
    ),
    "ai": Template(
        "ai",
        "Optimized for AI assistants (ChatGPT, Claude)",
        {"compact": True, "max_files": 30, "include_docstrings": True}
    )
}


class TemplateManager:
    """Manage context templates."""
    
    def __init__(self):
        self.templates = dict(BUILT_IN_TEMPLATES)
        self._load_custom()
    
    def _load_custom(self):
        """Load custom templates from config."""
        from devcontext.compat import get_config_dir
        config_dir = Path(get_config_dir())
        custom_templates = config_dir / "templates.json"
        
        if custom_templates.exists():
            with open(custom_templates) as f:
                data = json.load(f)
            
            for name, item in data.items():
                self.templates[name] = Template(
                    item["name"],
                    item.get("description", ""),
                    item.get("template", {})
                )
    
    def save_custom(self, name: str, template: Template):
        """Save a custom template."""
        from devcontext.compat import get_config_dir
        config_dir = Path(get_config_dir())
        config_dir.mkdir(parents=True, exist_ok=True)
        
        custom_templates = config_dir / "templates.json"
        
        data = {}
        if custom_templates.exists():
            with open(custom_templates) as f:
                data = json.load(f)
        
        data[name] = {
            "name": template.name,
            "description": template.description,
            "template": template.template
        }
        
        with open(custom_templates, 'w') as f:
            json.dump(data, f, indent=2)
        
        self.templates[name] = template
    
    def list(self) -> List[Dict[str, str]]:
        """List all templates."""
        return [
            {"name": t.name, "description": t.description}
            for t in self.templates.values()
        ]
    
    def get(self, name: str) -> Optional[Template]:
        """Get a template by name."""
        return self.templates.get(name)
    
    def render(self, name: str, context: Dict[str, Any]) -> Optional[str]:
        """Render a template with context."""
        template = self.get(name)
        if template:
            return template.render(context)
        return None


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage context templates")
    sub = parser.add_subparsers(dest="command")
    
    list_cmd = sub.add_parser("list", help="List templates")
    
    get_cmd = sub.add_parser("get", help="Get template")
    get_cmd.add_argument("name", help="Template name")
    
    create_cmd = sub.add_parser("create", help="Create template")
    create_cmd.add_argument("name", help="Template name")
    create_cmd.add_argument("description", help="Template description")
    
    render_cmd = sub.add_parser("render", help="Render template")
    render_cmd.add_argument("name", help="Template name")
    render_cmd.add_argument("input", help="Context JSON file")
    
    args = parser.parse_args()
    
    manager = TemplateManager()
    
    if args.command == "list":
        templates = manager.list()
        print("Available templates:")
        for t in templates:
            print(f"  {t['name']}: {t['description']}")
    
    elif args.command == "get":
        template = manager.get(args.name)
        if template:
            print(f"Name: {template.name}")
            print(f"Description: {template.description}")
            print(f"Template: {json.dumps(template.template, indent=2)}")
        else:
            print(f"Template '{args.name}' not found")
    
    elif args.command == "create":
        template = Template(args.name, args.description, {})
        manager.save_custom(args.name, template)
        print(f"Template '{args.name}' created")
    
    elif args.command == "render":
        with open(args.input) as f:
            context = json.load(f)
        
        output = manager.render(args.name, context)
        if output:
            print(output)
        else:
            print(f"Template '{args.name}' not found")


if __name__ == "__main__":
    main()