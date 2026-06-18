# Banner generator for DevContext - creates ASCII/text banners

from typing import Tuple


def create_banner(text: str, width: int = 60, char: str = "=") -> str:
    """Create a simple text banner."""
    lines = [
        char * width,
        centered_text(text, width),
        char * width,
    ]
    return "\n".join(lines)


def centered_text(text: str, width: int) -> str:
    """Center text within width."""
    if len(text) >= width:
        return text[:width]
    padding = (width - len(text)) // 2
    return " " * padding + text


def create_ascii_art(text: str) -> str:
    """Create ASCII art banner."""
    fonts = {
        "big": _ASCII_BIG,
        "small": _ASCII_SMALL,
    }
    
    # Simple block letters
    lines = ["", text.upper(), ""]
    
    result = []
    result.append("```")
    result.append(create_banner("", 50, "─"))
    result.append(create_banner(text.upper(), 50, " "))
    result.append(create_banner("DevContext CLI", 50, " "))
    result.append(create_banner("", 50, "─"))
    result.append("```")
    
    return "\n".join(result)


def create_shields_badge(label: str, value: str, color: str = "green") -> str:
    """Create a shields.io badge."""
    return f"![{label}](https://img.shields.io/badge/{label}-{value}-{color})"


def create_github_badge(label: str, link: str) -> str:
    """Create GitHub-style badge."""
    return f"[![{label}](https://img.shields.io/github/stars/jhony91792-oss/devcontext?style=social)]({link})"


def generate_readme_badges() -> str:
    """Generate standard badges for README."""
    badges = [
        "![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)",
        "![License](https://img.shields.io/badge/License-MIT-green.svg)",
        "![PyPI](https://img.shields.io/badge/PyPI-v0.1.0-orange.svg)",
        "![CI](https://img.shields.io/badge/CI-Passing-brightgreen.svg)",
        "![Stars](https://img.shields.io/github/stars/jhony91792-oss/devcontext?style=social)",
        "![Forks](https://img.shields.io/github/forks/jhony91792-oss/devcontext?style=social)",
    ]
    return " | ".join(badges)


def generate_banner_full(name: str = "DevContext") -> str:
    """Generate full ASCII banner."""
    return f"""
╔══════════════════════════════════════════════════════════╗
║                                                          ║
║   ██████╗ ███████╗███╗   ███╗                             ║
║  ██╔═══██╗██╔════╝████╗ ████║                             ║
║  ██║   ██║█████╗  ██╔████╔██║  {name:^20}       ║
║  ██║   ██║██╔══╝  ██║╚██╔╝██║                             ║
║  ╚██████╔╝██║     ██║ ╚═╝ ██║                             ║
║   ╚═════╝ ╚═╝     ╚═╝     ╚═╝                             ║
║                                                          ║
║   AI-Ready Context Generation in 3 Seconds               ║
║                                                          ║
╚══════════════════════════════════════════════════════════╝
"""


_ASCII_BIG = {
    "D": [
        "███████╗",
        "██╔════╝",
        "██║     ",
        "██║     ",
        "██║     ",
        "██╔════╝",
        "███████╗",
    ]
}

_ASCII_SMALL = {
    "D": ["███", "█  █", "█  █", "█  █", "█  █", "███"]
}


# SVG banner generator
def generate_svg_banner(width: int = 800, height: int = 200) -> str:
    """Generate SVG banner image."""
    return f'''<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">
  <rect fill="#24292e" width="{width}" height="{height}" rx="10"/>
  <text x="{width//2}" y="80" font-family="Arial" font-size="48" fill="white" text-anchor="middle" font-weight="bold">DevContext</text>
  <text x="{width//2}" y="130" font-family="Arial" font-size="20" fill="#a0a0a0" text-anchor="middle">AI-Ready Context in 3 Seconds</text>
  <text x="{width//2}" y="170" font-family="monospace" font-size="16" fill="#4caf50" text-anchor="middle">pip install devcontext</text>
</svg>'''


if __name__ == "__main__":
    print(generate_banner_full())