# Auth Guard Skill

## Purpose
Standard error handling patterns for LockN Labs auth flows. Prevents silent auth failures from cascading into full outages.

## Core Principle: Never Swallow Auth Errors

The 2026-02-10 incident proved that silent `catch + redirect` is the worst pattern for auth flows. When Auth0 Actions SDK mismatches cause empty roles, the error must be **visible**, not hidden.

## Standard Error Handling Pattern

### 1. Auth0 Action Error Handling (Server-Side)

```javascript
// ❌ ANTI-PATTERN: Silent catch that caused the 2026-02-10 incident
exports.onExecutePostLogin = async (event, api) => {
  try {
    const roles = event.authorization?.roles || [];
    api.idToken.setCustomClaim('https://lockn.app/roles', roles);
  } catch (e) {
    // Silent failure → roles empty → all users denied
    console.log('role assignment skipped');
  }
};

// ✅ CORRECT: Fail loud, deny explicitly with reason
exports.onExecutePostLogin = async (event, api) => {
  try {
    const roles = event.authorization?.roles || [];
    
    if (roles.length === 0) {
      // Log structured alert — this is detectable by monitoring
      console.error(JSON.stringify({
        level: 'error',
        event: 'auth.roles_empty',
        userId: event.user.user_id,
        sdk_version: process.env.AUTH0_ACTION_SDK_VERSION || 'unknown',
        timestamp: new Date().toISOString()
      }));
      // Deny with a clear message, not a silent redirect
      api.access.deny('Role assignment failed. Contact support. Ref: AUTH-ROLES-EMPTY');
      return;
    }
    
    api.idToken.setCustomClaim('https://lockn.app/roles', roles);
    api.accessToken.setCustomClaim('https://lockn.app/roles', roles);
  } catch (error) {
    console.error(JSON.stringify({
      level: 'critical',
      event: 'auth.action_error',
      error: error.message,
      stack: error.stack,
      userId: event.user?.user_id,
      timestamp: new Date().toISOString()
    }));
    api.access.deny(`Auth action error: ${error.message}. Ref: AUTH-ACTION-FAIL`);
  }
};
```

### 2. SPA Client-Side Error Handling

```typescript
// ❌ ANTI-PATTERN: Silent redirect on auth error
const handleCallback = async () => {
  try {
    await auth0Client.handleRedirectCallback();
  } catch {
    window.location.href = '/';  // User never knows what happened
  }
};

// ✅ CORRECT: Surface the error with context
const handleCallback = async () => {
  try {
    const result = await auth0Client.handleRedirectCallback();
    if (!result) throw new Error('Empty callback result');
    
    // Validate token has expected claims
    const token = await auth0Client.getIdTokenClaims();
    const roles = token?.['https://lockn.app/roles'];
    if (!roles || roles.length === 0) {
      reportAuthAnomaly('ROLES_EMPTY_POST_LOGIN', { userId: token?.sub });
      showUserError(
        'Authentication succeeded but role assignment failed.',
        'Please try again. If this persists, contact support.',
        'AUTH-ROLES-001'
      );
      return;
    }
  } catch (error) {
    reportAuthAnomaly('CALLBACK_FAILED', { error: error.message });
    showUserError(
      'Login failed',
      error.message || 'An unexpected error occurred during authentication.',
      'AUTH-CALLBACK-001'
    );
  }
};
```

### 3. Error Reporting Integration

```typescript
function reportAuthAnomaly(code: string, context: Record<string, any>) {
  // 1. Structured log for monitoring
  console.error(JSON.stringify({
    level: 'error',
    category: 'auth',
    code,
    ...context,
    timestamp: new Date().toISOString(),
    url: window.location.href,
    userAgent: navigator.userAgent
  }));
  
  // 2. If monitoring service available (e.g., Sentry, Datadog)
  if (window.monitoringClient) {
    window.monitoringClient.captureEvent({
      message: `Auth anomaly: ${code}`,
      level: 'error',
      tags: { category: 'auth', code },
      extra: context
    });
  }
  
  // 3. Beacon to auth health endpoint (fire-and-forget)
  navigator.sendBeacon('/api/auth-health/report', JSON.stringify({ code, ...context }));
}

function showUserError(title: string, detail: string, refCode: string) {
  // Replace with your UI pattern (toast, modal, error page)
  const errorEl = document.getElementById('auth-error-container');
  if (errorEl) {
    errorEl.innerHTML = `
      <div class="auth-error">
        <h3>${title}</h3>
        <p>${detail}</p>
        <small>Reference: ${refCode}</small>
        <button onclick="window.location.reload()">Try Again</button>
      </div>
    `;
    errorEl.style.display = 'block';
  }
}
```

## Callback URL Strategy (Single Route)

Per LOC-425, use a **single callback route** instead of per-page callbacks:

```
✅ Allowed Callback URL: https://app.lockn.dev/auth/callback
❌ NOT: https://app.lockn.dev/page1, https://app.lockn.dev/page2, ...
```

The callback route handles redirect and restores the user's intended destination:

```typescript
// /auth/callback route handler
const returnTo = sessionStorage.getItem('auth_return_to') || '/dashboard';
sessionStorage.removeItem('auth_return_to');
await auth0Client.handleRedirectCallback();
router.push(returnTo);
```

## Auth Smoke Test Checklist (LOC-426)

Post-deploy, validate:
1. **Login flow**: Can a test user authenticate end-to-end?
2. **Token claims**: Does the ID token contain expected roles?
3. **Callback resolution**: Does `/auth/callback` resolve correctly?
4. **Silent renewal**: Does `getTokenSilently()` work?
5. **Logout**: Does logout clear session and redirect?

## Integration with Monitoring

Auth errors should trigger alerts when:
- `auth.roles_empty` count > 0 in any 5-minute window
- `auth.action_error` fires at all (critical)
- `auth.callback_failed` rate exceeds 5% of login attempts
- Silent auth failure rate exceeds baseline by 2x

## Related Tickets
- LOC-425: Single callback route consolidation
- LOC-426: Auth Smoke Tests
- LOC-427: Temporary Security Gate Tracker
