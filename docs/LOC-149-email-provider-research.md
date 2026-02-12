# LOC-149: Email Provider Research & Templates

**Date:** 2026-02-06  
**Status:** Complete

---

## Email Provider Comparison

| Provider | Free Tier | Pricing (Paid) | Pros | Cons | .NET SDK |
|----------|-----------|----------------|------|------|----------|
| **SendGrid** | 60-day trial only (no permanent free tier) | Essentials: $19.95/mo (up to 50k), Pro: $89.95/mo | Comprehensive analytics, strong deliverability, dynamic templates, dedicated IPs on Pro | No permanent free tier, complex pricing tiers, costs escalate quickly | ✅ Official: `SendGrid` NuGet, .NET Standard 1.3+ |
| **Postmark** | 100 emails/mo forever (Developer tier) | Basic: $15/mo (10k), Pro: $16.50/mo (10k), Platform: $18/mo (10k) | **Best-in-class deliverability**, 4x faster delivery than competitors, focused on transactional, excellent docs | Higher per-email overage ($1.20-1.80/1k), limited free tier volume | ✅ Official: `Postmark` NuGet v5.2.0, .NET Standard 2.0 |
| **AWS SES** | 3,000 msgs/mo for 12 months (then expires) | $0.10/1,000 emails after free tier | **Cheapest at scale**, integrates with AWS ecosystem, highly reliable | 12-month free tier limit, more complex setup, requires AWS account, sandbox mode initially | ✅ Official: `AWSSDK.SimpleEmail` NuGet |
| **Mailgun** | 100 emails/day (~3k/mo) | Basic: $15/mo (10k), Foundation: $35/mo (50k), Scale: $90/mo (100k) | Good API, solid documentation, decent deliverability, dedicated IPs on Scale | **No official .NET SDK** (community only), costs add up at volume | ⚠️ Community: `mailgun_csharp` (3rd party, outdated) |

---

## Recommendation: **Postmark**

### Rationale

1. **Deliverability is Critical for Invites**
   - Beta/early access invites MUST reach inboxes, not spam folders
   - Postmark has industry-leading deliverability rates and publishes them publicly
   - 4x faster delivery than competitors (users get invites within seconds)

2. **Transactional Focus**
   - Postmark only handles transactional email (no marketing bulk mail)
   - This keeps their IP reputation pristine
   - Invite emails are inherently transactional

3. **Official .NET SDK**
   - `Postmark` NuGet package is actively maintained
   - .NET Standard 2.0 compatible (works with .NET Core 3.1+, .NET 5-9)
   - Clean, fluent API

4. **Simple Pricing**
   - 100 free emails/mo for development (never expires)
   - $15/mo for 10k emails when scaling
   - Predictable costs, no surprises

5. **Developer Experience**
   - Excellent documentation
   - Built-in responsive email templates
   - 45-day message retention for debugging

### When to Reconsider AWS SES

If sending 100k+ emails/month, AWS SES becomes more cost-effective:
- Postmark 100k emails: ~$100-130/mo
- AWS SES 100k emails: ~$10/mo

But for beta/early access invites (likely <10k/mo initially), Postmark's superior deliverability justifies the cost.

---

## Email Templates

### 1. Beta Invite Email

**Subject Line Options:**
- `You're in! 🎉 Your Locus beta access is ready`
- `[Locus] Your exclusive beta invite`
- `Welcome to the Locus beta — let's get started`

**HTML Version:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Your Locus Beta Invite</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2563eb; margin: 0;">🎉 You're In!</h1>
  </div>
  
  <p>Hi {{firstName}},</p>
  
  <p>Great news — you've been selected for the <strong>Locus beta</strong>!</p>
  
  <p>We've been building Locus to help teams {{value_prop}}, and we'd love your feedback as we refine the experience.</p>
  
  <div style="text-align: center; margin: 30px 0;">
    <a href="{{activationUrl}}" style="background-color: #2563eb; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
      Activate Your Account
    </a>
  </div>
  
  <p style="font-size: 14px; color: #666;">This invite expires in 7 days. Click the button above or copy this link:</p>
  <p style="font-size: 14px; color: #2563eb; word-break: break-all;">{{activationUrl}}</p>
  
  <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
  
  <p><strong>What to expect:</strong></p>
  <ul>
    <li>Full access to all beta features</li>
    <li>Direct line to our team for feedback</li>
    <li>Early adopter perks when we launch</li>
  </ul>
  
  <p>Questions? Just reply to this email — we read every message.</p>
  
  <p>— The Locus Team</p>
  
  <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
    <p>Locus, Inc. | {{companyAddress}}</p>
    <p><a href="{{unsubscribeUrl}}" style="color: #999;">Unsubscribe</a></p>
  </div>
  
</body>
</html>
```

**Plain Text Version:**
```
You're In! 🎉

Hi {{firstName}},

Great news — you've been selected for the Locus beta!

We've been building Locus to help teams {{value_prop}}, and we'd love your feedback as we refine the experience.

ACTIVATE YOUR ACCOUNT:
{{activationUrl}}

This invite expires in 7 days.

WHAT TO EXPECT:
• Full access to all beta features
• Direct line to our team for feedback  
• Early adopter perks when we launch

Questions? Just reply to this email — we read every message.

— The Locus Team

---
Locus, Inc. | {{companyAddress}}
Unsubscribe: {{unsubscribeUrl}}
```

---

### 2. Early Access Invite Email

**Subject Line Options:**
- `{{firstName}}, you're on the early access list`
- `Early access to Locus — you're next in line`
- `Your spot is reserved — Locus early access`

**HTML Version:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Early Access to Locus</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2563eb; margin: 0;">Your Early Access is Ready</h1>
  </div>
  
  <p>Hi {{firstName}},</p>
  
  <p>Thanks for your patience! We're excited to invite you to <strong>Locus</strong>.</p>
  
  <p>You signed up {{daysAgo}} days ago, and we've been working hard to make sure Locus is ready for you. Here's what's new since you joined the waitlist:</p>
  
  <ul>
    <li>{{feature1}}</li>
    <li>{{feature2}}</li>
    <li>{{feature3}}</li>
  </ul>
  
  <div style="text-align: center; margin: 30px 0;">
    <a href="{{activationUrl}}" style="background-color: #2563eb; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
      Get Started Now
    </a>
  </div>
  
  <p style="font-size: 14px; color: #666;">Your invite link expires in 14 days.</p>
  
  <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <p style="margin: 0; font-weight: 600;">🎁 Early Access Bonus</p>
    <p style="margin: 10px 0 0 0;">As an early adopter, you'll get {{earlyAccessPerk}} — our way of saying thanks for believing in us early.</p>
  </div>
  
  <p>We'd love to hear what you think. Hit reply anytime.</p>
  
  <p>— The Locus Team</p>
  
  <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
    <p>Locus, Inc. | {{companyAddress}}</p>
    <p><a href="{{unsubscribeUrl}}" style="color: #999;">Unsubscribe</a></p>
  </div>
  
</body>
</html>
```

**Plain Text Version:**
```
Your Early Access is Ready

Hi {{firstName}},

Thanks for your patience! We're excited to invite you to Locus.

You signed up {{daysAgo}} days ago, and we've been working hard to make sure Locus is ready for you. Here's what's new since you joined the waitlist:

• {{feature1}}
• {{feature2}}
• {{feature3}}

GET STARTED NOW:
{{activationUrl}}

Your invite link expires in 14 days.

🎁 EARLY ACCESS BONUS
As an early adopter, you'll get {{earlyAccessPerk}} — our way of saying thanks for believing in us early.

We'd love to hear what you think. Hit reply anytime.

— The Locus Team

---
Locus, Inc. | {{companyAddress}}
Unsubscribe: {{unsubscribeUrl}}
```

---

### 3. Welcome Email (Post-Signup)

**Subject Line Options:**
- `Welcome to Locus — here's how to get started`
- `You're all set! Let's build something great`
- `🚀 Your Locus account is ready`

**HTML Version:**
```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Welcome to Locus</title>
</head>
<body style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
  
  <div style="text-align: center; margin-bottom: 30px;">
    <h1 style="color: #2563eb; margin: 0;">Welcome to Locus! 🚀</h1>
  </div>
  
  <p>Hi {{firstName}},</p>
  
  <p>Your account is all set up and ready to go. Here's everything you need to hit the ground running.</p>
  
  <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
  
  <h2 style="color: #1e40af; font-size: 18px;">📋 Quick Start Checklist</h2>
  
  <div style="background-color: #f8fafc; padding: 20px; border-radius: 8px; margin: 20px 0;">
    <p style="margin: 0 0 10px 0;"><strong>1. Complete your profile</strong> (2 min)</p>
    <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">Add your info so your team knows who you are.</p>
    
    <p style="margin: 0 0 10px 0;"><strong>2. Create your first {{primaryAction}}</strong> (5 min)</p>
    <p style="margin: 0 0 15px 0; color: #666; font-size: 14px;">See how Locus works with a quick hands-on example.</p>
    
    <p style="margin: 0 0 10px 0;"><strong>3. Invite your team</strong> (1 min)</p>
    <p style="margin: 0; color: #666; font-size: 14px;">Locus is better together. Add teammates from Settings → Team.</p>
  </div>
  
  <div style="text-align: center; margin: 30px 0;">
    <a href="{{dashboardUrl}}" style="background-color: #2563eb; color: white; padding: 14px 28px; text-decoration: none; border-radius: 6px; font-weight: 600; display: inline-block;">
      Go to Dashboard
    </a>
  </div>
  
  <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
  
  <h2 style="color: #1e40af; font-size: 18px;">📚 Resources</h2>
  
  <ul>
    <li><a href="{{docsUrl}}" style="color: #2563eb;">Documentation</a> — Guides and API reference</li>
    <li><a href="{{tutorialsUrl}}" style="color: #2563eb;">Video tutorials</a> — Step-by-step walkthroughs</li>
    <li><a href="{{communityUrl}}" style="color: #2563eb;">Community</a> — Ask questions, share tips</li>
  </ul>
  
  <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
  
  <h2 style="color: #1e40af; font-size: 18px;">💬 Need Help?</h2>
  
  <p>We're here for you:</p>
  <ul>
    <li><strong>Email:</strong> <a href="mailto:support@locus.io" style="color: #2563eb;">support@locus.io</a></li>
    <li><strong>Chat:</strong> Click the bubble in the bottom-right of your dashboard</li>
    <li><strong>Reply to this email</strong> — we respond within 24 hours</li>
  </ul>
  
  <p>We're thrilled to have you on board. Let's build something great together!</p>
  
  <p>— The Locus Team</p>
  
  <div style="margin-top: 40px; padding-top: 20px; border-top: 1px solid #eee; font-size: 12px; color: #999; text-align: center;">
    <p>Locus, Inc. | {{companyAddress}}</p>
    <p>
      <a href="{{preferencesUrl}}" style="color: #999;">Email preferences</a> · 
      <a href="{{unsubscribeUrl}}" style="color: #999;">Unsubscribe</a>
    </p>
  </div>
  
</body>
</html>
```

**Plain Text Version:**
```
Welcome to Locus! 🚀

Hi {{firstName}},

Your account is all set up and ready to go. Here's everything you need to hit the ground running.

---

📋 QUICK START CHECKLIST

1. Complete your profile (2 min)
   Add your info so your team knows who you are.

2. Create your first {{primaryAction}} (5 min)
   See how Locus works with a quick hands-on example.

3. Invite your team (1 min)
   Locus is better together. Add teammates from Settings → Team.

GO TO DASHBOARD: {{dashboardUrl}}

---

📚 RESOURCES

• Documentation: {{docsUrl}}
• Video tutorials: {{tutorialsUrl}}
• Community: {{communityUrl}}

---

💬 NEED HELP?

• Email: support@locus.io
• Chat: Click the bubble in the bottom-right of your dashboard
• Reply to this email — we respond within 24 hours

We're thrilled to have you on board. Let's build something great together!

— The Locus Team

---
Locus, Inc. | {{companyAddress}}
Email preferences: {{preferencesUrl}}
Unsubscribe: {{unsubscribeUrl}}
```

---

## Template Variables Reference

| Variable | Description | Example |
|----------|-------------|---------|
| `{{firstName}}` | User's first name | Sarah |
| `{{activationUrl}}` | One-time activation link | https://app.locus.io/activate/abc123 |
| `{{dashboardUrl}}` | Main app dashboard | https://app.locus.io/dashboard |
| `{{unsubscribeUrl}}` | One-click unsubscribe | https://app.locus.io/unsubscribe?token=xyz |
| `{{companyAddress}}` | Physical address (CAN-SPAM) | 123 Main St, City, ST 12345 |
| `{{daysAgo}}` | Days since waitlist signup | 42 |
| `{{earlyAccessPerk}}` | Specific early adopter benefit | 3 months free on our Pro plan |
| `{{value_prop}}` | Core value proposition | collaborate on real-time projects |
| `{{primaryAction}}` | Main onboarding action | project / workspace / document |

---

## Implementation Notes

### Postmark Setup

1. Install SDK:
   ```bash
   dotnet add package Postmark
   ```

2. Basic usage:
   ```csharp
   using PostmarkDotNet;
   
   var client = new PostmarkClient("YOUR-SERVER-API-TOKEN");
   
   var response = await client.SendEmailAsync(new PostmarkMessage
   {
       From = "hello@locus.io",
       To = userEmail,
       Subject = "You're in! 🎉 Your Locus beta access is ready",
       HtmlBody = htmlTemplate,
       TextBody = plainTextTemplate,
       Tag = "beta-invite",
       TrackOpens = true,
       TrackLinks = LinkTrackingOptions.HtmlAndText
   });
   ```

3. Use Postmark's template system for dynamic variables:
   ```csharp
   var response = await client.SendEmailWithTemplateAsync(new TemplatedPostmarkMessage
   {
       From = "hello@locus.io",
       To = userEmail,
       TemplateAlias = "beta-invite",
       TemplateModel = new Dictionary<string, object>
       {
           { "firstName", user.FirstName },
           { "activationUrl", GenerateActivationUrl(user) }
       }
   });
   ```

### Email Best Practices Applied

- ✅ Single CTA button (clear action)
- ✅ Mobile-responsive inline styles
- ✅ Plain text fallback for all emails
- ✅ CAN-SPAM compliant (unsubscribe, physical address)
- ✅ Preheader text via hidden content
- ✅ Expiration dates for urgency
- ✅ Reply-to enabled (builds trust)
- ✅ Minimal images (better deliverability)
