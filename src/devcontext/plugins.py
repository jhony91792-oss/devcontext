# Plugin system for DevContext

import importlib
import os
from pathlib import Path
from typing import Dict, Any, List, Optional, Callable


class Plugin:
    """Base plugin class."""
    
    name: str = "base"
    version: str = "0.1.0"
    
    def on_generate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Called after context generation."""
        return context
    
    def on_format(self, output: str, format_type: str) -> str:
        """Called during formatting."""
        return output
    
    def on_file_analyze(self, filepath: str, info: Dict[str, Any]) -> Dict[str, Any]:
        """Called for each file analyzed."""
        return info


class PluginManager:
    """Manage DevContext plugins."""
    
    def __init__(self):
        self.plugins: List[Plugin] = []
    
    def load_plugin(self, plugin_path: str) -> Optional[Plugin]:
        """Load a plugin from path."""
        try:
            spec = importlib.util.spec_from_file_location("plugin", plugin_path)
            if spec and spec.loader:
                module = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(module)
                
                # Find Plugin class
                for item in dir(module):
                    obj = getattr(module, item)
                    if isinstance(obj, type) and issubclass(obj, Plugin) and obj is not Plugin:
                        return obj()
        except Exception as e:
            print(f"Failed to load plugin {plugin_path}: {e}")
        return None
    
    def load_from_directory(self, plugin_dir: str):
        """Load all plugins from directory."""
        plugin_path = Path(plugin_dir)
        
        if not plugin_path.exists():
            return
        
        for file in plugin_path.glob("*.py"):
            if file.stem.startswith("_"):
                continue
            
            plugin = self.load_plugin(str(file))
            if plugin:
                self.plugins.append(plugin)
                print(f"Loaded plugin: {plugin.name}")
    
    def apply_generate_hooks(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all generate hooks."""
        result = context
        for plugin in self.plugins:
            result = plugin.on_generate(result)
        return result
    
    def apply_format_hooks(self, output: str, format_type: str) -> str:
        """Apply all format hooks."""
        result = output
        for plugin in self.plugins:
            result = plugin.on_format(result, format_type)
        return result


def load_plugins(plugin_dir: str = None) -> PluginManager:
    """Load plugins from directory."""
    if plugin_dir is None:
        plugin_dir = os.path.expanduser("~/.config/devcontext/plugins")
    
    manager = PluginManager()
    manager.load_from_directory(plugin_dir)
    return manager


# Example plugin template
EXAMPLE_PLUGIN = '''
from devcontext.plugins import Plugin

class MyPlugin(Plugin):
    name = "my-plugin"
    version = "0.1.0"
    
    def on_generate(self, context):
        # Modify context here
        context["my_custom_field"] = "added by plugin"
        return context
'''

# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage DevContext plugins")
    sub = parser.add_subparsers(dest="command")
    
    list_cmd = sub.add_parser("list", help="List loaded plugins")
    list_cmd.add_argument("-d", "--dir", help="Plugin directory")
    
    init_cmd = sub.add_parser("init", help="Create example plugin")
    init_cmd.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    if args.command == "list":
        manager = load_plugins(args.dir or "")
        print(f"Loaded plugins: {len(manager.plugins)}")
        for p in manager.plugins:
            print(f"  - {p.name} v{p.version}")
    
    elif args.command == "init":
        output = args.output or "my_plugin.py"
        with open(output, 'w') as f:
            f.write(EXAMPLE_PLUGIN)
        print(f"Example plugin written to {output}")


if __name__ == "__main__":
    main()