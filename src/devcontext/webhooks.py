# Webhooks module for DevContext

import json
import hmac
import hashlib
from typing import Dict, Any, List, Optional, Callable
from pathlib import Path


class Webhook:
    """Represents a webhook endpoint."""
    
    def __init__(self, url: str, events: List[str], secret: str = None):
        self.url = url
        self.events = events
        self.secret = secret
    
    def sign_payload(self, payload: str) -> str:
        """Sign webhook payload."""
        if not self.secret:
            return ""
        return hmac.new(
            self.secret.encode(),
            payload.encode(),
            hashlib.sha256
        ).hexdigest()


class WebhookManager:
    """Manage webhook endpoints."""
    
    def __init__(self, config_path: str = None):
        if config_path is None:
            from devcontext.compat import get_cache_dir
            config_path = str(Path(get_cache_dir()) / "webhooks.json")
        
        self.config_path = Path(config_path)
        self.webhooks: List[Webhook] = []
        self._load()
    
    def _load(self):
        """Load webhooks from config."""
        if self.config_path.exists():
            with open(self.config_path) as f:
                data = json.load(f)
            
            for item in data.get("webhooks", []):
                webhook = Webhook(
                    item["url"],
                    item["events"],
                    item.get("secret")
                )
                self.webhooks.append(webhook)
    
    def _save(self):
        """Save webhooks to config."""
        data = {
            "webhooks": [
                {
                    "url": w.url,
                    "events": w.events,
                    "secret": w.secret
                }
                for w in self.webhooks
            ]
        }
        
        self.config_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.config_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    def add(self, url: str, events: List[str], secret: str = None) -> Webhook:
        """Add a webhook."""
        webhook = Webhook(url, events, secret)
        self.webhooks.append(webhook)
        self._save()
        return webhook
    
    def remove(self, url: str) -> bool:
        """Remove a webhook by URL."""
        self.webhooks = [w for w in self.webhooks if w.url != url]
        self._save()
        return True
    
    def list(self) -> List[Dict[str, Any]]:
        """List all webhooks."""
        return [
            {
                "url": w.url,
                "events": w.events,
                "has_secret": w.secret is not None
            }
            for w in self.webhooks
        ]
    
    def trigger(self, event: str, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Trigger webhooks for an event."""
        import urllib.request
        
        results = []
        
        for webhook in self.webhooks:
            if event not in webhook.events:
                continue
            
            payload = json.dumps(data)
            
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "DevContext-Webhook/0.1.0"
            }
            
            if webhook.secret:
                signature = webhook.sign_payload(payload)
                headers["X-DevContext-Signature"] = signature
            
            try:
                req = urllib.request.Request(
                    webhook.url,
                    data=payload.encode(),
                    headers=headers,
                    method="POST"
                )
                
                with urllib.request.urlopen(req, timeout=10) as r:
                    results.append({
                        "url": webhook.url,
                        "status": r.status,
                        "success": True
                    })
            except Exception as e:
                results.append({
                    "url": webhook.url,
                    "error": str(e),
                    "success": False
                })
        
        return results


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Manage DevContext webhooks")
    sub = parser.add_subparsers(dest="command")
    
    add_cmd = sub.add_parser("add", help="Add webhook")
    add_cmd.add_argument("url", help="Webhook URL")
    add_cmd.add_argument("-e", "--events", nargs="+", required=True, help="Events to trigger on")
    add_cmd.add_argument("-s", "--secret", help="Secret for signing")
    
    remove_cmd = sub.add_parser("remove", help="Remove webhook")
    remove_cmd.add_argument("url", help="Webhook URL")
    
    list_cmd = sub.add_parser("list", help="List webhooks")
    
    test_cmd = sub.add_parser("test", help="Test webhook")
    test_cmd.add_argument("url", help="Webhook URL")
    
    args = parser.parse_args()
    
    manager = WebhookManager()
    
    if args.command == "add":
        manager.add(args.url, args.events, args.secret)
        print(f"Added webhook: {args.url}")
    
    elif args.command == "remove":
        manager.remove(args.url)
        print(f"Removed webhook: {args.url}")
    
    elif args.command == "list":
        webhooks = manager.list()
        print(f"Webhooks: {len(webhooks)}")
        for w in webhooks:
            secret = "🔒" if w["has_secret"] else "🔓"
            print(f"  {secret} {w['url']} ({', '.join(w['events'])})")
    
    elif args.command == "test":
        results = manager.trigger("test", {"message": "DevContext test"})
        for r in results:
            if r["success"]:
                print(f"✅ {r['url']}: {r['status']}")
            else:
                print(f"❌ {r['url']}: {r.get('error')}")


if __name__ == "__main__":
    main()