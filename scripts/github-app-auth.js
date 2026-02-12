#!/usr/bin/env node
/**
 * GitHub App Authentication Helper
 * Generates JWT and installation tokens for LockN GitHub Apps
 */

const crypto = require('crypto');
const fs = require('fs');
const path = require('path');

// App configurations from environment
const APPS = {
  architect: {
    id: process.env.GITHUB_APP_LOCKN_ARCHITECT_ID,
    keyPath: process.env.GITHUB_APP_LOCKN_ARCHITECT_KEY
  },
  coder: {
    id: process.env.GITHUB_APP_LOCKN_CODER_ID,
    keyPath: process.env.GITHUB_APP_LOCKN_CODER_KEY
  },
  devops: {
    id: process.env.GITHUB_APP_LOCKN_DEVOPS_ID,
    keyPath: process.env.GITHUB_APP_LOCKN_DEVOPS_KEY
  },
  orchestrator: {
    id: process.env.GITHUB_APP_LOCKN_ORCHESTRATOR_ID,
    keyPath: process.env.GITHUB_APP_LOCKN_ORCHESTRATOR_KEY
  },
  qa: {
    id: process.env.GITHUB_APP_LOCKN_QA_ID,
    keyPath: process.env.GITHUB_APP_LOCKN_QA_KEY
  }
};

/**
 * Generate JWT for GitHub App authentication
 */
function generateJWT(appId, privateKeyPath) {
  const privateKey = fs.readFileSync(privateKeyPath, 'utf8');
  
  const now = Math.floor(Date.now() / 1000);
  const payload = {
    iat: now,
    exp: now + 600, // 10 minutes
    iss: appId
  };
  
  const header = Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })).toString('base64url');
  const body = Buffer.from(JSON.stringify(payload)).toString('base64url');
  const signingInput = `${header}.${body}`;
  
  const signature = crypto.createSign('RSA-SHA256')
    .update(signingInput)
    .sign(privateKey, 'base64url');
  
  return `${signingInput}.${signature}`;
}

/**
 * Get installation token using JWT
 */
async function getInstallationToken(jwt, installationId) {
  const response = await fetch(`https://api.github.com/app/installations/${installationId}/access_tokens`, {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${jwt}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  
  return response.json();
}

/**
 * List installations for an app
 */
async function listInstallations(jwt) {
  const response = await fetch('https://api.github.com/app/installations', {
    headers: {
      'Authorization': `Bearer ${jwt}`,
      'Accept': 'application/vnd.github.v3+json'
    }
  });
  
  if (!response.ok) {
    throw new Error(`HTTP ${response.status}: ${await response.text()}`);
  }
  
  return response.json();
}

// CLI interface
async function main() {
  const command = process.argv[2];
  const appName = process.argv[3];
  
  if (!command || !appName) {
    console.log('Usage: node github-app-auth.js <command> <app-name>');
    console.log('Commands: jwt, installations, token');
    console.log('Apps: architect, coder, devops, orchestrator, qa');
    process.exit(1);
  }
  
  const app = APPS[appName];
  if (!app || !app.id) {
    console.error(`Unknown app: ${appName}`);
    process.exit(1);
  }
  
  try {
    switch (command) {
      case 'jwt':
        const jwt = generateJWT(app.id, app.keyPath);
        console.log(jwt);
        break;
        
      case 'installations':
        const jwt2 = generateJWT(app.id, app.keyPath);
        const installations = await listInstallations(jwt2);
        console.log(JSON.stringify(installations, null, 2));
        break;
        
      case 'token':
        const installationId = process.argv[4];
        if (!installationId) {
          console.error('Usage: token <app-name> <installation-id>');
          process.exit(1);
        }
        const jwt3 = generateJWT(app.id, app.keyPath);
        const tokenData = await getInstallationToken(jwt3, installationId);
        console.log(tokenData.token);
        break;
        
      default:
        console.error(`Unknown command: ${command}`);
        process.exit(1);
    }
  } catch (err) {
    console.error(`Error: ${err.message}`);
    process.exit(1);
  }
}

if (require.main === module) {
  main();
}

module.exports = { generateJWT, getInstallationToken, listInstallations };
