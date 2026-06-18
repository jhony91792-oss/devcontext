# Banner module for DevContext - ASCII banners

from typing import Optional


BANNERS = {
    "default": """
╔══════════════════════════════════════╗
║       DevContext v0.1.0              ║
║  Generate AI-ready context           ║
╚══════════════════════════════════════╝
""",
    
    "mini": """
  DevContext v0.1.0
  ================
""",
    
    "full": """
╭───────────────────────────────────────╮
│  ███████╗██╗   ██╗ ██████╗ ██████╗   │
│  ██╔════╝██║   ██║██╔═══██╗██╔══██╗  │
│  ███████╗██║   ██║██║   ██║██████╔╝  │
│  ╚════██║██║   ██║██║   ██║██╔══██╗  │
│  ███████║╚██████╔╝╚██████╔╝██║  ██║  │
│  ╚══════╝ ╚═════╝  ╚═════╝ ╚═╝  ╚═╝  │
│                                       │
│  Context Generator for AI             │
╰───────────────────────────────────────╯
"""
}


def get_banner(name: str = "default") -> str:
    """Get a banner by name."""
    return BANNERS.get(name, BANNERS["default"])


def print_banner(name: str = "default"):
    """Print a banner."""
    print(get_banner(name))


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Display DevContext banner")
    parser.add_argument("-n", "--name", choices=list(BANNERS.keys()), default="default")
    
    args = parser.parse_args()
    print_banner(args.name)


if __name__ == "__main__":
    main()