# Caching functionality for DevContext

import os
import json
import hashlib
import time
from pathlib import Path
from typing import Optional, Dict, Any


class ContextCache:
    """Cache generated context to avoid regenerating unchanged codebases."""
    
    def __init__(self, cache_dir: Optional[str] = None):
        if cache_dir is None:
            cache_dir = Path.home() / ".cache" / "devcontext"
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(parents=True, exist_ok=True)
    
    def _get_cache_key(self, path: str, options: Dict[str, Any]) -> str:
        """Generate cache key from path and options."""
        key_data = json.dumps({
            "path": str(Path(path).resolve()),
            "options": options
        }, sort_keys=True)
        return hashlib.sha256(key_data.encode()).hexdigest()[:16]
    
    def _get_cache_path(self, key: str) -> Path:
        """Get path for cache file."""
        return self.cache_dir / f"{key}.json"
    
    def get(self, path: str, options: Dict[str, Any], max_age: int = 3600) -> Optional[Dict]:
        """Get cached context if valid."""
        key = self._get_cache_key(path, options)
        cache_path = self._get_cache_path(key)
        
        if not cache_path.exists():
            return None
        
        # Check age
        age = time.time() - cache_path.stat().st_mtime
        if age > max_age:
            return None
        
        try:
            with open(cache_path) as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError):
            return None
    
    def set(self, path: str, options: Dict[str, Any], context: Dict) -> bool:
        """Save context to cache."""
        key = self._get_cache_key(path, options)
        cache_path = self._get_cache_path(key)
        
        try:
            with open(cache_path, 'w') as f:
                json.dump(context, f)
            return True
        except OSError:
            return False
    
    def invalidate(self, path: str, options: Dict[str, Any]) -> bool:
        """Remove cached context."""
        key = self._get_cache_key(path, options)
        cache_path = self._get_cache_path(key)
        
        if cache_path.exists():
            cache_path.unlink()
            return True
        return False
    
    def clear(self) -> int:
        """Clear all cached entries. Returns count of cleared entries."""
        count = 0
        for cache_file in self.cache_dir.glob("*.json"):
            cache_file.unlink()
            count += 1
        return count
    
    def size(self) -> int:
        """Get total cache size in bytes."""
        total = 0
        for cache_file in self.cache_dir.glob("*.json"):
            total += cache_file.stat().st_size
        return total
    
    def prune(self, max_age: int = 86400) -> int:
        """Remove cache entries older than max_age seconds."""
        count = 0
        now = time.time()
        
        for cache_file in self.cache_dir.glob("*.json"):
            age = now - cache_file.stat().st_mtime
            if age > max_age:
                cache_file.unlink()
                count += 1
        
        return count


# Global cache instance
_cache: Optional[ContextCache] = None


def get_cache() -> ContextCache:
    """Get global cache instance."""
    global _cache
    if _cache is None:
        _cache = ContextCache()
    return _cache


def cached_generate(path: str, options: Dict[str, Any], generator_func) -> Dict:
    """Generate context with caching."""
    cache = get_cache()
    
    # Try cache first
    cached = cache.get(path, options)
    if cached is not None:
        return cached
    
    # Generate fresh
    context = generator_func()
    
    # Save to cache
    cache.set(path, options, context)
    
    return context