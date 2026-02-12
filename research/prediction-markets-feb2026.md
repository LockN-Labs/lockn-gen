# Prediction Markets: Passive Income Strategy Report
**Date:** February 2, 2026 | **Target:** ~$500/month | **Location:** Georgia, US

---

## 1. Platform Comparison

| Platform | Regulation | US Access | Fees | Settlement | Liquidity | API |
|----------|-----------|-----------|------|------------|-----------|-----|
| **Kalshi** | CFTC-regulated DCM ✅ | Full US access ✅ | ~1-3.5% taker fee (formula: `0.035 × C × P × (1-P)`), $0.07-$1.75 per 100 contracts | USD (bank/debit) | **Highest** — $5.8B/mo (Nov 2025), sports-heavy | REST + WebSocket, tiered rate limits |
| **Polymarket** | Acquired QCX DCM license; CFTC no-action letter | **Limited** — US app in invite-only beta, full launch delayed into 2026. Nevada filed complaint Jan 2026 | No trading fee; **2% on winnings** + gas costs | USDC on Polygon | $3.7B/mo, institutional-heavy on politics/macro | Comprehensive — `py-clob-client` Python SDK, CLOB API |
| **PredictIt** | Now fully regulated DCM/DCO (as of Jan 26, 2026!) | Full US access ✅ | 10% on profits + 5% withdrawal fee | USD | Lower than Kalshi/Polymarket but growing with midterms | Limited API |
| **ForecastEx (CME)** | CME Group DCM | Via brokers (Robinhood, Interactive Brokers) | Broker-dependent | USD via brokerage | Growing — FanDuel Predicts partnership, 5 states | Via broker APIs |
| **Manifold** | Unregulated (play money + sweepstakes) | Yes | 5% cash-out fee on Sweepcash | Sweepcash → USD | Low real-money liquidity | Open API |
| **Metaculus** | Not a trading platform | N/A | N/A | Reputation-based | N/A | N/A (forecasting only) |

### Recommendation for Georgia, US
**Primary: Kalshi** — fully legal, best liquidity, fiat on/off ramp, API access.  
**Secondary: PredictIt** — now fully regulated, politics-focused (great for 2026 midterms).  
**Watch: Polymarket US app** — when it launches broadly, the cross-platform arbitrage opportunity with Kalshi will be massive.  
**Access: ForecastEx via Robinhood/IBKR** — adds a third leg for arbitrage.

---

## 2. Current High-Volume Markets (Feb 2026)

**By volume/liquidity:**
1. **Sports** (Kalshi dominant) — NFL playoffs/Super Bowl, NCAA basketball, NBA, Australian Open just resolved
2. **Politics** — 2026 midterm elections ramping up (Senate/House control), Trump administration policy outcomes
3. **Crypto** — BTC price targets (15-min, hourly, daily), ETH milestones
4. **Economics** — Fed rate decisions, inflation data, jobs reports, GDP
5. **Tech/AI** — AGI timelines, company earnings, product launches
6. **Geopolitics** — US-China trade, Ukraine/Russia, tariff outcomes

**Most profitable for consistent trading:** Short-duration crypto markets (BTC 15-min) and economic data releases (binary outcome, resolvable quickly, high volume).

---

## 3. Edge Strategies

### A. Cross-Platform Arbitrage (Best Fit for You)
- Buy YES on platform A + NO on platform B when combined cost < $1.00
- Documented 4-6¢ spreads between Polymarket and Kalshi on same events
- **Key risk:** Resolution criteria can differ! (2024 govt shutdown incident — Polymarket said YES, Kalshi said NO)
- Requires capital on both platforms + fast execution
- Top arbitrageurs made **$4.2M** (top 3 wallets) in 2024-2025 on Polymarket alone

### B. Same-Market Rebalancing
- When YES + NO < $1.00 within a single platform
- Typical spread: 0.5-2%, closes within **200 milliseconds**
- Requires bot with sub-second execution — perfect for your infrastructure

### C. Combinatorial/Logical Arbitrage
- Exploit logical relationships (e.g., "Trump wins" must be ≤ "Republican wins")
- 7,000+ markets with measurable mispricings found in academic study
- Larger spreads, requires deeper analysis — great use case for AI agents

### D. Event Research / Informed Trading
- Use AI to process news faster than the market prices it in
- Economic data releases: position before announcement based on model predictions
- Sports: statistical models outperform casual bettors significantly
- **This is your biggest edge** — your AI infra + agents can monitor news/data 24/7

### E. Market Making
- Quote bid/ask spreads, profit from the spread
- Requires significant capital and sophisticated inventory management
- Institutional players offering $200K salaries for this skill
- Binary payoff structure means you need to hedge carefully

---

## 4. Capital Requirements

| Strategy | Starting Capital | Expected Monthly Return | Notes |
|----------|-----------------|------------------------|-------|
| Cross-platform arbitrage | $5,000-10,000 | 3-8% ($150-800/mo) | Need capital split across platforms |
| Same-market rebalancing (bot) | $2,000-5,000 | 5-15% ($100-750/mo) | High frequency, small per-trade profit |
| Informed event trading | $3,000-8,000 | 5-10% ($150-800/mo) | Higher variance, research-dependent |
| Market making | $10,000-25,000 | 2-5% ($200-1,250/mo) | Most capital-intensive, steadiest |
| **Blended approach** | **$5,000-10,000** | **~$500/mo target** | Combine arbitrage + informed trading |

**Realistic assessment:** $5,000-$10,000 starting capital to reliably hit $500/month. The documented case of $764/day on $200 is an outlier — don't expect that consistently. Academic data shows top performers average 5-15% monthly returns with automation.

---

## 5. Tools & Automation

### APIs
| Platform | API Type | Docs | Key Features |
|----------|----------|------|-------------|
| Kalshi | REST + WebSocket | [docs.kalshi.com](https://docs.kalshi.com) | Market data, order placement, streaming prices, tiered rate limits |
| Polymarket | REST (CLOB) | [docs.polymarket.com](https://docs.polymarket.com) | `py-clob-client` Python SDK, on-chain settlement |
| ForecastEx | Via broker APIs | Robinhood/IBKR APIs | Standard brokerage API access |

### Open-Source Tools
- **[Polymarket-Kalshi Arbitrage Bot](https://github.com/terauss/Polymarket-Kalshi-Arbitrage-bot)** — Python, monitors cross-platform spreads
- **[NautilusTrader](https://nautilustrader.io/)** — Institutional-grade, Polymarket CLOB integration, sub-ms latency
- **[EventArb.com](https://www.eventarb.com/)** — Real-time cross-platform arbitrage calculator
- **[Awesome Prediction Market Tools](https://github.com/aarora4/Awesome-Prediction-Market-Tools)** — Curated directory of everything
- **[OctoBot](https://www.octobot.cloud/)** — Visual strategy builder with Polymarket support

### Your Custom Stack (Recommended)
Given your infrastructure (Threadripper Pro, 96GB VRAM, 256GB RAM):

1. **Data Layer:** Kalshi WebSocket + Polymarket CLOB streaming → local database
2. **Analysis Layer:** AI agent (local GLM-4 or Claude) for news processing, probability estimation, logical relationship detection
3. **Execution Layer:** Python/Rust bot for order placement on both platforms
4. **Monitoring:** Telegram/Slack alerts for opportunities above threshold
5. **Edge:** Use your local LLM to scan news feeds and estimate true probabilities faster than markets adjust

---

## 6. Risks & Pitfalls

### Regulatory (Georgia-specific)
- **Kalshi:** Fully legal, CFTC-regulated. However, state gaming boards are filing challenges in 2026 — Nevada already filed against Polymarket. Georgia hasn't acted yet but monitor this.
- **Polymarket:** US access still in limbo. Using VPN to access global Polymarket = **technically violating TOS and potentially CFTC settlement terms**. Don't do it.
- **Tax:** Prediction market gains are taxable. Kalshi issues 1099s. Track everything.

### Platform Risk
- **Resolution disputes:** Platforms can resolve identical events differently. The 2024 govt shutdown case is a cautionary tale. Always verify resolution criteria match before cross-platform arb.
- **Liquidity risk:** You may not be able to exit positions before resolution if the market thins out.
- **Counterparty risk:** Polymarket is crypto-native — smart contract risk exists. Kalshi is CFTC-regulated with clearing.

### Strategy Risk
- **Speed competition:** Sub-200ms arbitrage windows mean you're competing with institutional bots. Your edge is NOT speed — it's **information processing** via AI.
- **Spread compression:** As more capital enters ($5.6B institutional in 2025), easy arbitrage opportunities shrink.
- **Correlation risk:** Don't load up on related positions (e.g., all political markets that correlate).
- **Overconfidence in models:** AI probability estimates can be systematically wrong. Size positions conservatively.

### Common Mistakes
1. Not verifying resolution criteria match across platforms before arbitrage
2. Ignoring fees in profit calculations (Kalshi's 3.5% + PredictIt's 10%+5% can eat spreads)
3. Concentrating too much capital in single events
4. Treating prediction markets like sports betting (no edge = negative EV after fees)
5. Neglecting the time value of money — capital locked until resolution

---

## 7. Actionable Plan

### Week 1-2: Setup
- [ ] Open Kalshi account, verify, fund with $3,000
- [ ] Open PredictIt account, fund with $1,000
- [ ] Set up Polymarket wallet (for when US access expands), fund with $1,000 USDC
- [ ] Request Kalshi API access, test with paper trades
- [ ] Clone and test Polymarket-Kalshi arbitrage bot

### Week 3-4: Build
- [ ] Set up Kalshi WebSocket data feed → local database
- [ ] Build news monitoring agent (RSS + Twitter + economic calendar)
- [ ] Implement probability estimation pipeline using local LLM
- [ ] Create Slack alerting for spread opportunities > 3%

### Month 2: Go Live
- [ ] Start with small positions ($50-100 per trade)
- [ ] Focus on economic data releases (Fed, CPI, jobs) — binary, fast-resolving
- [ ] Run arbitrage bot on BTC short-duration markets
- [ ] Track P&L rigorously, refine models

### Month 3+: Scale
- [ ] Increase position sizes as track record builds
- [ ] Add ForecastEx via Robinhood as third arbitrage leg
- [ ] Build combinatorial arbitrage detection (AI-powered logical consistency checker)
- [ ] Target $500/month consistently before scaling further

---

## Key Takeaway

Your biggest edge is **not** speed (institutions have you beat) — it's **AI-powered information processing**. Use your local inference stack to:
1. Monitor news/data feeds 24/7
2. Estimate true probabilities before markets adjust
3. Detect logical inconsistencies across related markets
4. Automate execution on the opportunities your models identify

With $5,000-$10,000 starting capital and disciplined execution, $500/month is achievable within 2-3 months of optimization. The prediction market industry hit $37B in volume in 2025 and is still growing — the opportunity window is open but narrowing as institutional capital floods in.
