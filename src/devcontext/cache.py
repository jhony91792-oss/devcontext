# Cache module for DevContext

import os
import json
import hashlib
import time
from pathlib import Path
from typing import Dict, Any, Optional, List
from datetime import datetime, timedelta


class CacheEntry:
    """Represents a cached item."""
    
    def __init__(self, key: str, value: Any, ttl: int = None):
        self.key = key
        self.value = value
        self.created = time.time()
        self.ttl = ttl  # seconds, None = no expiration
    
    def is_expired(self) -> bool:
        """Check if entry is expired."""
        if self.ttl is None:
            return False
        return (time.time() - self.created) > self.ttl
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary."""
        return {
            "key": self.key,
            "value": self.value,
            "created": self.created,
            "ttl": self.ttl
        }
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CacheEntry":
        """Create from dictionary."""
        entry = cls(data["key"], data["value"], data.get("ttl"))
        entry.created = data.get("created", time.time())
        return entry


class Cache:
    """In-memory cache with optional persistence."""
    
    def __init__(self, max_size: int = 100, persist_path: str = None):
        self.max_size = max_size
        self.persist_path = persist_path
        self._cache: Dict[str, CacheEntry] = {}
        
        if persist_path:
            self._load()
    
    def _load(self):
        """Load cache from disk."""
        if self.persist_path and Path(self.persist_path).exists():
            try:
                with open(self.persist_path) as f:
                    data = json.load(f)
                
                for item in data.get("entries", []):
                    entry = CacheEntry.from_dict(item)
                    if not entry.is_expired():
                        self._cache[entry.key] = entry
            except:
                pass
    
    def _save(self):
        """Save cache to disk."""
        if not self.persist_path:
            return
        
        data = {
            "entries": [e.to_dict() for e in self._cache.values()]
        }
        
        Path(self.persist_path).parent.mkdir(parents=True, exist_ok=True)
        with open(self.persist_path, 'w') as f:
            json.dump(data, f)
    
    def get(self, key: str) -> Optional[Any]:
        """Get value from cache."""
        if key not in self._cache:
            return None
        
        entry = self._cache[key]
        
        if entry.is_expired():
            del self._cache[key]
            return None
        
        return entry.value
    
    def set(self, key: str, value: Any, ttl: int = None):
        """Set value in cache."""
        entry = CacheEntry(key, value, ttl)
        self._cache[key] = entry
        
        # Enforce max size
        if len(self._cache) > self.max_size:
            # Remove oldest
            oldest_key = min(self._cache.keys(), key=lambda k: self._cache[k].created)
            del self._cache[oldest_key]
        
        self._save()
    
    def delete(self, key: str) -> bool:
        """Delete from cache."""
        if key in self._cache:
            del self._cache[key]
            self._save()
            return True
        return False
    
    def clear(self):
        """Clear all cache."""
        self._cache = {}
        self._save()
    
    def keys(self) -> List[str]:
        """Get all cache keys."""
        return list(self._cache.keys())
    
    def size(self) -> int:
        """Get cache size."""
        return len(self._cache)


def generate_cache_key(path: str, format: str = "json", **kwargs) -> str:
    """Generate a cache key for a path."""
    components = [path, format]
    components.extend(f"{k}={v}" for k, v in sorted(kwargs.items()))
    key_string = "|".join(components)
    return hashlib.md5(key_string.encode()).hexdigest()


# CLI
def main():
    import argparse
    parser = argparse.ArgumentParser(description="DevContext cache")
    sub = parser.add_subparsers(dest="command")
    
    list_cmd = sub.add_parser("list", help="List cache entries")
    
    clear_cmd = sub.add_parser("clear", help="Clear cache")
    
    stats_cmd = sub.add_parser("stats", help="Show cache statistics")
    
    args = parser.parse_args()
    
    cache = Cache()
    
    if args.command == "list":
        keys = cache.keys()
        print(f"Cache entries: {len(keys)}")
        for key in keys[:20]:
            print(f"  {key}")
    
    elif args.command == "clear":
        cache.clear()
        print("Cache cleared")
    
    elif args.command == "stats":
        print(f"Cache size: {cache.size()}/{cache.max_size}")


if __name__ == "__main__":
    main()