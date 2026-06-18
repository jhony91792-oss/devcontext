# Autoupdate module for DevContext

import os
import sys
import json
import subprocess
from pathlib import Path
from typing import Optional, Dict, Any
from datetime import datetime


class UpdateChecker:
    """Check for DevContext updates."""
    
    PYPI_URL = "https://pypi.org/pypi/devcontext/json"
    GITHUB_RELEASES = "https://api.github.com/repos/jhony91792-oss/devcontext/releases"
    
    def __init__(self, current_version: str = "0.1.0"):
        self.current_version = current_version
    
    def check_pypi(self) -> Optional[Dict[str, Any]]:
        """Check latest version on PyPI."""
        try:
            import urllib.request
            req = urllib.request.Request(self.PYPI_URL)
            with urllib.request.urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
                latest = data['info']['version']
                return {
                    "latest": latest,
                    "current": self.current_version,
                    "outdated": self._compare_versions(latest) > 0
                }
        except Exception:
            return None
    
    def _compare_versions(self, latest: str) -> int:
        """Compare versions. Returns: -1 if current < latest, 0 if equal, 1 if newer."""
        from packaging import version
        try:
            if version.parse(self.current_version) < version.parse(latest):
                return -1
            elif version.parse(self.current_version) > version.parse(latest):
                return 1
            return 0
        except Exception:
            return 0
    
    def check_github(self) -> Optional[Dict[str, Any]]:
        """Check GitHub releases."""
        try:
            import urllib.request
            token = os.environ.get("GITHUB_TOKEN", "")
            headers = {
                "User-Agent": "DevContext/1.0",
                "Accept": "application/vnd.github+json"
            }
            if token:
                headers["Authorization"] = f"Bearer {token}"
            
            req = urllib.request.Request(self.GITHUB_RELEASES, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as r:
                releases = json.loads(r.read())
                if releases:
                    latest = releases[0]
                    return {
                        "tag": latest.get("tag_name"),
                        "name": latest.get("name"),
                        "url": latest.get("html_url"),
                        "published": latest.get("published_at")
                    }
        except Exception:
            pass
        return None
    
    def get_update_info(self) -> Dict[str, Any]:
        """Get complete update information."""
        return {
            "current_version": self.current_version,
            "pypi": self.check_pypi(),
            "github": self.check_github(),
            "checked_at": datetime.now().isoformat()
        }


def check_for_updates() -> bool:
    """Check if updates are available. Returns True if update needed."""
    checker = UpdateChecker()
    info = checker.get_update_info()
    
    pypi = info.get("pypi")
    if pypi and pypi.get("outdated"):
        print(f"Update available: {pypi['latest']} (current: {pypi['current']})")
        return True
    
    return False


def install_update() -> bool:
    """Install latest update from PyPI."""
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "--upgrade", "devcontext"],
            check=True
        )
        return True
    except subprocess.CalledProcessError:
        return False


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Check for DevContext updates")
    parser.add_argument("--check", action="store_true", help="Check for updates")
    parser.add_argument("--install", action="store_true", help="Install latest version")
    
    args = parser.parse_args()
    
    checker = UpdateChecker()
    
    if args.check or (not args.check and not args.install):
        info = checker.get_update_info()
        print(f"Current version: {info['current_version']}")
        
        pypi = info.get('pypi')
        if pypi:
            if pypi.get('outdated'):
                print(f"⚠️ Update available: {pypi['latest']}")
            else:
                print("✅ You have the latest version")
        
        github = info.get('github')
        if github:
            print(f"Latest GitHub release: {github.get('tag')}")
    
    if args.install:
        print("Installing update...")
        if install_update():
            print("✅ Update installed!")
        else:
            print("❌ Update failed")


if __name__ == "__main__":
    main()