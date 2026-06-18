# API client for programmatic DevContext usage

import json
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional, List


class DevContextClient:
    """Python client for DevContext CLI."""
    
    def __init__(self, binary: str = "devcontext", default_options: Optional[Dict] = None):
        self.binary = binary
        self.default_options = default_options or {}
    
    def _run(self, args: List[str], input_path: Optional[str] = None) -> str:
        """Run devcontext command and return output."""
        cmd = [self.binary] + args
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                check=True,
                input=input_path,
                cwd=self.default_options.get("cwd")
            )
            return result.stdout
        except subprocess.CalledProcessError as e:
            raise DevContextError(f"Command failed: {e.stderr}")
    
    def generate(self, path: str = ".", format: str = "json", 
                 include_stats: bool = True, **kwargs) -> Dict[str, Any]:
        """Generate context for a codebase."""
        args = ["generate", path, "--format", format]
        
        if not include_stats:
            args.append("--no-stats")
        
        for key, value in kwargs.items():
            args.extend([f"--{key}", str(value)])
        
        output = self._run(args)
        
        if format == "json":
            return json.loads(output)
        return output
    
    def tree(self, path: str = ".", max_depth: int = 5, **kwargs) -> str:
        """Get file tree for a codebase."""
        args = ["tree", path, "--max-depth", str(max_depth)]
        
        for key, value in kwargs.items():
            args.extend([f"--{key}", str(value)])
        
        return self._run(args)
    
    def parse(self, file_path: str, **kwargs) -> Dict[str, Any]:
        """Parse a single file."""
        args = ["parse", file_path]
        
        for key, value in kwargs.items():
            args.extend([f"--{key}", str(value)])
        
        output = self._run(args)
        return json.loads(output)
    
    def diff(self, old: str, new: str, format: str = "summary") -> str:
        """Compare two contexts."""
        args = ["diff", old, new, "--format", format]
        return self._run(args)


class DevContextError(Exception):
    """DevContext-specific error."""
    pass


# Alternative: Direct import (for when devcontext is installed as package)
def generate_context(path: str = ".", **kwargs) -> Dict[str, Any]:
    """
    Generate context directly using the module.
    
    Usage:
        from devcontext.api_client import generate_context
        context = generate_context("./myproject")
    """
    import devcontext
    
    options = {
        "path": path,
        **kwargs
    }
    
    # Use CLI for full functionality
    client = DevContextClient()
    return client.generate(**options)


# Async client for concurrent operations
import concurrent.futures


class AsyncDevContextClient(DevContextClient):
    """Async version of DevContextClient."""
    
    def generate_async(self, paths: List[str], **kwargs) -> Dict[str, str]:
        """Generate context for multiple paths concurrently."""
        results = {}
        
        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = {
                executor.submit(self.generate, path, **kwargs): path 
                for path in paths
            }
            
            for future in concurrent.futures.as_completed(futures):
                path = futures[future]
                try:
                    results[path] = future.result()
                except DevContextError as e:
                    results[path] = {"error": str(e)}
        
        return results


# Plugin system for extending DevContext
class DevContextPlugin:
    """Base class for DevContext plugins."""
    
    name = "base_plugin"
    version = "0.1.0"
    
    def on_context_generated(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Called after context is generated. Return modified context."""
        return context
    
    def on_file_scanned(self, file_info: Dict[str, Any]) -> Dict[str, Any]:
        """Called for each file scanned. Return modified file info."""
        return file_info


class PluginManager:
    """Manage DevContext plugins."""
    
    def __init__(self):
        self.plugins: List[DevContextPlugin] = []
    
    def register(self, plugin: DevContextPlugin):
        """Register a plugin."""
        self.plugins.append(plugin)
    
    def unregister(self, plugin_name: str):
        """Unregister a plugin by name."""
        self.plugins = [p for p in self.plugins if p.name != plugin_name]
    
    def apply_context_generated(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply all plugins to generated context."""
        result = context
        for plugin in self.plugins:
            result = plugin.on_context_generated(result)
        return result


# Global plugin manager
_plugin_manager: Optional[PluginManager] = None


def get_plugin_manager() -> PluginManager:
    """Get global plugin manager."""
    global _plugin_manager
    if _plugin_manager is None:
        _plugin_manager = PluginManager()
    return _plugin_manager