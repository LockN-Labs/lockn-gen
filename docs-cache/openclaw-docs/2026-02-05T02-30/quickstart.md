# Quick start

## Install

- npm
- pnpm
npm install -g openclaw@latest

pnpm add -g openclaw@latest

## Onboard and run the Gateway

1

2

3

After onboarding, the Gateway runs via the user service. You can still run it manually with openclaw gateway.

## From source (development)

git clone https://github.com/openclaw/openclaw.git
cd openclaw
pnpm install
pnpm ui:build # auto-installs UI deps on first run
pnpm build
openclaw onboard --install-daemon

If you do not have a global install yet, run onboarding via pnpm openclaw ... from the repo.

## Multi instance quickstart (optional)

OPENCLAW_CONFIG_PATH=~/.openclaw/a.json \
OPENCLAW_STATE_DIR=~/.openclaw-a \
openclaw gateway --port 19001

## Send a test message

Requires a running Gateway.
openclaw message send --target +15555550123 --message "Hello from OpenClaw"
