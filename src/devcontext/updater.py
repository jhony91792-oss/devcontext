# Updater module for DevContext - check for updates

import os
import json
import subprocess
from typing import Dict, Any, Optional
from urllib.request import Request, urlopen


class Updater:
    """Check for and apply updates."""
    
    def __init__(self, package_name: str = "devcontext"):
        self.package_name = package_name
        self.current_version = "0.1.0"
    
    def get_current_version(self) -> str:
        """Get current installed version."""
        try:
            result = subprocess.run(
                ["devcontext", "--version"],
                capture_output=True,
                text=True,
                timeout=5
            )
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
        
        return self.current_version
    
    def get_latest_version(self) -> Optional[str]:
        """Get latest version from PyPI."""
        try:
            req = Request(
                f"https://pypi.org/pypi/{self.package_name}/json",
                headers={"User-Agent": "DevContext/0.1.0"}
            )
            
            with urlopen(req, timeout=10) as r:
                data = json.loads(r.read())
            
            return data["info"]["version"]
        except:
            return None
    
    def check_update(self) -> Dict[str, Any]:
        """Check if update is available."""
        current = self.get_current_version()
        latest = self.get_latest_version()
        
        if not latest:
            return {
                "update_available": False,
                "error": "Could not fetch latest version"
            }
        
        # Simple version comparison
        update_available = current != latest
        
        return {
            "update_available": update_available,
            "current_version": current,
            "latest_version": latest
        }
    
    def update(self) -> bool:
        """Update to latest version."""
        try:
            result = subprocess.run(
                ["pip", "install", "--upgrade", self.package_name],
                capture_output=True,
                text=True
            )
            return result.returncode == 0
        except:
            return False


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext updater")
    sub = parser.add_subparsers(dest="command")
    
    check_cmd = sub.add_parser("check", help="Check for updates")
    check_cmd.add_argument("-j", "--json", action="store_true")
    
    update_cmd = sub.add_parser("update", help="Update to latest version")
    
    args = parser.parse_args()
    
    updater = Updater()
    
    if args.command == "check":
        result = updater.check_update()
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            if result.get("update_available"):
                print(f"⚠️  Update available: {result['current_version']} → {result['latest_version']}")
            else:
                print(f"✅ You're running the latest version: {result['current_version']}")
    
    elif args.command == "update":
        print("Updating...")
        if updater.update():
            print("✅ Update complete")
        else:
            print("❌ Update failed")


if __name__ == "__main__":
    main()