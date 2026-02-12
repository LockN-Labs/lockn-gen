#!/usr/bin/env python3
"""
GitHub App authentication and admin operations for LockN agents.
"""

import jwt
import time
import requests
import json
import sys
from pathlib import Path
from typing import Optional, Dict, Any

KEYS_DIR = Path("/home/sean/keys")

APP_IDS = {
    'coder': 2816646,
    'qa': 2816677,
    'architect': 2816706,
    'devops': 2816768,
    'orchestrator': 2816797,
}


class GitHubAppAuth:
    """Authenticate as a GitHub App and get installation tokens."""
    
    def __init__(self, app_name: str):
        self.app_name = app_name
        self.app_id = APP_IDS.get(app_name)
        if not self.app_id:
            raise ValueError(f"Unknown app: {app_name}. Valid: {list(APP_IDS.keys())}")
        
        self.key_file = KEYS_DIR / f"lockn-{app_name}.2026-02-07.private-key.pem"
        if not self.key_file.exists():
            raise FileNotFoundError(f"Key file not found: {self.key_file}")
        
        self._jwt = None
        self._jwt_expires = 0
        self._installation_tokens: Dict[str, tuple] = {}  # org -> (token, expires)
    
    def get_jwt(self) -> str:
        """Get or refresh the app JWT."""
        now = int(time.time())
        if self._jwt and now < self._jwt_expires - 60:
            return self._jwt
        
        with open(self.key_file, 'r') as f:
            private_key = f.read()
        
        payload = {
            'iat': now - 60,
            'exp': now + (10 * 60),
            'iss': self.app_id
        }
        
        self._jwt = jwt.encode(payload, private_key, algorithm='RS256')
        self._jwt_expires = now + (10 * 60)
        return self._jwt
    
    def get_installations(self) -> list:
        """List all installations of this app."""
        headers = {
            'Authorization': f'Bearer {self.get_jwt()}',
            'Accept': 'application/vnd.github+json'
        }
        resp = requests.get('https://api.github.com/app/installations', headers=headers)
        resp.raise_for_status()
        return resp.json()
    
    def get_installation_id(self, org: str) -> Optional[int]:
        """Get installation ID for an organization."""
        installations = self.get_installations()
        for inst in installations:
            if inst.get('account', {}).get('login') == org:
                return inst['id']
        return None
    
    def get_installation_token(self, org: str) -> str:
        """Get an installation access token for an organization."""
        now = int(time.time())
        
        # Check cache
        if org in self._installation_tokens:
            token, expires = self._installation_tokens[org]
            if now < expires - 60:
                return token
        
        # Get installation ID
        inst_id = self.get_installation_id(org)
        if not inst_id:
            raise ValueError(f"App not installed on {org}. Install at: "
                           f"https://github.com/apps/lockn-{self.app_name}/installations/select_target")
        
        # Get new token
        headers = {
            'Authorization': f'Bearer {self.get_jwt()}',
            'Accept': 'application/vnd.github+json'
        }
        resp = requests.post(
            f'https://api.github.com/app/installations/{inst_id}/access_tokens',
            headers=headers
        )
        resp.raise_for_status()
        data = resp.json()
        
        token = data['token']
        # Tokens expire in 1 hour
        self._installation_tokens[org] = (token, now + 3600)
        return token


def post_status(app_name: str, repo: str, sha: str, state: str, 
                description: str, context: Optional[str] = None, org: str = "LockN-Labs"):
    """Post a commit status check."""
    auth = GitHubAppAuth(app_name)
    token = auth.get_installation_token(org)
    
    context = context or f"LockN {app_name.title()}"
    
    resp = requests.post(
        f'https://api.github.com/repos/{repo}/statuses/{sha}',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github+json'
        },
        json={
            'state': state,
            'description': description,
            'context': context
        }
    )
    resp.raise_for_status()
    return resp.json()


def create_check_run(app_name: str, repo: str, head_sha: str, name: str,
                     status: str = "completed", conclusion: str = "success",
                     summary: str = "", org: str = "LockN-Labs"):
    """Create a check run (richer than status)."""
    auth = GitHubAppAuth(app_name)
    token = auth.get_installation_token(org)
    
    resp = requests.post(
        f'https://api.github.com/repos/{repo}/check-runs',
        headers={
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github+json'
        },
        json={
            'name': name,
            'head_sha': head_sha,
            'status': status,
            'conclusion': conclusion,
            'output': {
                'title': name,
                'summary': summary
            }
        }
    )
    resp.raise_for_status()
    return resp.json()


# CLI interface
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: gh_admin.py <command> [args...]")
        print("Commands: jwt, token, installations")
        sys.exit(1)
    
    cmd = sys.argv[1]
    
    if cmd == "jwt":
        app_id = int(sys.argv[2])
        key_file = sys.argv[3]
        
        now = int(time.time())
        with open(key_file, 'r') as f:
            private_key = f.read()
        
        payload = {'iat': now - 60, 'exp': now + (10 * 60), 'iss': app_id}
        token = jwt.encode(payload, private_key, algorithm='RS256')
        print(token)
    
    elif cmd == "token":
        app_id = int(sys.argv[2])
        key_file = sys.argv[3]
        org = sys.argv[4] if len(sys.argv) > 4 else "LockN-Labs"
        
        # Find app name from ID
        app_name = next((k for k, v in APP_IDS.items() if v == app_id), None)
        if not app_name:
            print(f"Unknown app ID: {app_id}", file=sys.stderr)
            sys.exit(1)
        
        auth = GitHubAppAuth(app_name)
        try:
            token = auth.get_installation_token(org)
            print(token)
        except ValueError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
    
    elif cmd == "installations":
        app_id = int(sys.argv[2])
        key_file = sys.argv[3]
        
        app_name = next((k for k, v in APP_IDS.items() if v == app_id), None)
        auth = GitHubAppAuth(app_name)
        installations = auth.get_installations()
        
        for inst in installations:
            print(f"{inst['account']['login']}: {inst['id']}")
    
    else:
        print(f"Unknown command: {cmd}", file=sys.stderr)
        sys.exit(1)
