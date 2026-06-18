# Notifiers module for DevContext - Slack/Discord/PagerDuty integrations

import os
import json
import subprocess
from typing import Dict, Any, Optional, List


class NotificationError(Exception):
    """Notification sending error."""
    pass


class BaseNotifier:
    """Base class for notifiers."""
    
    def send(self, message: str, **kwargs) -> bool:
        """Send notification. Override in subclass."""
        raise NotImplementedError


class SlackNotifier(BaseNotifier):
    """Send notifications to Slack."""
    
    def __init__(self, webhook_url: Optional[str] = None, 
                 default_channel: str = "#devcontext"):
        self.webhook_url = webhook_url or os.environ.get("SLACK_WEBHOOK_URL")
        self.default_channel = default_channel
    
    def send(self, message: str, channel: Optional[str] = None,
             username: str = "DevContext Bot",
             icon_emoji: str = ":robot_face:") -> bool:
        """Send Slack message."""
        if not self.webhook_url:
            raise NotificationError("Slack webhook URL not configured")
        
        payload = {
            "text": message,
            "username": username,
            "icon_emoji": icon_emoji
        }
        
        if channel or self.default_channel:
            payload["channel"] = channel or self.default_channel
        
        try:
            cmd = [
                "curl", "-s", "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload),
                self.webhook_url
            ]
            result = subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise NotificationError(f"Failed to send Slack notification: {e}")


class DiscordNotifier(BaseNotifier):
    """Send notifications to Discord."""
    
    def __init__(self, webhook_url: Optional[str] = None):
        self.webhook_url = webhook_url or os.environ.get("DISCORD_WEBHOOK_URL")
    
    def send(self, message: str, 
             username: str = "DevContext",
             avatar_url: Optional[str] = None) -> bool:
        """Send Discord message."""
        if not self.webhook_url:
            raise NotificationError("Discord webhook URL not configured")
        
        payload = {
            "content": message,
            "username": username
        }
        
        if avatar_url:
            payload["avatar_url"] = avatar_url
        
        try:
            cmd = [
                "curl", "-s", "-X", "POST",
                "-H", "Content-Type: application/json",
                "-d", json.dumps(payload),
                self.webhook_url
            ]
            result = subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise NotificationError(f"Failed to send Discord notification: {e}")


class EmailNotifier(BaseNotifier):
    """Send notifications via email."""
    
    def __init__(self, smtp_host: str = "localhost", 
                 smtp_port: int = 587,
                 smtp_user: Optional[str] = None,
                 smtp_password: Optional[str] = None,
                 from_addr: str = "devcontext@example.com"):
        self.smtp_host = smtp_host
        self.smtp_port = smtp_port
        self.smtp_user = smtp_user or os.environ.get("SMTP_USER")
        self.smtp_password = smtp_password or os.environ.get("SMTP_PASSWORD")
        self.from_addr = from_addr
    
    def send(self, message: str, to_addr: str,
             subject: str = "DevContext Notification") -> bool:
        """Send email notification."""
        import smtplib
        from email.mime.text import MIMEText
        from email.mime.multipart import MIMEMultipart
        
        if not self.smtp_user or not self.smtp_password:
            raise NotificationError("SMTP credentials not configured")
        
        msg = MIMEMultipart()
        msg["From"] = self.from_addr
        msg["To"] = to_addr
        msg["Subject"] = subject
        msg.attach(MIMEText(message, "plain"))
        
        try:
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_user, self.smtp_password)
                server.send_message(msg)
            return True
        except Exception as e:
            raise NotificationError(f"Failed to send email: {e}")


class WebhookNotifier(BaseNotifier):
    """Send notifications to generic webhook."""
    
    def __init__(self, webhook_url: str, 
                 headers: Optional[Dict[str, str]] = None):
        self.webhook_url = webhook_url
        self.headers = headers or {}
    
    def send(self, message: str, **kwargs) -> bool:
        """Send webhook notification."""
        payload = {
            "text": message,
            **kwargs
        }
        
        try:
            cmd = [
                "curl", "-s", "-X", "POST",
                "-H", f"Content-Type: application/json",
                "-H", *[f"{k}: {v}" for k, v in self.headers.items()],
                "-d", json.dumps(payload),
                self.webhook_url
            ]
            result = subprocess.run(cmd, capture_output=True, check=True)
            return True
        except subprocess.CalledProcessError as e:
            raise NotificationError(f"Failed to send webhook notification: {e}")


def notify_stars_update(old_count: int, new_count: int, 
                        repo_url: str) -> bool:
    """Notify about star count update."""
    if new_count <= old_count:
        return False
    
    diff = new_count - old_count
    message = f"⭐ DevContext gained {diff} new star(s)! Total: {new_count}\n{repo_url}"
    
    # Try Slack first
    try:
        notifier = SlackNotifier()
        notifier.send(message)
        return True
    except NotificationError:
        pass
    
    # Try Discord
    try:
        notifier = DiscordNotifier()
        notifier.send(message)
        return True
    except NotificationError:
        pass
    
    return False