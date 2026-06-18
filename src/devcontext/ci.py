# CI/CD integration helpers for DevContext

import os
import json
import subprocess
from pathlib import Path
from typing import Dict, Any, List, Optional


def get_ci_info() -> Dict[str, Any]:
    """Detect CI environment and return info."""
    ci_indicators = {
        "GITHUB_ACTIONS": "github-actions",
        "GITLAB_CI": "gitlab",
        "JENKINS_URL": "jenkins",
        "CIRCLECI": "circleci",
        "TRAVIS": "travis",
        "BITBUCKET_COMMIT": "bitbucket",
        "BUILDKITE": "buildkite",
    }
    
    for env_var, name in ci_indicators.items():
        if os.environ.get(env_var):
            return {
                "ci": name,
                "is_ci": True,
                "commit": os.environ.get("GITHUB_SHA") or os.environ.get("CI_COMMIT_SHA"),
                "branch": os.environ.get("GITHUB_REF_NAME") or os.environ.get("CI_COMMIT_REF_NAME"),
                "url": os.environ.get("GITHUB_URL") or os.environ.get("CI_PIPELINE_URL"),
            }
    
    return {"ci": None, "is_ci": False}


def generate_github_actions_workflow() -> str:
    """Generate GitHub Actions workflow for DevContext."""
    return """name: DevContext CI

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

jobs:
  context:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      
      - name: Install DevContext
        run: pip install devcontext
      
      - name: Generate Context
        run: devcontext generate . -o context.json
      
      - name: Upload Context
        uses: actions/upload-artifact@v4
        with:
          name: codebase-context
          path: context.json
          retention-days: 30
      
      - name: Comment on PR
        if: github.event_name == 'pull_request'
        uses: actions/github-script@v7
        with:
          script: |
            github.rest.issues.createComment({
              issue_number: context.issue.number,
              owner: context.repo.owner,
              repo: context.repo.repo,
              body: '## DevContext Analysis\\n\\nContext generated successfully!\\n\\n[View Context](${{ steps.context.outputs.url }})'
            })
"""


def generate_gitlab_ci_config() -> str:
    """Generate GitLab CI configuration."""
    return """devcontext:
  stage: analyze
  image: python:3.11
  script:
    - pip install devcontext
    - devcontext generate . -o context.json
  artifacts:
    paths:
      - context.json
    expire_in: 1 week
"""


def generate_jenkinsfile() -> str:
    """Generate Jenkinsfile snippet."""
    return '''pipeline {
    agent any
    stages {
        stage('Generate Context') {
            steps {
                sh 'pip install devcontext'
                sh 'devcontext generate . -o context.json'
            }
        }
        stage('Upload Context') {
            steps {
                archiveArtifacts artifacts: 'context.json'
            }
        }
    }
}'''


def run_in_ci() -> bool:
    """Run DevContext in CI and output context."""
    ci_info = get_ci_info()
    
    if not ci_info["is_ci"]:
        print("Not running in CI environment")
        return False
    
    print(f"Running in {ci_info['ci']}")
    
    # Generate context
    try:
        result = subprocess.run(
            ["devcontext", "generate", ".", "-o", "context.json"],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("Context generated successfully")
            
            # Output for CI
            if os.environ.get("GITHUB_ACTIONS"):
                with open("context.json") as f:
                    print(f"::set-output name=context::{f.read()}")
            
            return True
        else:
            print(f"Error: {result.stderr}")
            return False
            
    except FileNotFoundError:
        print("DevContext not installed. Run: pip install devcontext")
        return False


# GitHub Actions specific
def github_actions_post(context: str, repo: str, pr_number: int, token: str):
    """Post context as PR comment in GitHub Actions."""
    import urllib.request
    
    url = f"https://api.github.com/repos/{repo}/issues/{pr_number}/comments"
    
    data = json.dumps({"body": f"## DevContext Context\n\n```json\n{context[:1000]}...\n```"}).encode()
    
    req = urllib.request.Request(
        url,
        data=data,
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        },
        method="POST"
    )
    
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())


if __name__ == "__main__":
    ci = get_ci_info()
    print(f"CI Status: {ci}")
    
    if ci["is_ci"]:
        run_in_ci()