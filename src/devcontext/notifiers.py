# Notification system for DevContext

import json
import smtplib
import ssl
from email.mime.text import MIMEText
from typing import Dict, Any, List, Optional
from pathlib import Path


class NotificationChannel:
    """Base notification channel."""
    
    def send(self, message: str, **kwargs) -> bool:
        raise NotImplementedError


class EmailChannel(NotificationChannel):
    """Email notification channel."""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str, use_tls: bool = True):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
        self.use_tls = use_tls
    
    def send(self, message: str, to: str, subject: str = "DevContext Notification") -> bool:
        """Send email notification."""
        try:
            msg = MIMEText(message, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email send failed: {e}")
            return False


class SlackChannel(NotificationChannel):
    """Slack webhook notification channel."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(self, message: str, **kwargs) -> bool:
        """Send Slack notification."""
        import urllib.request
        
        try:
            payload = json.dumps({"text": message}).encode()
            
            req = urllib.request.Request(
                self.webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status == 200
        except Exception as e:
            print(f"Slack send failed: {e}")
            return False


class DiscordChannel(NotificationChannel):
    """Discord webhook notification channel."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def send(self, message: str, **kwargs) -> bool:
        """Send Discord notification."""
        import urllib.request
        
        try:
            payload = json.dumps({"content": message}).encode()
            
            req = urllib.request.Request(
                self.webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status == 200
        except Exception as e:
            print(f"Discord send failed: {e}")
            return False


class Notifier:
    """Notification manager."""
    
    def __init__(self):
        self.channels: List[NotificationChannel] = []
    
    def add_email(self, smtp_server: str, smtp_port: int, username: str, password: str) -> EmailChannel:
        """Add email channel."""
        channel = EmailChannel(smtp_server, smtp_port, username, password)
        self.channels.append(channel)
        return channel
    
    def add_slack(self, webhook_url: str) -> SlackChannel:
        """Add Slack channel."""
        channel = SlackChannel(webhook_url)
        self.channels.append(channel)
        return channel
    
    def add_discord(self, webhook_url: str) -> DiscordChannel:
        """Add Discord channel."""
        channel = DiscordChannel(webhook_url)
        self.channels.append(channel)
        return channel
    
    def notify(self, message: str, **kwargs) -> Dict[str, bool]:
        """Send notification to all channels."""
        results = {}
        
        for i, channel in enumerate(self.channels):
            try:
                if isinstance(channel, EmailChannel):
                    results[f"email"] = channel.send(message, to=kwargs.get("to", ""))
                else:
                    results[f"channel_{i}"] = channel.send(message)
            except Exception as e:
                results[f"channel_{i}"] = False
        
        return results


def create_notifier_from_config(config_path: str = None) -> Notifier:
    """Create notifier from config file."""
    if config_path is None:
        from devcontext.compat import get_config_dir
        config_path = str(Path(get_config_dir()) / "notifications.json")
    
    notifier = Notifier()
    
    if Path(config_path).exists():
        with open(config_path) as f:
            config = json.load(f)
        
        if "email" in config:
            email_cfg = config["email"]
            notifier.add_email(
                email_cfg["smtp_server"],
                email_cfg["smtp_port"],
                email_cfg["username"],
                email_cfg["password"]
            )
        
        if "slack" in config:
            notifier.add_slack(config["slack"]["webhook_url"])
        
        if "discord" in config:
            notifier.add_discord(config["discord"]["webhook_url"])
    
    return notifier


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext notifications")
    sub = parser.add_subparsers(dest="command")
    
    test_cmd = sub.add_parser("test", help="Test notifications")
    test_cmd.add_argument("-t", "--to", help="Email recipient")
    
    send_cmd = sub.add_parser("send", help="Send notification")
    send_cmd.add_argument("message", help="Message to send")
    send_cmd.add_argument("-t", "--to", help="Email recipient")
    
    args = parser.parse_args()
    
    notifier = create_notifier_from_config()
    
    if args.command == "test":
        results = notifier.notify("DevContext test notification")
        for channel, success in results.items():
            print(f"{'✅' if success else '❌'} {channel}")
    
    elif args.command == "send":
        results = notifier.notify(args.message, to=args.to)
        for channel, success in results.items():
            print(f"{'✅' if success else '❌'} {channel}")


if __name__ == "__main__":
    main()