# Tailscale + Caddy Security Review (dev.lockn.ai)

Date: 2026-02-06

## Scope
Proposed private dev setup:
- Tailscale mesh (100.x.y.z) for private network access
- Caddy reverse proxy for `dev.lockn.ai`
- Caddy binds only to Tailscale interface
- Upstream services: LockN Score API (:8000) and Web (:3000)

This review assesses security posture, risks, best practices, certificate strategy, alternatives, and provides a recommendation.

---

## 1) Security assessment
**Overall:** Sound approach for a private dev environment when paired with strong Tailscale ACLs and minimal host exposure. Binding Caddy to the Tailscale interface drastically reduces public attack surface. Primary risks shift to Tailscale identity/ACL configuration, endpoint hygiene, and app-layer security (auth, CSRF, etc.).

**Strengths**
- **Private-by-default exposure:** Services are not on the public internet.
- **Identity-based access:** Tailscale uses device + user identity, enabling tight ACL controls.
- **Single ingress point:** Caddy can centralize TLS, headers, auth, and logging.

**Primary residual risks**
- **Misconfigured ACLs** or tailnet sharing could broaden access.
- **Compromised tailnet device** could reach services if ACLs are too permissive.
- **App-layer flaws** (auth bypass, CSRF, SSRF) are still exploitable by any allowed tailnet client.

---

## 2) Attack vectors / risks
1. **ACL misconfiguration:** `* -> *` or overly broad groups allow unintended access.
2. **Tailnet compromise or device loss:** A stolen device or malware on an allowed client can access services.
3. **DNS exposure:** If `dev.lockn.ai` is public DNS pointing to the Tailnet IP, it leaks nothing by itself but signals the service name. If pointing to a public IP, exposure risk increases.
4. **Host network exposure:** If the host has other listening services on 0.0.0.0, those are still reachable from non-Tailscale networks.
5. **Reverse proxy misroutes:** Incorrect Caddy upstream routing could expose internal admin endpoints.
6. **Web app vulnerabilities:** Auth, session management, CORS/CSRF, SSRF can be abused by any allowed tailnet member.
7. **WebSocket/HTTP2 upgrade handling:** If misconfigured, could allow proxy bypass or broken origin checks.

---

## 3) Best practices for Tailscale ACLs
**Goal:** Least privilege per user/group, per service, per port.

**Recommendations**
- **Use groups** (e.g., `devs`, `ops`) and avoid `*` in ACLs.
- **Limit ports**: Allow only 443 (Caddy) or specific service ports if needed.
- **Use tags** for service nodes (e.g., `tag:dev-web`) and restrict who can access them.
- **Deny by default:** Use the smallest allow list that meets needs.
- **Use device posture / autogroup** if available (e.g., `autogroup:admin` sparingly).
- **Shorten session lifetimes** and enable **device approval** and **key expiry**.
- **Enable 2FA** on Tailscale identity provider.
- **Disable tailnet sharing** unless explicitly required.

**Example ACL sketch**
```json
{
  "groups": {
    "group:devs": ["alice@company.com", "bob@company.com"],
    "group:ops": ["ops@company.com"]
  },
  "tagOwners": {
    "tag:dev-web": ["group:ops"],
    "tag:dev-api": ["group:ops"]
  },
  "acls": [
    {"action": "accept", "src": ["group:devs"], "dst": ["tag:dev-web:443", "tag:dev-api:443"]}
  ]
}
```

---

## 4) Caddy hardening recommendations
1. **Bind to Tailscale only**
   - Use `bind` directive to restrict listener to `100.x.x.x` or `tailscale0` interface.
2. **Disable public listeners**
   - Ensure no `:80` or `:443` on `0.0.0.0`.
3. **Headers**
   - Set security headers (HSTS if appropriate for dev, CSP if feasible, X-Content-Type-Options, Referrer-Policy).
4. **Access logs**
   - Enable and ship logs to detect unexpected access patterns.
5. **Upstream timeouts**
   - Configure proxy timeouts to prevent resource exhaustion.
6. **Admin API**
   - Disable or restrict Caddy admin API (`admin off` or bind to localhost).
7. **mTLS (optional)**
   - If you want additional protection, enable mTLS between Caddy and clients; but Tailscale already provides identity-layer security.
8. **Rate limiting (optional)**
   - Prevent brute force, but for private dev might be low priority.

---

## 5) Certificate handling
**Option A: Caddy auto-HTTPS (ACME)**
- **Pros:** Standard public CA, works seamlessly with browsers.
- **Cons:** Requires public DNS and validation (HTTP-01 or DNS-01). If Caddy is bound only to Tailscale, HTTP-01 won’t work. DNS-01 can work with provider creds.

**Option B: Tailscale HTTPS certs (`tailscale cert`)**
- **Pros:** Easy for tailnet-only hostnames (`*.ts.net`). No public exposure required.
- **Cons:** Not valid for arbitrary public domains like `dev.lockn.ai` unless using Tailscale-managed MagicDNS names.

**Option C: Internal CA / self-signed**
- **Pros:** No external dependencies.
- **Cons:** Requires cert trust distribution to clients.

**Recommendation:**
- If `dev.lockn.ai` must be used, prefer **DNS-01 ACME** with Caddy and bind-only-to-tailscale.
- If okay with `dev-*.ts.net`, use **Tailscale certs** for simplicity.

---

## 6) Alternative approaches considered
1. **Pure Tailscale + Serve**
   - Tailscale’s `serve`/`funnel` can publish services with auth and HTTPS built-in. Good for small setups but less flexible than Caddy.
2. **SSH-based reverse tunnels**
   - E.g., `ssh -R` to a bastion. More manual, weaker identity management.
3. **Cloudflare Tunnel + Access**
   - Strong access controls and SSO. But exposes services publicly (behind access gate) and adds third-party dependency.
4. **WireGuard + Nginx**
   - Similar to Tailscale but more ops-heavy.

---

## 7) Final recommendation
**Use Tailscale + Caddy, but lock it down**:
- **Bind Caddy to Tailscale interface only.**
- **Use tight ACLs** with groups/tags and port restrictions.
- **Prefer DNS-01 ACME** for `dev.lockn.ai` while staying private.
- **Monitor logs** and restrict host services.

This provides strong isolation for dev environments without exposing ports to the public internet, provided ACLs and device hygiene are solid.

---

## Specific questions
**Is binding Caddy to Tailscale IP sufficient isolation?**
- **Mostly yes**, for network-level exposure. It prevents public internet access. However, **ACLs and device security** still matter. A compromised tailnet device is still inside.

**Should we use Tailscale’s built-in HTTPS (tailscale cert)?**
- Only if you’re OK using Tailscale-managed hostnames (`*.ts.net`). For `dev.lockn.ai`, use Caddy + DNS-01 ACME.

**Any concerns with WebSocket proxying?**
- Caddy handles WebSockets transparently via `reverse_proxy`, but ensure:
  - **Origin checks** in the app if needed.
  - **Timeouts** are set to avoid idle connections hanging.
  - **Auth/session** validation on WS endpoints (don’t assume private network = trusted).

---

## Summary
This architecture is **secure by default** when combined with least-privilege ACLs and a locked-down Caddy config. Primary risks are **ACL sprawl** and **compromised tailnet devices**, not public exposure. For certs, **DNS-01 ACME** is best for `dev.lockn.ai`; **Tailscale certs** are ideal only for `.ts.net` names. Bind-only-to-tailscale is good isolation, but not a substitute for access controls and app-layer security.
