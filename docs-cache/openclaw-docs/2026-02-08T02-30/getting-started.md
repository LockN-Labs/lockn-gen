## Getting Started

Goal: go from zero to a first working chat with minimal setup.
Fastest chat: open the Control UI (no channel setup needed). Run openclaw dashboard
and chat in the browser, or open http://127.0.0.1:18789/ on the
.
Docs: [Dashboard](/web/dashboard) and [Control UI](/web/control-ui).

## Prereqs

- Node 22 or newer

Check your Node version with node --version if you are unsure.

## Quick setup (CLI)

1

Install OpenClaw (recommended)

- macOS/Linux
- Windows (PowerShell)
curl -fsSL https://openclaw.ai/install.sh | bash

iwr -useb https://openclaw.ai/install.ps1 | iex

Other install methods and requirements: [Install](/install).

2

Run the onboarding wizard
openclaw onboard --install-daemon

The wizard configures auth, gateway settings, and optional channels.
See [Onboarding Wizard](/start/wizard) for details.

3

Check the Gateway
If you installed the service, it should already be running:
openclaw gateway status

4

Open the Control UI
openclaw dashboard

If the Control UI loads, your Gateway is ready for use.

## Optional checks and extras

Run the Gateway in the foreground
Useful for quick tests or troubleshooting.
openclaw gateway --port 18789

Send a test message
Requires a configured channel.
openclaw message send --target +15555550123 --message "Hello from OpenClaw"

## Go deeper

## What you will have

- A running Gateway

- Auth configured

- Control UI access or a connected channel

## Next steps

- DM safety and approvals: [Pairing](/channels/pairing)

- Connect more channels: [Channels](/channels)

- Advanced workflows and from source: [Setup](/start/setup)
