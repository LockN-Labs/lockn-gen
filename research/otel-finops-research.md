# OpenTelemetry GenAI FinOps Research — LockN Labs

**Date:** February 2, 2026  
**Purpose:** Instrumentation strategy for AI agent FinOps observability product

---

## 1. OpenTelemetry GenAI Semantic Conventions (Current State)

**Status:** `Development` (not yet stable — still evolving, but widely adopted)

The OTel GenAI semantic conventions are maintained at [opentelemetry.io/docs/specs/semconv/gen-ai/](https://opentelemetry.io/docs/specs/semconv/gen-ai/) and cover four signal types:

### 1.1 Token Usage

**Span attributes (per-request):**
- `gen_ai.usage.input_tokens` — int, number of prompt/input tokens (Recommended)
- `gen_ai.usage.output_tokens` — int, number of completion/response tokens (Recommended)

**Metric: `gen_ai.client.token.usage`**
- Instrument: Histogram
- Unit: `{token}`
- Required attributes: `gen_ai.operation.name`, `gen_ai.provider.name`, `gen_ai.token.type` (input|output)
- Conditional: `gen_ai.request.model`
- Recommended: `gen_ai.response.model`
- Bucket boundaries: `[1, 4, 16, 64, 256, 1024, 4096, 16384, 65536, 262144, 1048576, 4194304, 16777216, 67108864]`
- **Important:** When systems report both *used* and *billable* tokens, instrumentation MUST report billable tokens.

**No `total_tokens` attribute** — you derive it from input + output.

### 1.2 Model Identification

- `gen_ai.request.model` — requested model name (e.g., `gpt-4`)
- `gen_ai.response.model` — actual model that responded (e.g., `gpt-4-0613`)
- `gen_ai.provider.name` — well-known values: `openai`, `anthropic`, `aws.bedrock`, `azure.ai.openai`, `gcp.gemini`, `gcp.vertex_ai`, `cohere`, `deepseek`, `groq`, `mistral_ai`, `perplexity`, `x_ai`, `ibm.watsonx.ai`
- `server.address` + `server.port` — for self-hosted/proxy identification

### 1.3 Tool/Function Call Tracing

**Operation name:** `execute_tool` is a well-known `gen_ai.operation.name` value.

**Agent span conventions** ([gen-ai-agent-spans](https://opentelemetry.io/docs/specs/semconv/gen-ai/gen-ai-agent-spans/)) define:
- `create_agent` — agent creation span
- `invoke_agent` — agent invocation span  
- `execute_tool` — tool execution span

**Agent attributes:**
- `gen_ai.agent.id` — unique agent identifier
- `gen_ai.agent.name` — human-readable name
- `gen_ai.agent.description` — free-form description

**Tool definitions captured via:**
- `gen_ai.tool.definitions` (Opt-In) — full JSON of available tools
- `gen_ai.input.messages` / `gen_ai.output.messages` (Opt-In) — capture tool_call and tool_call_response in message history

### 1.4 Agent Span Hierarchy

The conventions support natural parent-child trace structure:

```
invoke_agent "Main Agent"           ← parent span
  ├── chat "gpt-4"                  ← LLM inference span
  ├── execute_tool "search_db"      ← tool execution span
  ├── chat "gpt-4"                  ← second LLM call
  ├── invoke_agent "Sub Agent"      ← nested agent span
  │   ├── chat "claude-3"
  │   └── execute_tool "fetch_url"
  └── chat "gpt-4"                  ← final synthesis
```

Span kind: `CLIENT` for remote calls, `INTERNAL` for in-process.

### 1.5 Cost Attribution

**Not standardized yet.** The conventions provide the building blocks:
- Token counts (input/output) per request
- Model identity (request + response model)
- Provider identity
- Operation duration (`gen_ai.client.operation.duration` — Required histogram, seconds)

**Cost must be computed externally** by joining token counts × model pricing tables. This is a clear product opportunity.

### 1.6 Additional Metrics

- `gen_ai.client.operation.duration` — **Required** histogram (seconds), buckets: `[0.01 → 81.92]`
- `gen_ai.server.request.duration` — server-side duration
- `gen_ai.server.time_per_output_token` — server TTFT/TBT metrics

---

## 2. Existing OTel Instrumentation Libraries

### 2.1 OpenLLMetry (Traceloop)

**Repo:** [github.com/traceloop/openllmetry](https://github.com/traceloop/openllmetry)  
**Languages:** Python (primary), JS/TS, Ruby (alpha)  
**License:** Apache 2.0

**What it covers:**
- Auto-instrumentation for 20+ LLM providers: OpenAI, Anthropic, Cohere, HuggingFace, Bedrock, VertexAI, etc.
- Token usage, latency, cost tracking per request
- Prompt/completion content capture (opt-in)
- Framework support: LangChain, LlamaIndex, Haystack, CrewAI
- VectorDB tracing: Pinecone, Chroma, Weaviate, Qdrant
- Pure OTel output — works with any OTel-compatible backend

**Integration pattern:**
```python
from traceloop.sdk import Traceloop
Traceloop.init()  # Auto-patches supported libraries
```

**Key strength for LockN:** Already follows GenAI semantic conventions closely. Traceloop led the OTel LLM semantic convention working group. Mature, production-ready.

**Limitation:** No built-in cost computation — just token counts. Dashboard/visualization is via Traceloop's paid product or external backends.

### 2.2 OpenLIT

**Repo:** [github.com/openlit/openlit](https://github.com/openlit/openlit)  
**License:** Apache 2.0

**What it covers:**
- Auto-instrumentation for 50+ integrations: LLMs, VectorDBs, agent frameworks, GPUs
- Built-in dashboard (self-hosted UI with ClickHouse backend)
- GPU monitoring (NVIDIA)
- Guardrails, evaluations, prompt management, vault, playground
- OTel-native output — vendor neutral

**Integration:**
```python
import openlit
openlit.init()  # That's it
```

**Key strength:** Most complete open-source package — includes its own UI/dashboard. Good reference architecture for what a FinOps product looks like.

**Limitation:** Tries to be everything (observability + guardrails + eval + prompt mgmt). Jack of all trades. FinOps/cost is not the primary focus.

### 2.3 LangSmith vs LangFuse vs OTel-Native

| Feature | LangSmith | LangFuse | OTel-Native (OpenLLMetry/OpenLIT) |
|---------|-----------|----------|-----------------------------------|
| **Vendor lock-in** | LangChain ecosystem | Framework-agnostic | Framework-agnostic |
| **Protocol** | Proprietary | OTel-compatible (OTLP ingestion) | Native OTel/OTLP |
| **Self-hosting** | No (SaaS only) | Yes (open-source) | Yes |
| **Token tracking** | Yes | Yes | Yes |
| **Cost tracking** | Basic | Yes (model pricing tables) | Manual (tokens only) |
| **Agent tracing** | Excellent for LangChain | Good (manual spans) | Good (auto-instrument) |
| **Eval/scoring** | Built-in | Built-in | External |
| **OTel export** | No | Yes (OTel ingestion) | Native |
| **Pricing** | Free tier → $400/mo+ | Open-source / cloud $59/mo+ | Free |

**LangFuse** is the closest competitor model to what LockN could build. It's open-source, OTel-compatible, and framework-agnostic. But it's focused on *developer observability*, not *FinOps*.

**LangSmith** is LangChain-locked. Not a threat for framework-agnostic FinOps.

### 2.4 Self-Hosted Inference: vLLM & llama.cpp

**vLLM:**
- **Native OTel support** — built-in tracing and Prometheus metrics
- Set `OTEL_EXPORTER_OTLP_ENDPOINT` and `OTEL_SERVICE_NAME` env vars
- Exports: request traces with token counts, latency, model info
- Prometheus metrics: `vllm:num_requests_running`, `vllm:avg_generation_throughput_toks_per_s`, etc.
- **Limitation:** Only exports token counts and latency to OTel traces; prompt/completion content requires separate capture
- Production Stack has full Kubernetes OTel integration guide

**llama.cpp:**
- **No native OTel support** as of Feb 2026
- **llama-stack** (Meta's higher-level framework) has OTel telemetry: `llama_stack_tokens_total` counter, OpenTelemetry collector integration
- For raw llama.cpp server: must use proxy/wrapper approach (e.g., liteLLM proxy with OTel, or custom middleware)
- Community interest exists but no merged PR for native OTel in llama.cpp server

**LiteLLM** is a key enabler: acts as an OpenAI-compatible proxy in front of any model (including llama.cpp, Ollama, vLLM) and has native OTel integration. Good architectural pattern for LockN.

---

## 3. Token Compression Measurement

### 3.1 Instrumentation Strategy (Before/After)

**Custom span attributes for compression:**
```
lockn.compression.strategy = "context_distillation" | "prompt_caching" | "semantic_dedup" | "summary_injection"
lockn.compression.input_tokens_original = 8500     # before compression
lockn.compression.input_tokens_compressed = 3200   # after compression
lockn.compression.ratio = 0.376                     # compressed/original
lockn.compression.cache_hit = true                  # for prompt caching
lockn.compression.quality_score = 0.94              # output quality retention
```

**Implementation pattern:**
1. **Wrapper/middleware approach:** Intercept LLM calls, measure original context size, apply compression, measure compressed size, forward to model
2. **A/B trace tagging:** Tag traces with `lockn.experiment.group = "control" | "compressed"` for side-by-side comparison
3. **Use OTel resource attributes** for experiment metadata: `service.version`, `deployment.environment`

### 3.2 Key Metrics That Prove Value

| Metric | Formula | What It Proves |
|--------|---------|----------------|
| **Token Savings Rate** | `1 - (compressed_tokens / original_tokens)` | Raw efficiency gain |
| **Cost Savings ($)** | `tokens_saved × price_per_token` | Direct financial impact |
| **Cost Savings (%)** | Per-agent, per-task, per-org roll-up | Executive-level ROI |
| **Latency Improvement** | `avg(duration_compressed) / avg(duration_original)` | Speed benefit |
| **Quality Retention** | `eval_score_compressed / eval_score_original` | No degradation proof |
| **Cache Hit Rate** | `cache_hits / total_requests` | Caching effectiveness |
| **Context Window Utilization** | `tokens_used / max_context_window` | Headroom created |
| **Requests Enabled** | Requests that *would have exceeded* context window | Unlocked capability |

### 3.3 A/B Comparison Dashboard Design

**Panel 1: Cost Waterfall**
- Stacked bar: Original cost vs. Compressed cost vs. Savings, per day/week
- Cumulative savings line overlay

**Panel 2: Token Distribution**
- Histogram comparing input token distributions: control vs compressed
- Percentile lines (p50, p95, p99)

**Panel 3: Quality Scatter**
- X-axis: compression ratio, Y-axis: quality score
- Each dot is a request — shows the quality/compression tradeoff frontier

**Panel 4: Latency CDF**
- Cumulative distribution: time-to-first-token and total duration
- Control vs compressed overlaid

**Panel 5: Per-Agent Savings Table**
- Agent name, total tokens (before/after), cost (before/after), quality score, savings %

---

## 4. Architecture for a FinOps Product

### 4.1 Reference Architecture

```
┌─────────────────────────────────────────────────────────┐
│                    Agent Applications                     │
│  OpenClaw │ CrewAI │ LangGraph │ LlamaIndex │ Custom     │
└────────────────────────┬────────────────────────────────┘
                         │ OTel SDK (auto-instrumented)
                         │ OpenLLMetry / OpenLIT / custom
                         ▼
┌─────────────────────────────────────────────────────────┐
│              OTel Collector Pipeline                      │
│                                                           │
│  Receivers:  OTLP (gRPC :4317, HTTP :4318)               │
│  Processors:                                              │
│    ├── batch (performance)                                │
│    ├── memory_limiter                                     │
│    ├── attributes (enrich with cost data)     ◄── LockN  │
│    ├── transform (compute derived metrics)    ◄── LockN  │
│    └── filter (sampling, PII redaction)                   │
│  Exporters:                                               │
│    ├── clickhouse (traces + metrics)                      │
│    ├── prometheus (real-time metrics)                      │
│    └── debug (development)                                │
└─────────────────────────────────────────────────────────┘
                         │
            ┌────────────┼────────────┐
            ▼            ▼            ▼
     ┌───────────┐ ┌──────────┐ ┌──────────┐
     │ClickHouse │ │Prometheus│ │  S3/Blob │
     │(traces,   │ │(real-time│ │(long-term│
     │ spans,    │ │ metrics, │ │ archive) │
     │ raw data) │ │ alerting)│ │          │
     └─────┬─────┘ └────┬─────┘ └──────────┘
           │             │
           └──────┬──────┘
                  ▼
     ┌─────────────────────┐
     │   LockN Dashboard   │
     │   (Grafana-based)   │
     │                     │
     │ • Cost attribution  │
     │ • Token analytics   │
     │ • Compression ROI   │
     │ • Agent hierarchy   │
     │ • Budget alerts     │
     └─────────────────────┘
```

### 4.2 Storage Backend Recommendation

**Primary: ClickHouse**
- Column-oriented, extremely fast for analytical queries on trace/span data
- Native OTel Collector exporter (`clickhouse` exporter)
- Handles high-cardinality data (trace IDs, span attributes) well
- Compression ratios 10-30x on trace data
- SQL interface — easy to build dashboards and custom queries
- Used by: Signoz, OpenLIT, Uptrace (all OTel-native platforms)

**Secondary: Prometheus + Grafana**
- Real-time metrics, alerting, dashboards
- `gen_ai.client.token.usage` and `gen_ai.client.operation.duration` → Prometheus histograms
- Grafana for visualization layer (connects to both ClickHouse and Prometheus)

**Why not just Prometheus?** Traces require a different storage model. Prometheus is metrics-only. ClickHouse handles both traces and metrics, but Prometheus has better real-time alerting.

### 4.3 OTel Collector Custom Processor (LockN Secret Sauce)

Build a custom OTel Collector processor that:
1. **Enriches spans with cost data** — looks up model pricing table, computes `lockn.cost.input`, `lockn.cost.output`, `lockn.cost.total` from token counts
2. **Aggregates per-agent costs** — maintains running totals per `gen_ai.agent.id`
3. **Detects anomalies** — token usage spikes, runaway agents
4. **Enforces budgets** — can drop/alert on spans that exceed per-agent or per-org budgets

This processor is the core IP. Everything else (storage, dashboards) is commodity.

### 4.4 Framework-Agnostic Strategy

**Layer 1: OTel SDK instrumentation** (framework-specific, thin)
- Use OpenLLMetry for supported frameworks (LangChain, LlamaIndex, CrewAI)
- Build custom instrumentors for unsupported frameworks (OpenClaw, AutoGen)
- All output standard OTLP — framework differences are absorbed here

**Layer 2: OTel Collector** (framework-agnostic)
- Everything above the collector is the same regardless of framework
- Custom processors, storage, dashboards — all framework-agnostic

**Layer 3: LiteLLM proxy** (optional, for self-hosted models)
- Proxy in front of llama.cpp, Ollama, vLLM
- Adds OTel instrumentation to any model endpoint
- Standardizes the API surface

**Key integration points to build:**
- `lockn-otel-openclaw` — OpenClaw gateway middleware
- `lockn-otel-crewai` — CrewAI callback handler  
- `lockn-otel-langgraph` — LangGraph tracer
- `lockn-otel-generic` — Generic OpenAI-compatible client wrapper
- `lockn-collector-processor` — OTel Collector cost enrichment processor

---

## 5. Competitive Landscape

### 5.1 Who's Selling Agent Observability Today

| Company | Focus | Pricing | OTel Native? | FinOps Focus? |
|---------|-------|---------|--------------|---------------|
| **Helicone** | LLM proxy + logging | $25/mo flat | No (proxy-based) | Basic cost tracking |
| **LangSmith** | LangChain observability | Free → $400/mo | No (proprietary) | Token counting only |
| **LangFuse** | Open-source LLM obs | Free → $59/mo | OTel-compatible | Basic cost per trace |
| **Traceloop** | OpenLLMetry commercial | Enterprise pricing | Yes (OTel-native) | Token + latency |
| **OpenLIT** | Open-source full-stack | Free (self-hosted) | Yes (OTel-native) | Basic |
| **Portkey** | AI gateway + routing | Usage-based | No (gateway) | Budget limits |
| **Arize/Phoenix** | ML + LLM observability | Free → enterprise | OTel-compatible | Minimal |
| **AgentOps** | Agent-specific monitoring | Free → $99/mo | No | Cost tracking |
| **Braintrust** | Eval + observability | Free → enterprise | Partial | Basic |
| **Datadog** | Enterprise APM + GenAI | $$$$ | Yes (OTel ingestion) | Yes (enterprise) |
| **New Relic** | Enterprise APM + GenAI | Usage-based | Yes (OTel ingestion) | Basic |

### 5.2 What's Missing from Current Offerings

1. **True FinOps for AI** — Nobody is doing proper cost attribution at the agent/task/workflow level with budget governance. Existing tools show costs per-request but don't answer "how much did this customer's support ticket cost across 47 agent calls?"

2. **Compression ROI measurement** — Zero products measure the impact of token compression, prompt caching, or context optimization. No before/after comparison tooling exists.

3. **Cross-framework agent hierarchy** — Most tools trace within one framework. Nobody traces a workflow that spans OpenClaw → CrewAI → raw API calls as a unified cost center.

4. **Budget governance** — Portkey has basic limits, but nobody does proper FinOps-style: budgets, forecasting, anomaly detection, chargeback/showback reports, approval workflows for expensive operations.

5. **Self-hosted model cost accounting** — When running llama.cpp/vLLM on your own GPUs, what's the *actual* cost per token including compute, memory, electricity? Nobody computes this.

6. **OTel-native cost enrichment** — Nobody ships an OTel Collector processor that enriches spans with cost data at collection time. Everyone does it in the application layer or dashboard layer.

### 5.3 The Gap LockN Can Own

**Position: "FinOps for AI Agents"** — not another observability platform, but the *financial intelligence layer* that sits on top of any observability stack.

**Core differentiators:**

1. **Cost enrichment at the OTel Collector level** — Works with ANY framework, ANY backend. Ship a processor, not a platform.
   
2. **Compression ROI proof** — Built-in A/B measurement for token compression strategies. "We saved you $47,000 this month" with evidence.

3. **Agent-level cost attribution** — Roll up costs from individual LLM calls → tool executions → agent invocations → tasks → workflows → customers → business units.

4. **Budget governance** — Set budgets per agent/team/customer. Alert, throttle, or block when approaching limits. Approval workflows for expensive operations.

5. **Self-hosted model TCO** — Calculate true cost-per-token for self-hosted models (GPU amortization, electricity, cooling, staff time) and compare against API providers.

6. **Framework-agnostic by design** — OTel Collector processor + thin SDK instrumentors. Not locked to any framework.

**Go-to-market:**
- Open-source the OTel Collector processor (community + adoption)
- Sell the dashboard, analytics, governance, and compression optimization as SaaS/on-prem
- Bundle with LockN compression tools: "Save X%, here's the proof"

---

## 6. Specific Libraries & Integration Points

### Key Dependencies

| Component | Library | Version/Status |
|-----------|---------|---------------|
| OTel Python SDK | `opentelemetry-api`, `opentelemetry-sdk` | 1.29+ (stable) |
| OTel Collector | `otelcol-contrib` | 0.115+ (includes ClickHouse exporter) |
| GenAI conventions | `opentelemetry-semantic-conventions` | 0.52+ (gen_ai attributes) |
| OpenLLMetry | `traceloop-sdk` | 0.38+ |
| OpenLIT | `openlit` | 1.34+ |
| ClickHouse | `clickhouse-server` | 24.8+ (OTel schema support) |
| Grafana | `grafana` + `clickhouse-datasource` | 11.x |
| LiteLLM | `litellm` | 1.55+ (OTel integration) |
| vLLM | `vllm` | 0.7+ (native OTel) |
| LangFuse | `langfuse` | 2.x (OTel ingestion) |

### Custom Components to Build

1. **`lockn-otel-processor`** — OTel Collector processor (Go)
   - Cost enrichment from pricing table
   - Agent cost aggregation
   - Budget enforcement
   - Anomaly detection

2. **`lockn-sdk-python`** — Python SDK
   - Compression measurement decorators
   - A/B experiment tagging
   - Custom span attributes (`lockn.*`)
   - Framework-specific instrumentors

3. **`lockn-pricing-service`** — Model pricing API
   - Real-time pricing for all major providers
   - Self-hosted model TCO calculator
   - Historical pricing for accurate retroactive costing

4. **`lockn-dashboard`** — Grafana dashboards (JSON provisioning)
   - Cost attribution views
   - Compression ROI panels
   - Budget governance
   - Agent hierarchy explorer

---

## 7. Quick Start Architecture (MVP)

For the fastest path to a demo:

```bash
# 1. OTel Collector with ClickHouse
docker compose up -d clickhouse otel-collector grafana

# 2. Instrument an agent app
pip install traceloop-sdk  # or openlit
# Point OTEL_EXPORTER_OTLP_ENDPOINT=http://localhost:4318

# 3. Add LockN cost enrichment
# Custom processor in OTel Collector config enriches spans with cost

# 4. Query in Grafana
# ClickHouse datasource → custom dashboards
```

**MVP scope:** Cost per request, cost per agent, daily spend trends, token usage breakdown by model. This alone is more than most tools offer for FinOps.
