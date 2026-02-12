# Auth0 Management API Integration Guide

> Research completed for LOC-148 | Last updated: 2026-02-06

## Authentication

### How to Get Management API Token

Auth0 uses OAuth 2.0 Client Credentials flow for machine-to-machine authentication.

**Prerequisites:**
1. Create a Machine-to-Machine Application in Auth0 Dashboard
2. Authorize it for the Auth0 Management API with required scopes
3. Note the Client ID and Client Secret

**Token Request:**
```bash
POST https://{yourDomain}/oauth/token
Content-Type: application/json

{
  "grant_type": "client_credentials",
  "client_id": "{yourClientId}",
  "client_secret": "{yourClientSecret}",
  "audience": "https://{yourDomain}/api/v2/"
}
```

**Response:**
```json
{
  "access_token": "eyJ...Ggg",
  "expires_in": 86400,
  "scope": "read:users create:users update:users",
  "token_type": "Bearer"
}
```

### Token Refresh Strategy

- **Default expiry:** 24 hours (86400 seconds)
- **Recommendation:** Cache the token and refresh before expiry
- **Pattern:** Request new token when `expires_in` approaches (e.g., 5 minutes before)
- **No refresh tokens:** Must request a new token via client credentials flow

**Required Scopes for User Management:**
| Permission | Description |
|------------|-------------|
| `create:users` | Create users in database/passwordless connections |
| `read:users` | Search and retrieve user records |
| `update:users` | Update any user attribute |
| `delete:users` | Delete users |
| `create:roles` | Create new roles |
| `read:roles` | Read role definitions |
| `update:users` | Assign roles to users |

---

## User Creation

### API Endpoint and Payload

**Endpoint:** `POST /api/v2/users`

**Full Request:**
```bash
POST https://{yourDomain}/api/v2/users
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "email": "user@example.com",
  "email_verified": true,
  "password": "SecurePassword123!",
  "connection": "Username-Password-Authentication",
  "name": "John Doe",
  "given_name": "John",
  "family_name": "Doe",
  "nickname": "john",
  "user_metadata": {
    "preferred_language": "en"
  },
  "app_metadata": {
    "plan": "beta-tester",
    "signup_source": "admin_invite"
  },
  "blocked": false,
  "verify_email": false
}
```

### Pre-Verified Email Flow (Admin-Created Users)

For invite-only / admin-created users who should skip email verification:

```json
{
  "email": "invited@example.com",
  "email_verified": true,
  "password": "TemporaryPassword123!",
  "connection": "Username-Password-Authentication",
  "app_metadata": {
    "invited_by": "admin",
    "role": "beta-tester"
  }
}
```

**Key fields:**
- `email_verified: true` — Skip verification email
- `verify_email: false` — Don't send verification (default when email_verified is true)
- After creation, send password reset ticket for user to set their own password

### Key Fields Explained

| Field | Type | Description |
|-------|------|-------------|
| `email` | string | **Required.** User's email address |
| `connection` | string | **Required.** Connection name (e.g., `Username-Password-Authentication`) |
| `password` | string | Required for database connections |
| `email_verified` | boolean | Set `true` to skip verification |
| `user_metadata` | object | User-editable custom data |
| `app_metadata` | object | Admin-only custom data (roles, plans, flags) |
| `blocked` | boolean | Block user from logging in |

---

## Role Management

### Creating Roles

**Endpoint:** `POST /api/v2/roles`

**Scope Required:** `create:roles`

```bash
POST https://{yourDomain}/api/v2/roles
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "name": "beta-tester",
  "description": "Users with early access to beta features"
}
```

**Create custom roles for your use cases:**
```json
// beta-tester role
{
  "name": "beta-tester",
  "description": "Access to beta features and early releases"
}

// early-access role
{
  "name": "early-access", 
  "description": "Priority access to new features before general release"
}
```

### Assigning Roles to Users

**Endpoint:** `POST /api/v2/users/{user_id}/roles`

**Scope Required:** `read:roles`, `update:users`

```bash
POST https://{yourDomain}/api/v2/users/{user_id}/roles
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "roles": ["rol_abc123", "rol_def456"]
}
```

**Note:** You need the role IDs, not names. Get them via `GET /api/v2/roles`.

### Checking User Roles

**Endpoint:** `GET /api/v2/users/{user_id}/roles`

```bash
GET https://{yourDomain}/api/v2/users/{user_id}/roles
Authorization: Bearer {access_token}
```

**Response:**
```json
[
  {
    "id": "rol_abc123",
    "name": "beta-tester",
    "description": "Access to beta features"
  }
]
```

### Alternative: Using app_metadata for Roles

For simpler use cases, store roles directly in `app_metadata`:

```json
{
  "app_metadata": {
    "roles": ["beta-tester", "early-access"],
    "permissions": ["feature:beta", "feature:early"]
  }
}
```

**Pros:** Simpler, no extra API calls
**Cons:** Not integrated with Auth0's RBAC, won't appear in tokens automatically

---

## Email Triggers

### Password Reset Ticket

**Endpoint:** `POST /api/v2/tickets/password-change`

**Scope Required:** `create:user_tickets`

```bash
POST https://{yourDomain}/api/v2/tickets/password-change
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "user_id": "auth0|123456",
  "result_url": "https://yourapp.com/welcome",
  "ttl_sec": 86400,
  "mark_email_as_verified": true,
  "includeEmailInRedirect": false
}
```

**Response:**
```json
{
  "ticket": "https://{yourDomain}/lo/reset?ticket=abc123..."
}
```

**Use cases:**
- Send to admin-created users to set their password
- Embed in custom welcome emails
- Force password reset for security

### Email Verification Ticket

**Endpoint:** `POST /api/v2/tickets/email-verification`

```bash
POST https://{yourDomain}/api/v2/tickets/email-verification
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "user_id": "auth0|123456",
  "result_url": "https://yourapp.com/verified",
  "ttl_sec": 432000
}
```

### Trigger Verification Email Directly

**Endpoint:** `POST /api/v2/jobs/verification-email`

```bash
POST https://{yourDomain}/api/v2/jobs/verification-email
Content-Type: application/json
Authorization: Bearer {access_token}

{
  "user_id": "auth0|123456",
  "client_id": "{yourClientId}"
}
```

### Custom Email Templates

Email templates are managed in Auth0 Dashboard under **Branding > Email Templates**.

Available templates:
- Verification Email
- Welcome Email
- Change Password
- Blocked Account
- Password Breach Alert
- MFA Enrollment

**Note:** Custom templates require a custom email provider (SendGrid, Mailgun, etc.) — Auth0's built-in provider doesn't support customization.

---

## Code Examples (.NET)

### NuGet Packages

```bash
dotnet add package Auth0.AuthenticationApi
dotnet add package Auth0.ManagementApi
```

### HttpClient Setup with Token Management

```csharp
using Auth0.AuthenticationApi;
using Auth0.AuthenticationApi.Models;
using Auth0.ManagementApi;
using Auth0.ManagementApi.Models;

public class Auth0ManagementService
{
    private readonly string _domain;
    private readonly string _clientId;
    private readonly string _clientSecret;
    private ManagementApiClient? _managementClient;
    private DateTime _tokenExpiry = DateTime.MinValue;

    public Auth0ManagementService(string domain, string clientId, string clientSecret)
    {
        _domain = domain;
        _clientId = clientId;
        _clientSecret = clientSecret;
    }

    private async Task<ManagementApiClient> GetClientAsync()
    {
        // Refresh token if expired or expiring soon
        if (_managementClient == null || DateTime.UtcNow >= _tokenExpiry.AddMinutes(-5))
        {
            using var authClient = new AuthenticationApiClient(_domain);
            
            var tokenResponse = await authClient.GetTokenAsync(new ClientCredentialsTokenRequest
            {
                Audience = $"https://{_domain}/api/v2/",
                ClientId = _clientId,
                ClientSecret = _clientSecret
            });

            _tokenExpiry = DateTime.UtcNow.AddSeconds(tokenResponse.ExpiresIn);
            _managementClient = new ManagementApiClient(
                tokenResponse.AccessToken, 
                new Uri($"https://{_domain}/api/v2")
            );
        }

        return _managementClient;
    }
}
```

### Create User with Role

```csharp
public async Task<User> CreateUserWithRoleAsync(
    string email, 
    string name, 
    string roleId,
    bool sendPasswordReset = true)
{
    var client = await GetClientAsync();
    
    // 1. Create the user with a temporary password
    var user = await client.Users.CreateAsync(new UserCreateRequest
    {
        Email = email,
        EmailVerified = true,  // Skip verification for invited users
        Password = GenerateSecurePassword(),
        Connection = "Username-Password-Authentication",
        Name = name,
        AppMetadata = new
        {
            invited = true,
            invitedAt = DateTime.UtcNow
        }
    });

    // 2. Assign the role
    await client.Users.AssignRolesAsync(user.UserId, new AssignRolesRequest
    {
        Roles = new[] { roleId }
    });

    // 3. Optionally generate password reset ticket
    if (sendPasswordReset)
    {
        var ticket = await client.Tickets.CreatePasswordChangeTicketAsync(
            new PasswordChangeTicketRequest
            {
                UserId = user.UserId,
                ResultUrl = "https://yourapp.com/welcome",
                MarkEmailAsVerified = true,
                Ttl = 86400  // 24 hours
            });
        
        // Send ticket.Value (the URL) via your email service
    }

    return user;
}

private string GenerateSecurePassword()
{
    // Generate a random 32-char password (user will reset it anyway)
    return Convert.ToBase64String(RandomNumberGenerator.GetBytes(24));
}
```

### Create Role

```csharp
public async Task<Role> CreateRoleAsync(string name, string description)
{
    var client = await GetClientAsync();
    
    return await client.Roles.CreateAsync(new RoleCreateRequest
    {
        Name = name,
        Description = description
    });
}

// Usage: Create beta-tester and early-access roles
await CreateRoleAsync("beta-tester", "Access to beta features");
await CreateRoleAsync("early-access", "Priority access to new features");
```

### Error Handling

```csharp
public async Task<User?> SafeCreateUserAsync(string email, string name)
{
    try
    {
        var client = await GetClientAsync();
        
        return await client.Users.CreateAsync(new UserCreateRequest
        {
            Email = email,
            EmailVerified = true,
            Password = GenerateSecurePassword(),
            Connection = "Username-Password-Authentication",
            Name = name
        });
    }
    catch (Auth0.Core.Exceptions.ErrorApiException ex)
    {
        // Handle specific Auth0 errors
        switch (ex.ApiError.ErrorCode)
        {
            case "invalid_body":
                _logger.LogError("Invalid request: {Message}", ex.ApiError.Message);
                break;
            case "conflict":
                _logger.LogWarning("User already exists: {Email}", email);
                break;
            default:
                _logger.LogError(ex, "Auth0 API error: {Code}", ex.ApiError.ErrorCode);
                break;
        }
        return null;
    }
    catch (Auth0.Core.Exceptions.RateLimitApiException ex)
    {
        _logger.LogWarning(
            "Rate limited. Retry after {Seconds}s", 
            ex.RateLimit.Reset.TotalSeconds);
        
        // Implement exponential backoff
        await Task.Delay(TimeSpan.FromSeconds(ex.RateLimit.Reset.TotalSeconds));
        return await SafeCreateUserAsync(email, name); // Retry
    }
}
```

### Complete Service Example

```csharp
public interface IAuth0UserService
{
    Task<User> CreateBetaTesterAsync(string email, string name);
    Task<string> GetPasswordResetLinkAsync(string userId);
    Task<IList<Role>> GetUserRolesAsync(string userId);
}

public class Auth0UserService : IAuth0UserService
{
    private readonly Auth0ManagementService _auth0;
    private readonly ILogger<Auth0UserService> _logger;
    private string? _betaTesterRoleId;

    public Auth0UserService(
        Auth0ManagementService auth0,
        ILogger<Auth0UserService> logger)
    {
        _auth0 = auth0;
        _logger = logger;
    }

    public async Task<User> CreateBetaTesterAsync(string email, string name)
    {
        // Ensure role exists and get ID
        var roleId = await EnsureBetaTesterRoleAsync();
        
        // Create user with role
        var user = await _auth0.CreateUserWithRoleAsync(email, name, roleId);
        
        _logger.LogInformation(
            "Created beta tester: {Email} ({UserId})", 
            email, user.UserId);
        
        return user;
    }

    private async Task<string> EnsureBetaTesterRoleAsync()
    {
        if (_betaTesterRoleId != null) return _betaTesterRoleId;
        
        var client = await _auth0.GetClientAsync();
        var roles = await client.Roles.GetAllAsync(new GetRolesRequest());
        
        var role = roles.FirstOrDefault(r => r.Name == "beta-tester");
        if (role == null)
        {
            role = await client.Roles.CreateAsync(new RoleCreateRequest
            {
                Name = "beta-tester",
                Description = "Early access to beta features"
            });
        }
        
        _betaTesterRoleId = role.Id;
        return _betaTesterRoleId;
    }
}
```

---

## Rate Limits

### Limits by Tenant Type

| Tenant Type | Management API Limit | Burst Limit |
|-------------|---------------------|-------------|
| Free/Trial | 2 requests/second | — |
| Essential/Professional | 15 requests/second | 50 requests |
| Enterprise | 15 requests/second | 50 requests |
| Enterprise (with burst) | 100+ RPS | Configurable |

### Specific Endpoint Limits

Some endpoints have additional limits:
- **User creation:** Part of global limit
- **Password change tickets:** Part of global limit
- **Bulk user export:** Separate job queue

### Rate Limit Headers

Every response includes:
```
X-RateLimit-Limit: 15
X-RateLimit-Remaining: 14
X-RateLimit-Reset: 1612345678
```

### Recommended Patterns

1. **Check remaining limit before bulk operations:**
   ```csharp
   // Check X-RateLimit-Remaining header
   if (remaining < 5) await Task.Delay(1000);
   ```

2. **Implement exponential backoff:**
   ```csharp
   async Task<T> WithRetryAsync<T>(Func<Task<T>> action, int maxRetries = 3)
   {
       for (int i = 0; i < maxRetries; i++)
       {
           try { return await action(); }
           catch (RateLimitApiException ex)
           {
               var delay = Math.Pow(2, i) * 1000; // 1s, 2s, 4s
               await Task.Delay((int)delay);
           }
       }
       throw new Exception("Max retries exceeded");
   }
   ```

3. **Batch operations with delays:**
   ```csharp
   foreach (var batch in users.Chunk(10))
   {
       await Task.WhenAll(batch.Select(CreateUserAsync));
       await Task.Delay(1000); // 1 second between batches
   }
   ```

4. **Use bulk import for large datasets:**
   - For 100+ users, use `POST /api/v2/jobs/users-imports`
   - Uploads a JSON file, processes asynchronously
   - No rate limiting on the import itself

---

## Quick Reference

### Common Endpoints

| Operation | Method | Endpoint |
|-----------|--------|----------|
| Create user | POST | `/api/v2/users` |
| Get user | GET | `/api/v2/users/{id}` |
| Update user | PATCH | `/api/v2/users/{id}` |
| Delete user | DELETE | `/api/v2/users/{id}` |
| Create role | POST | `/api/v2/roles` |
| Assign roles | POST | `/api/v2/users/{id}/roles` |
| Get user roles | GET | `/api/v2/users/{id}/roles` |
| Password reset ticket | POST | `/api/v2/tickets/password-change` |
| Email verification ticket | POST | `/api/v2/tickets/email-verification` |
| Send verification email | POST | `/api/v2/jobs/verification-email` |

### User ID Format

Auth0 user IDs follow the format: `{connection}|{id}`
- Database users: `auth0|507f1f77bcf86cd799439011`
- Google users: `google-oauth2|115036145678901234567`
- Custom: Depends on connection strategy

---

## References

- [Auth0 Management API v2 Reference](https://auth0.com/docs/api/management/v2)
- [Get Management API Tokens](https://auth0.com/docs/secure/tokens/access-tokens/management-api-access-tokens)
- [Rate Limit Policy](https://auth0.com/docs/troubleshoot/customer-support/operational-policies/rate-limit-policy)
- [Auth0.NET SDK](https://github.com/auth0/auth0.net)
- [Create Roles](https://auth0.com/docs/manage-users/access-control/configure-core-rbac/roles/create-roles)
- [Assign Roles to Users](https://auth0.com/docs/manage-users/access-control/configure-core-rbac/rbac-users/assign-roles-to-users)
