# Share module for DevContext - share context via various channels

import json
import smtplib
import ssl
from email.mime.text import MIMEText
from typing import Dict, Any, List, Optional
from urllib.request import Request, urlopen


class ShareChannel:
    """Base share channel."""
    
    def share(self, content: str, **kwargs) -> bool:
        raise NotImplementedError


class EmailShare(ShareChannel):
    """Share via email."""
    
    def __init__(self, smtp_server: str, smtp_port: int, username: str, password: str):
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.username = username
        self.password = password
    
    def share(self, content: str, to: str, subject: str = "DevContext Share", **kwargs) -> bool:
        """Share via email."""
        try:
            msg = MIMEText(content, 'plain', 'utf-8')
            msg['Subject'] = subject
            msg['From'] = self.username
            msg['To'] = to
            
            context = ssl.create_default_context()
            
            with smtplib.SMTP_SSL(self.smtp_server, self.smtp_port, context=context) as server:
                server.login(self.username, self.password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Email share failed: {e}")
            return False


class WebhookShare(ShareChannel):
    """Share via webhook."""
    
    def __init__(self, webhook_url: str):
        self.webhook_url = webhook_url
    
    def share(self, content: str, **kwargs) -> bool:
        """Share via webhook."""
        try:
            payload = json.dumps({"content": content}).encode()
            
            req = Request(
                self.webhook_url,
                data=payload,
                headers={"Content-Type": "application/json"}
            )
            
            with urlopen(req, timeout=10) as r:
                return r.status == 200
        except Exception as e:
            print(f"Webhook share failed: {e}")
            return False


class FileShare(ShareChannel):
    """Share via file."""
    
    def share(self, content: str, path: str = "context.txt", **kwargs) -> bool:
        """Save to file."""
        try:
            with open(path, 'w') as f:
                f.write(content)
            return True
        except Exception as e:
            print(f"File share failed: {e}")
            return False


class ShareManager:
    """Manage sharing channels."""
    
    def __init__(self):
        self.channels: List[ShareChannel] = []
    
    def add_email(self, smtp_server: str, smtp_port: int, username: str, password: str) -> EmailShare:
        """Add email channel."""
        channel = EmailShare(smtp_server, smtp_port, username, password)
        self.channels.append(channel)
        return channel
    
    def add_webhook(self, webhook_url: str) -> WebhookShare:
        """Add webhook channel."""
        channel = WebhookShare(webhook_url)
        self.channels.append(channel)
        return channel
    
    def add_file(self, path: str) -> FileShare:
        """Add file channel."""
        channel = FileShare()
        # Store path for later use
        return channel
    
    def share(self, content: str, **kwargs) -> Dict[str, bool]:
        """Share content via all channels."""
        results = {}
        
        for i, channel in enumerate(self.channels):
            name = type(channel).__name__
            try:
                if isinstance(channel, FileShare):
                    results[name] = channel.share(content, path=kwargs.get("path", "context.txt"))
                elif isinstance(channel, EmailShare):
                    results[name] = channel.share(content, to=kwargs.get("to", ""))
                else:
                    results[name] = channel.share(content)
            except Exception as e:
                results[name] = False
        
        return results


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="Share DevContext output")
    parser.add_argument("content", help="Content to share")
    parser.add_argument("-t", "--to", help="Email recipient")
    parser.add_argument("-s", "--subject", default="DevContext Share", help="Email subject")
    parser.add_argument("-o", "--output", help="Output file")
    
    args = parser.parse_args()
    
    share = ShareManager()
    
    if args.output:
        channel = FileShare()
        if channel.share(args.content, args.output):
            print(f"✅ Saved to {args.output}")
        else:
            print(f"❌ Failed to save")
    
    if args.to:
        # Use Gmail
        channel = EmailShare("smtp.gmail.com", 465, "jhony91792@gmail.com", "veum tkuk almg rolx")
        if channel.share(args.content, args.to, args.subject):
            print(f"✅ Sent to {args.to}")
        else:
            print(f"❌ Failed to send")


if __name__ == "__main__":
    main()