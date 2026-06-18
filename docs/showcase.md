# DevContext Showcases

Real-world examples of DevContext usage and results.

## Example 1: Django REST API

### Project Structure
```
my_api/
├── manage.py
├── requirements.txt
├── README.md
├── my_api/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── apps/
│   ├── users/
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── views.py
│   │   ├── serializers.py
│   │   └── urls.py
│   └── products/
│       ├── __init__.py
│       ├── models.py
│       ├── views.py
│       └── serializers.py
└── tests/
    ├── test_users.py
    └── test_products.py
```

### DevContext Output
```json
{
  "tool": "DevContext",
  "version": "0.1.0",
  "summary": {
    "total_files": 15,
    "by_language": {"python": 12, "text": 3}
  },
  "structure": {
    "apps/users/models.py": {
      "classes": ["User", "UserProfile"],
      "functions": ["create_user"]
    },
    "apps/users/views.py": {
      "functions": ["user_list", "user_detail", "user_create"]
    }
  }
}
```

## Example 2: React + TypeScript App

### DevContext Output
```json
{
  "tool": "DevContext",
  "version": "0.1.0",
  "summary": {
    "total_files": 42,
    "by_language": {"typescript": 28, "javascript": 8, "css": 6}
  },
  "structure": {
    "src/App.tsx": {
      "functions": ["App"],
      "classes": []
    },
    "src/components/Button.tsx": {
      "functions": ["Button"],
      "classes": []
    }
  }
}
```

## Example 3: Go Microservice

### DevContext Output
```json
{
  "tool": "DevContext",
  "version": "0.1.0",
  "summary": {
    "total_files": 8,
    "by_language": {"go": 7, "yaml": 1}
  },
  "structure": {
    "main.go": {
      "functions": ["main", "handleRequest"],
      "structs": ["Config", "Handler"]
    },
    "handlers.go": {
      "functions": ["GetUsers", "CreateUser", "DeleteUser"]
    }
  }
}
```

## Success Stories

*Coming soon — share your story!*

If DevContext helped you, please share:
- How you use it
- Time saved
- Any feedback

Open an issue or PR to add your story here.