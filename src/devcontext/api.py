# API server module for DevContext

import json
from typing import Dict, Any, Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class DevContextAPI:
    """REST API for DevContext."""
    
    def __init__(self, port: int = 8080):
        self.port = port
        self.context_cache: Dict[str, Any] = {}
    
    def generate(self, path: str = ".") -> Dict[str, Any]:
        """Generate context."""
        from devcontext import DevContext
        
        dc = DevContext(path)
        return dc.generate()
    
    def handle_request(self, method: str, path: str, data: Dict[str, Any] = None) -> Dict[str, Any]:
        """Handle API request."""
        if path == "/generate":
            target_path = data.get("path", ".") if data else "."
            return self.generate(target_path)
        
        elif path == "/health":
            return {"status": "ok", "version": "0.1.0"}
        
        elif path == "/stats":
            return {
                "files": len(self.context_cache),
                "cache_size": sum(len(str(v)) for v in self.context_cache.values())
            }
        
        return {"error": "Unknown endpoint"}


class APIHandler(BaseHTTPRequestHandler):
    """HTTP request handler."""
    
    api: Optional[DevContextAPI] = None
    
    def do_GET(self):
        """Handle GET requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        if path == "/health":
            self.send_json({"status": "ok", "version": "0.1.0"})
        else:
            self.send_json({"error": "Not found"}, 404)
    
    def do_POST(self):
        """Handle POST requests."""
        parsed = urlparse(self.path)
        path = parsed.path
        
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length) if content_length > 0 else b"{}"
        
        try:
            data = json.loads(body)
        except:
            data = {}
        
        result = self.api.handle_request("POST", path, data) if self.api else {"error": "No API"}
        
        self.send_json(result)
    
    def send_json(self, data: Dict[str, Any], status: int = 200):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())


def start_server(port: int = 8080):
    """Start API server."""
    api = DevContextAPI(port)
    APIHandler.api = api
    
    server = HTTPServer(("0.0.0.0", port), APIHandler)
    print(f"DevContext API server running on port {port}")
    print(f"  GET  /health - Health check")
    print(f"  POST /generate - Generate context")
    
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
        server.shutdown()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext API server")
    parser.add_argument("-p", "--port", type=int, default=8080, help="Port to listen on")
    
    args = parser.parse_args()
    
    start_server(args.port)


if __name__ == "__main__":
    main()