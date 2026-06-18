# DevContext __init__.py

"""
DevContext - Generate AI-ready context from codebases.

A CLI tool that generates comprehensive context from codebases
in seconds, making it easy to share with AI assistants.

Usage:
    from devcontext import DevContext
    
    dc = DevContext(".")
    context = dc.generate()
"""

__version__ = "0.1.0"
__author__ = "DevContext Team"
__license__ = "MIT"

from devcontext.devcontext import DevContext

__all__ = ["DevContext", "__version__"]