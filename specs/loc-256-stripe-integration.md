# LOC-256: Stripe Integration for LockN Labs
## Technical Specification

**Company:** OneSun Labs LLC DBA LockN Labs  
**Date:** February 8, 2026  
**Version:** 1.0  
**License Requirements:** Apache/MIT licensed components only  

---

## Executive Summary

This specification outlines the integration of Stripe's billing platform with the LockN Labs .NET ecosystem to enable subscription management, usage-based billing, and customer portal functionality. The integration will support multiple pricing tiers with both fixed and metered billing models while maintaining PCI compliance and security best practices.

---

## 1. Stripe API Research & Capabilities (2026)

### 1.1 Core Stripe Services for SaaS

**Stripe Billing Platform Features:**
- **Subscription Management**: Fixed, per-seat, and usage-based billing models
- **Stripe Checkout**: Pre-built payment flows with subscription support
- **Customer Portal**: Self-service billing management
- **Webhooks**: Real-time event notifications for payment state changes
- **Invoice Management**: Automated invoice generation and payment collection
- **Usage Metering**: API-based consumption tracking and billing

### 1.2 Current API Capabilities

**Subscription Models Supported:**
- **Fixed Pricing**: Monthly/yearly flat rates
- **Per-Seat Pricing**: Linear scaling with user count
- **Usage-Based**: Metered billing with tiered pricing
- **Hybrid Models**: Combination of fixed base + usage overages

**Payment Methods:**
- Credit/debit cards (primary)
- ACH Direct Debit (US)
- SEPA Direct Debit (EU)
- Digital wallets (Apple Pay, Google Pay)

**Customer Portal Features:**
- Update payment methods
- View/download invoices
- Manage subscriptions (pause, cancel, upgrade/downgrade)
- View usage and billing history
- Update billing address and tax information

---

## 2. .NET Integration Architecture

### 2.1 System Overview

```
┌─────────────────┐    ┌──────────────────┐    ┌─────────────────┐
│   Auth0 Users   │◄──►│   LockN Backend  │◄──►│     Stripe      │
│                 │    │    (.NET 8+)     │    │   (Billing)     │
└─────────────────┘    └──────────────────┘    └─────────────────┘
                                │
                                ▼
                       ┌──────────────────┐
                       │   PostgreSQL     │
                       │   (User/Billing  │
                       │     Mapping)     │
                       └──────────────────┘
```

### 2.2 Core Components

#### 2.2.1 Stripe.NET SDK Integration

**NuGet Package:** `Stripe.net` (MIT License)
```csharp
// Package Reference
<PackageReference Include="Stripe.net" Version="45.x.x" />
```

**Configuration:**
```csharp
// Startup.cs / Program.cs
services.Configure<StripeSettings>(configuration.GetSection("Stripe"));
services.AddScoped<IStripeService, StripeService>();
StripeConfiguration.ApiKey = configuration["Stripe:SecretKey"];
```

#### 2.2.2 Service Layer Architecture

```csharp
public interface IStripeService
{
    // Customer Management
    Task<Customer> CreateCustomerAsync(string auth0UserId, string email, string name);
    Task<Customer> GetCustomerAsync(string customerId);
    Task<Customer> UpdateCustomerAsync(string customerId, CustomerUpdateRequest request);
    
    // Subscription Management
    Task<Subscription> CreateSubscriptionAsync(string customerId, string priceId);
    Task<Subscription> UpdateSubscriptionAsync(string subscriptionId, SubscriptionUpdateRequest request);
    Task<Subscription> CancelSubscriptionAsync(string subscriptionId, bool immediate = false);
    
    // Checkout Sessions
    Task<Session> CreateCheckoutSessionAsync(CheckoutSessionRequest request);
    
    // Customer Portal
    Task<BillingPortalSession> CreatePortalSessionAsync(string customerId, string returnUrl);
    
    // Usage Metering
    Task RecordUsageAsync(string subscriptionItemId, int quantity, string idempotencyKey);
    Task<UsageRecord> GetUsageAsync(string subscriptionItemId, DateTime startDate, DateTime endDate);
    
    // Webhooks
    Task<Event> ConstructWebhookEventAsync(string json, string signature, string secret);
    Task ProcessWebhookEventAsync(Event stripeEvent);
}
```

### 2.3 Subscription Management

#### 2.3.1 Stripe Checkout Integration

```csharp
[ApiController]
[Route("api/[controller]")]
public class BillingController : ControllerBase
{
    private readonly IStripeService _stripeService;
    private readonly IUserService _userService;
    
    [HttpPost("create-checkout-session")]
    [Authorize]
    public async Task<IActionResult> CreateCheckoutSession([FromBody] CheckoutRequest request)
    {
        var auth0UserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
        var user = await _userService.GetUserAsync(auth0UserId);
        
        var sessionRequest = new CheckoutSessionRequest
        {
            Customer = user.StripeCustomerId,
            PriceId = request.PriceId,
            Mode = "subscription",
            SuccessUrl = $"{request.BaseUrl}/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
            CancelUrl = $"{request.BaseUrl}/billing/cancel",
            Metadata = new Dictionary<string, string>
            {
                { "auth0_user_id", auth0UserId },
                { "tier", request.Tier }
            }
        };
        
        var session = await _stripeService.CreateCheckoutSessionAsync(sessionRequest);
        return Ok(new { checkoutUrl = session.Url });
    }
}
```

#### 2.3.2 Customer Portal Integration

```csharp
[HttpPost("create-portal-session")]
[Authorize]
public async Task<IActionResult> CreatePortalSession()
{
    var auth0UserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    var user = await _userService.GetUserAsync(auth0UserId);
    
    if (string.IsNullOrEmpty(user.StripeCustomerId))
    {
        return BadRequest("No billing account found");
    }
    
    var returnUrl = $"{Request.Scheme}://{Request.Host}/dashboard/billing";
    var portalSession = await _stripeService.CreatePortalSessionAsync(user.StripeCustomerId, returnUrl);
    
    return Ok(new { portalUrl = portalSession.Url });
}
```

### 2.4 Webhook Handling

#### 2.4.1 Webhook Endpoint

```csharp
[ApiController]
[Route("api/stripe")]
public class StripeWebhookController : ControllerBase
{
    private readonly IStripeService _stripeService;
    private readonly IConfiguration _configuration;
    private readonly ILogger<StripeWebhookController> _logger;
    
    [HttpPost("webhook")]
    public async Task<IActionResult> HandleWebhook()
    {
        var json = await new StreamReader(HttpContext.Request.Body).ReadToEndAsync();
        var signature = Request.Headers["Stripe-Signature"];
        var endpointSecret = _configuration["Stripe:WebhookSecret"];
        
        try
        {
            var stripeEvent = await _stripeService.ConstructWebhookEventAsync(json, signature, endpointSecret);
            await _stripeService.ProcessWebhookEventAsync(stripeEvent);
            
            return Ok();
        }
        catch (StripeException ex)
        {
            _logger.LogError(ex, "Webhook signature verification failed");
            return BadRequest();
        }
    }
}
```

#### 2.4.2 Event Processing

```csharp
public async Task ProcessWebhookEventAsync(Event stripeEvent)
{
    switch (stripeEvent.Type)
    {
        case Events.CustomerSubscriptionCreated:
            await HandleSubscriptionCreated(stripeEvent);
            break;
            
        case Events.CustomerSubscriptionUpdated:
            await HandleSubscriptionUpdated(stripeEvent);
            break;
            
        case Events.CustomerSubscriptionDeleted:
            await HandleSubscriptionCanceled(stripeEvent);
            break;
            
        case Events.InvoicePaymentSucceeded:
            await HandlePaymentSucceeded(stripeEvent);
            break;
            
        case Events.InvoicePaymentFailed:
            await HandlePaymentFailed(stripeEvent);
            break;
            
        case Events.CheckoutSessionCompleted:
            await HandleCheckoutCompleted(stripeEvent);
            break;
            
        default:
            _logger.LogInformation($"Unhandled event type: {stripeEvent.Type}");
            break;
    }
}

private async Task HandleSubscriptionCreated(Event stripeEvent)
{
    var subscription = stripeEvent.Data.Object as Subscription;
    var customerId = subscription.CustomerId;
    
    // Update user subscription status in database
    await _userService.UpdateSubscriptionStatusAsync(customerId, subscription.Id, "active");
    
    // Grant access to premium features
    await _featureService.EnablePremiumFeaturesAsync(customerId);
    
    // Send welcome email
    await _emailService.SendSubscriptionWelcomeEmailAsync(customerId);
}
```

### 2.5 Usage-Based Billing

#### 2.5.1 Usage Tracking Service

```csharp
public interface IUsageTrackingService
{
    Task RecordApiCallAsync(string auth0UserId, string endpoint, int cost = 1);
    Task RecordDataTransferAsync(string auth0UserId, long bytesTransferred);
    Task RecordComputeUsageAsync(string auth0UserId, TimeSpan duration);
    Task<UsageSummary> GetUsageSummaryAsync(string auth0UserId, DateTime period);
    Task SubmitUsageToStripeAsync(string auth0UserId, DateTime billingPeriod);
}

public class UsageTrackingService : IUsageTrackingService
{
    private readonly IUserService _userService;
    private readonly IStripeService _stripeService;
    private readonly IUsageRepository _usageRepository;
    
    public async Task RecordApiCallAsync(string auth0UserId, string endpoint, int cost = 1)
    {
        var usageRecord = new UsageRecord
        {
            Auth0UserId = auth0UserId,
            Timestamp = DateTime.UtcNow,
            UsageType = UsageType.ApiCall,
            Quantity = cost,
            Metadata = new { endpoint }
        };
        
        await _usageRepository.CreateAsync(usageRecord);
        
        // Real-time usage submission for high-volume customers
        var user = await _userService.GetUserAsync(auth0UserId);
        if (user.SubscriptionTier == "enterprise")
        {
            await SubmitUsageToStripeAsync(auth0UserId, DateTime.UtcNow);
        }
    }
    
    public async Task SubmitUsageToStripeAsync(string auth0UserId, DateTime billingPeriod)
    {
        var user = await _userService.GetUserAsync(auth0UserId);
        var usage = await _usageRepository.GetUsageForPeriodAsync(auth0UserId, billingPeriod);
        
        if (user.SubscriptionItemId != null && usage.TotalApiCalls > 0)
        {
            var idempotencyKey = $"{auth0UserId}-{billingPeriod:yyyy-MM-dd}";
            await _stripeService.RecordUsageAsync(
                user.SubscriptionItemId, 
                usage.TotalApiCalls, 
                idempotencyKey
            );
        }
    }
}
```

---

## 3. Data Model Design

### 3.1 User-Customer Mapping

```csharp
public class UserBillingProfile
{
    public int Id { get; set; }
    
    // Auth0 Integration
    public string Auth0UserId { get; set; } // Required, unique
    public string Email { get; set; }
    public string DisplayName { get; set; }
    
    // Stripe Integration
    public string StripeCustomerId { get; set; } // Unique
    public string SubscriptionId { get; set; }
    public string SubscriptionItemId { get; set; } // For usage reporting
    
    // Subscription Details
    public SubscriptionTier Tier { get; set; } = SubscriptionTier.Free;
    public SubscriptionStatus Status { get; set; } = SubscriptionStatus.Inactive;
    public DateTime? SubscriptionStartDate { get; set; }
    public DateTime? SubscriptionEndDate { get; set; }
    public DateTime? TrialEndDate { get; set; }
    
    // Usage Tracking
    public int MonthlyApiCalls { get; set; } = 0;
    public long MonthlyDataTransferBytes { get; set; } = 0;
    public DateTime UsageResetDate { get; set; }
    
    // Audit
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
    
    // Navigation
    public virtual List<UsageRecord> UsageRecords { get; set; } = new();
    public virtual List<InvoiceRecord> Invoices { get; set; } = new();
}

public enum SubscriptionTier
{
    Free = 0,
    Pro = 1,
    Enterprise = 2
}

public enum SubscriptionStatus
{
    Inactive = 0,
    Active = 1,
    Trialing = 2,
    PastDue = 3,
    Canceled = 4,
    Unpaid = 5
}
```

### 3.2 Usage Tracking Model

```csharp
public class UsageRecord
{
    public int Id { get; set; }
    public string Auth0UserId { get; set; }
    public DateTime Timestamp { get; set; }
    public UsageType UsageType { get; set; }
    public int Quantity { get; set; }
    public decimal Cost { get; set; }
    public string Metadata { get; set; } // JSON
    public bool SubmittedToStripe { get; set; } = false;
    public DateTime? StripeSubmissionDate { get; set; }
    
    // Navigation
    public virtual UserBillingProfile User { get; set; }
}

public enum UsageType
{
    ApiCall = 1,
    DataTransfer = 2,
    ComputeTime = 3,
    StorageUsage = 4
}
```

### 3.3 Database Schema (Entity Framework)

```csharp
public class BillingDbContext : DbContext
{
    public DbSet<UserBillingProfile> UserBillingProfiles { get; set; }
    public DbSet<UsageRecord> UsageRecords { get; set; }
    public DbSet<InvoiceRecord> Invoices { get; set; }
    
    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        // User Billing Profile
        modelBuilder.Entity<UserBillingProfile>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => e.Auth0UserId).IsUnique();
            entity.HasIndex(e => e.StripeCustomerId).IsUnique();
            entity.Property(e => e.Email).IsRequired().HasMaxLength(256);
            entity.Property(e => e.Auth0UserId).IsRequired().HasMaxLength(128);
        });
        
        // Usage Records
        modelBuilder.Entity<UsageRecord>(entity =>
        {
            entity.HasKey(e => e.Id);
            entity.HasIndex(e => new { e.Auth0UserId, e.Timestamp });
            entity.HasIndex(e => new { e.Auth0UserId, e.SubmittedToStripe });
            
            entity.HasOne(e => e.User)
                  .WithMany(u => u.UsageRecords)
                  .HasForeignKey(e => e.Auth0UserId)
                  .HasPrincipalKey(u => u.Auth0UserId);
        });
    }
}
```

---

## 4. Security Considerations

### 4.1 Webhook Security

#### 4.1.1 Signature Verification

```csharp
public class StripeWebhookVerificationService
{
    private readonly IConfiguration _configuration;
    
    public Event ConstructEvent(string json, string signature)
    {
        var endpointSecret = _configuration["Stripe:WebhookSecret"];
        
        try
        {
            return EventUtility.ConstructEvent(
                json, 
                signature, 
                endpointSecret,
                300, // 5 minute tolerance
                throwOnApiVersionMismatch: false
            );
        }
        catch (StripeException ex)
        {
            throw new UnauthorizedAccessException("Invalid webhook signature", ex);
        }
    }
}
```

#### 4.1.2 Webhook Security Best Practices

- **HTTPS Only**: All webhook endpoints must use HTTPS
- **Signature Verification**: Always verify Stripe-Signature header
- **Idempotency**: Handle duplicate webhook events gracefully
- **IP Allowlisting**: Restrict webhook endpoint access to Stripe IPs
- **Rate Limiting**: Implement rate limiting on webhook endpoints

```csharp
[EnableRateLimiting("WebhookPolicy")]
[RequireHttps]
public class StripeWebhookController : ControllerBase
{
    // Implementation...
}

// Startup configuration
services.AddRateLimiter(options =>
{
    options.AddFixedWindowLimiter("WebhookPolicy", limiterOptions =>
    {
        limiterOptions.PermitLimit = 100;
        limiterOptions.Window = TimeSpan.FromMinutes(1);
        limiterOptions.QueueProcessingOrder = QueueProcessingOrder.OldestFirst;
        limiterOptions.QueueLimit = 10;
    });
});
```

### 4.2 PCI Compliance

#### 4.2.1 Data Handling
- **No Card Storage**: Never store credit card information on LockN servers
- **Stripe.js Integration**: Use Stripe Elements for client-side card handling
- **Tokenization**: Only store Stripe customer/subscription IDs
- **Scope Limitation**: Minimize PCI scope by using Stripe Checkout

#### 4.2.2 Environment Separation

```bash
# Environment Variables (.env)
STRIPE_PUBLISHABLE_KEY_DEV=pk_test_...
STRIPE_SECRET_KEY_DEV=sk_test_...
STRIPE_WEBHOOK_SECRET_DEV=whsec_...

STRIPE_PUBLISHABLE_KEY_PROD=pk_live_...
STRIPE_SECRET_KEY_PROD=sk_live_...
STRIPE_WEBHOOK_SECRET_PROD=whsec_...
```

### 4.3 API Security

#### 4.3.1 Authentication & Authorization

```csharp
[Authorize]
[HttpGet("subscription-status")]
public async Task<IActionResult> GetSubscriptionStatus()
{
    var auth0UserId = User.FindFirst(ClaimTypes.NameIdentifier)?.Value;
    
    // Verify user owns the requested resource
    var userProfile = await _userService.GetUserAsync(auth0UserId);
    if (userProfile == null)
    {
        return NotFound();
    }
    
    return Ok(new SubscriptionStatusResponse
    {
        Tier = userProfile.Tier,
        Status = userProfile.Status,
        // Never expose Stripe IDs to client
        // StripeCustomerId = userProfile.StripeCustomerId // ❌ Don't do this
    });
}
```

#### 4.3.2 Data Privacy

- **Minimal Exposure**: Never expose Stripe customer/subscription IDs to frontend
- **Data Encryption**: Encrypt sensitive data in database using EF Core encryption
- **Audit Logging**: Log all billing-related actions

```csharp
public class AuditLogService
{
    public async Task LogBillingActionAsync(string auth0UserId, string action, object details)
    {
        var auditEntry = new AuditLog
        {
            UserId = auth0UserId,
            Action = action,
            Details = JsonSerializer.Serialize(details),
            Timestamp = DateTime.UtcNow,
            IpAddress = _httpContextAccessor.HttpContext?.Connection?.RemoteIpAddress?.ToString()
        };
        
        await _auditRepository.CreateAsync(auditEntry);
    }
}
```

---

## 5. Proposed Pricing Tiers

### 5.1 Free Tier
**Target:** Individual developers, proof-of-concept projects

**Features:**
- 1,000 API calls/month
- 100MB data transfer/month
- Basic documentation access
- Community support
- Single user account
- Standard rate limits

**Pricing:** $0/month

**Stripe Configuration:**
```json
{
  "product": "LockN Free",
  "price": {
    "unit_amount": 0,
    "currency": "usd",
    "recurring": {
      "interval": "month"
    }
  },
  "features": ["basic_api", "community_support"]
}
```

### 5.2 Pro Tier
**Target:** Small to medium development teams, production applications

**Features:**
- 50,000 API calls/month (base)
- Additional API calls: $0.01 per 100 calls
- 10GB data transfer/month (base)
- Additional transfer: $0.10 per GB
- Priority support (24h response)
- Advanced documentation & examples
- Up to 5 team members
- Custom rate limits
- Basic analytics dashboard

**Pricing:** $49/month + usage overages

**Stripe Configuration:**
```json
{
  "product": "LockN Pro",
  "prices": [
    {
      "id": "price_pro_base",
      "unit_amount": 4900,
      "currency": "usd",
      "recurring": {
        "interval": "month",
        "usage_type": "licensed"
      }
    },
    {
      "id": "price_pro_api_calls",
      "unit_amount": 1,
      "currency": "usd",
      "recurring": {
        "interval": "month",
        "usage_type": "metered",
        "aggregate_usage": "sum"
      },
      "billing_scheme": "per_unit",
      "tiers_mode": "graduated",
      "tiers": [
        {
          "up_to": 50000,
          "unit_amount": 0
        },
        {
          "up_to": "inf",
          "unit_amount": 1
        }
      ]
    }
  ]
}
```

### 5.3 Enterprise Tier
**Target:** Large organizations, high-volume applications

**Features:**
- 1,000,000 API calls/month (base)
- Additional API calls: $0.005 per 100 calls (50% discount)
- 100GB data transfer/month (base)
- Additional transfer: $0.05 per GB (50% discount)
- White-label options
- Custom integrations
- Dedicated support (4h response, phone support)
- Unlimited team members
- Advanced analytics & reporting
- Custom SLA options
- Priority feature requests
- On-premise deployment options

**Pricing:** $499/month + usage overages

**Stripe Configuration:**
```json
{
  "product": "LockN Enterprise",
  "prices": [
    {
      "id": "price_enterprise_base",
      "unit_amount": 49900,
      "currency": "usd",
      "recurring": {
        "interval": "month",
        "usage_type": "licensed"
      }
    },
    {
      "id": "price_enterprise_api_calls",
      "unit_amount": 0.5,
      "currency": "usd",
      "recurring": {
        "interval": "month",
        "usage_type": "metered",
        "aggregate_usage": "sum"
      },
      "billing_scheme": "per_unit",
      "tiers_mode": "graduated",
      "tiers": [
        {
          "up_to": 1000000,
          "unit_amount": 0
        },
        {
          "up_to": "inf",
          "unit_amount": 0.5
        }
      ]
    }
  ]
}
```

### 5.4 Tier Comparison Matrix

| Feature | Free | Pro | Enterprise |
|---------|------|-----|------------|
| **Base API Calls** | 1K/month | 50K/month | 1M/month |
| **Overage Pricing** | Not available | $0.01/100 calls | $0.005/100 calls |
| **Data Transfer** | 100MB | 10GB + $0.10/GB | 100GB + $0.05/GB |
| **Team Members** | 1 | 5 | Unlimited |
| **Support** | Community | Priority (24h) | Dedicated (4h) |
| **Analytics** | Basic | Advanced | Enterprise |
| **SLA** | None | 99.5% uptime | Custom SLA |
| **White-label** | No | No | Yes |
| **On-premise** | No | No | Available |

---

## 6. Implementation Plan

### 6.1 Phase 1: Foundation (Weeks 1-2)
- [ ] Set up Stripe account and configure products/prices
- [ ] Implement basic Stripe.NET integration
- [ ] Create database schema and migrations
- [ ] Implement Auth0 ↔ Stripe customer mapping
- [ ] Set up development/staging environments

### 6.2 Phase 2: Core Billing (Weeks 3-4)
- [ ] Implement Stripe Checkout integration
- [ ] Build webhook handling system
- [ ] Create customer portal integration
- [ ] Implement subscription status synchronization
- [ ] Add basic usage tracking

### 6.3 Phase 3: Advanced Features (Weeks 5-6)
- [ ] Implement usage-based billing
- [ ] Build usage analytics dashboard
- [ ] Add tier-based feature gates
- [ ] Implement invoice management
- [ ] Create billing admin panel

### 6.4 Phase 4: Testing & Launch (Weeks 7-8)
- [ ] Security audit and penetration testing
- [ ] Load testing webhook endpoints
- [ ] User acceptance testing
- [ ] Documentation and training materials
- [ ] Production deployment

---

## 7. Monitoring & Observability

### 7.1 Key Metrics
- **Subscription Metrics**: Monthly Recurring Revenue (MRR), churn rate, upgrade/downgrade rates
- **Usage Metrics**: API calls per tier, data transfer volumes, feature adoption
- **Payment Metrics**: Payment success/failure rates, retry success rates
- **Support Metrics**: Billing-related support tickets, resolution times

### 7.2 Alerting
- Failed payments requiring attention
- Webhook delivery failures
- Unusual usage spikes (potential abuse)
- Subscription cancellations
- API rate limit hits

### 7.3 Logging Strategy
```csharp
public class BillingEventLogger
{
    private readonly ILogger<BillingEventLogger> _logger;
    
    public void LogSubscriptionChange(string auth0UserId, string oldTier, string newTier, string reason)
    {
        _logger.LogInformation("Subscription tier change: User {UserId} changed from {OldTier} to {NewTier}. Reason: {Reason}",
            auth0UserId, oldTier, newTier, reason);
    }
    
    public void LogUsageThreshold(string auth0UserId, string usageType, int current, int limit)
    {
        _logger.LogWarning("Usage threshold exceeded: User {UserId} has {Current} {UsageType} usage (limit: {Limit})",
            auth0UserId, current, usageType, limit);
    }
}
```

---

## 8. Risk Assessment & Mitigation

### 8.1 Technical Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Webhook delivery failures | High | Medium | Implement retry logic, backup event polling |
| Payment processing downtime | High | Low | Use Stripe's 99.99% SLA, implement graceful degradation |
| Usage tracking accuracy | Medium | Medium | Implement idempotency, audit trails |
| Data synchronization issues | Medium | Medium | Regular reconciliation jobs, monitoring |

### 8.2 Business Risks
| Risk | Impact | Probability | Mitigation |
|------|--------|-------------|------------|
| Price sensitivity | Medium | Medium | A/B testing, gradual rollout, grandfathering |
| Competitive pricing pressure | High | High | Value-based differentiation, feature innovation |
| Compliance requirements | High | Low | Regular security audits, legal review |

---

## 9. Success Criteria

### 9.1 Technical KPIs
- **Webhook reliability**: >99.9% successful processing
- **Payment success rate**: >95% first-attempt success
- **API response times**: <200ms for billing endpoints
- **Usage tracking accuracy**: >99.5% precision

### 9.2 Business KPIs
- **Conversion rate**: Free → Pro >5%, Pro → Enterprise >2%
- **Revenue growth**: 20% MoM growth in first 6 months
- **Customer satisfaction**: <2% billing-related support tickets
- **Churn reduction**: <5% monthly churn rate

---

## 10. Conclusion

This specification provides a comprehensive roadmap for integrating Stripe's billing platform with LockN Labs' .NET ecosystem. The proposed architecture emphasizes security, scalability, and maintainability while providing flexibility for future pricing model evolution.

The three-tier pricing strategy (Free/Pro/Enterprise) provides clear upgrade paths and addresses different market segments. The usage-based billing component enables fair pricing for API consumption while encouraging adoption through generous base allowances.

Key success factors include:
1. **Robust webhook handling** for real-time billing synchronization
2. **Accurate usage tracking** for fair billing and analytics
3. **Security-first design** to maintain customer trust
4. **Comprehensive monitoring** for operational excellence

The implementation plan spreads technical risk across 8 weeks while delivering value incrementally. Regular security audits and performance monitoring will ensure long-term success of the billing integration.

---

## Appendices

### A. Required NuGet Packages
```xml
<PackageReference Include="Stripe.net" Version="45.x.x" />
<PackageReference Include="Microsoft.EntityFrameworkCore.Design" Version="8.x.x" />
<PackageReference Include="Microsoft.EntityFrameworkCore.PostgreSQL" Version="8.x.x" />
<PackageReference Include="Microsoft.AspNetCore.Authentication.JwtBearer" Version="8.x.x" />
<PackageReference Include="Microsoft.AspNetCore.RateLimiting" Version="8.x.x" />
```

### B. Environment Variables
```bash
# Stripe Configuration
STRIPE_PUBLISHABLE_KEY=pk_test_... 
STRIPE_SECRET_KEY=sk_test_...
STRIPE_WEBHOOK_SECRET=whsec_...

# Database
POSTGRES_CONNECTION_STRING=Host=localhost;Database=lockn_billing;Username=...

# Auth0
AUTH0_DOMAIN=lockn.auth0.com
AUTH0_CLIENT_ID=...
AUTH0_CLIENT_SECRET=...
```

### C. Stripe Product/Price Setup Script
```bash
#!/bin/bash
# Create products and prices in Stripe

# Free tier (product only, no price needed)
stripe products create --name "LockN Free" --description "Free tier for individual developers"

# Pro tier
PRO_PRODUCT_ID=$(stripe products create --name "LockN Pro" --description "Pro tier for development teams" --format-output-json | jq -r '.id')
stripe prices create --product $PRO_PRODUCT_ID --unit-amount 4900 --currency usd --recurring='{"interval":"month"}'

# Enterprise tier  
ENT_PRODUCT_ID=$(stripe products create --name "LockN Enterprise" --description "Enterprise tier for large organizations" --format-output-json | jq -r '.id')
stripe prices create --product $ENT_PRODUCT_ID --unit-amount 49900 --currency usd --recurring='{"interval":"month"}'
```

---

**Document Status:** ✅ Complete  
**Next Review:** March 15, 2026  
**Owner:** Revenue Infrastructure Team