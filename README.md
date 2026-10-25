# Awesome Agent Ops

[![CI](https://github.com/StefanYasin/awesome-agent-ops/actions/workflows/ci.yml/badge.svg)](https://github.com/StefanYasin/awesome-agent-ops/actions/workflows/ci.yml)

Tools for running AI agents in production: tracing, evals, guardrails, sandboxes, MCP security, fleet orchestration, cost control and incident response.

This is not a list of agents. If you want frameworks for building agents, [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) already covers that ground. This list starts after the agent exists and someone has to operate it.

I keep the scope narrow. A project belongs here if it helps you observe an agent, test it, constrain what it can do, run many of them, meter their usage or recover when they fail. Every entry links to a public repository, and every link is checked by CI on each push and by a weekly review job.

**88 entries across 8 sections. All links resolved when this version was published.**

## Contents

- [Observability and tracing](#observability-and-tracing) (12)
- [Evaluation and testing](#evaluation-and-testing) (13)
- [Guardrails and safety](#guardrails-and-safety) (9)
- [Sandboxes and permissions](#sandboxes-and-permissions) (13)
- [MCP security and gateways](#mcp-security-and-gateways) (13)
- [Fleet management and orchestration](#fleet-management-and-orchestration) (11)
- [Cost and usage tracking](#cost-and-usage-tracking) (7)
- [Incident response](#incident-response) (10)
- [What belongs here](#what-belongs-here)
- [Maintained by](#maintained-by)
- [Contributing](#contributing)
- [License](#license)

## Observability and tracing

You cannot debug an agent from a chat transcript. These projects capture spans, tool calls, token counts and outcomes, either through OpenTelemetry or a proxy.

- [AgentOps](https://github.com/AgentOps-AI/agentops) - Session-level tracing for agents: replays, cost totals and failure timelines from a two-line SDK hook.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Open-source trace viewer and eval workbench that speaks OpenTelemetry, so agent spans arrive without a proprietary agent SDK.
- [Helicone](https://github.com/Helicone/helicone) - Proxy-based LLM observability that records requests, tokens, latency and cache hits without changing application code.
- [Langfuse](https://github.com/langfuse/langfuse) - Self-hostable tracing, prompt versioning and evaluation for LLM apps, with per-span cost and latency breakdowns.
- [LangSmith Python SDK](https://github.com/langchain-ai/langsmith-python) - Official client for LangSmith's hosted tracing and evaluation service, including run trees and dataset experiments.
- [Langtrace](https://github.com/Scale3-Labs/langtrace) - OpenTelemetry-native tracing for LLM calls and agent steps, with a self-hosted collector and dashboard.
- [Ollama Watch](https://github.com/StefanYasin/ollama-watch) - Samples a local Ollama daemon on a timer, stores model residency and VRAM history in SQLite, then renders digests and a self-refreshing page.
- [OpenLIT](https://github.com/openlit/openlit) - OpenTelemetry-native instrumentation and a self-hosted dashboard for tracing, cost and evaluation of LLM and agent workloads.
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - OpenTelemetry instrumentation for LLM frameworks and vector stores, so traces land in whatever backend you already run.
- [Opik](https://github.com/comet-ml/opik) - Comet's open-source tracing and evaluation stack for LLM and agent runs, deployable locally or on their cloud.
- [Pydantic Logfire](https://github.com/pydantic/logfire) - OTel-based observability with first-class Pydantic AI and LLM spans, plus SQL querying over collected traces.
- [Weave](https://github.com/wandb/weave) - Weights & Biases toolkit for tracing, evaluating and comparing agent runs, with a UI tied to experiment tracking.

## Evaluation and testing

Evals are the regression tests of an agent. The tools here range from prompt assertions to full agent benchmarks.

- [AgentBench](https://github.com/THUDM/AgentBench) - Benchmark suite that puts models through multi-environment agent tasks such as OS, database and web navigation.
- [DeepEval](https://github.com/confident-ai/deepeval) - Pytest-style evaluation framework with metrics for hallucination, faithfulness, answer relevance and agent task completion.
- [Giskard](https://github.com/Giskard-AI/giskard-oss) - Testing library and scan engine for LLM agents, covering prompt injection, harmful output and RAG quality regressions.
- [Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) - UK AI Security Institute's eval framework, with solvers, scorers and tool use for agentic benchmarks.
- [LightEval](https://github.com/huggingface/lighteval) - Hugging Face's benchmark runner for local models and hosted endpoints, with configurable few-shot and generation settings.
- [LM Evaluation Harness](https://github.com/EleutherAI/lm-evaluation-harness) - EleutherAI's reference harness for few-shot benchmarks, widely used to produce comparable model scores.
- [OpenAI Evals](https://github.com/openai/evals) - Framework and public registry for writing evals as YAML or Python and comparing model outputs over time.
- [promptfoo](https://github.com/promptfoo/promptfoo) - CLI and library for testing prompts, agents and RAG pipelines, with assertions, CI output and red-team probes.
- [Ragas](https://github.com/vibrantlabsai/ragas) - Metrics library for RAG and agent evaluation, including context precision, faithfulness and response relevancy.
- [SWE-bench](https://github.com/SWE-bench/SWE-bench) - Benchmark of real GitHub issues that measures whether a coding agent can produce a patch that passes the project's tests.
- [tau-bench](https://github.com/sierra-research/tau-bench) - Benchmark for tool-using agents in customer service scenarios, scoring task success against simulated users.
- [Terminal-Bench](https://github.com/harbor-framework/terminal-bench-1) - Containerized benchmark of terminal tasks that tests whether an agent can operate a shell end to end.
- [TruLens](https://github.com/truera/trulens) - Adds scored feedback functions and comparison dashboards on top of recorded LLM and agent traces.

## Guardrails and safety

Guardrails check inputs, outputs and tool calls before damage is done. None of them replace a sandbox.

- [AI-Infra-Guard](https://github.com/Tencent/AI-Infra-Guard) - Tencent's red-team platform for AI infrastructure, with scans for agents, MCP servers, skills and model endpoints.
- [Garak](https://github.com/NVIDIA/garak) - NVIDIA's vulnerability scanner for LLMs, with probe families for jailbreaks, data leakage and prompt injection.
- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - Output validation framework built around RAIL specs and a library of validators for structure, PII and safety.
- [Invariant](https://github.com/invariantlabs-ai/invariant) - Rule-based guardrail layer that sits between an agent and its LLM or MCP servers and inspects tool calls in flight.
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - Programmable conversation rails using Colang, with input, output and retrieval checks plus tool-call policies.
- [Presidio](https://github.com/data-privacy-stack/presidio) - Detects and redacts personal data in text and images, with pluggable recognizers and anonymizers for pre- or post-processing pipelines.
- [PurpleLlama](https://github.com/meta-llama/PurpleLlama) - Meta's umbrella for open trust and safety tooling, including LlamaFirewall for prompt injection defense and CyberSecEval.
- [PyRIT](https://github.com/microsoft/PyRIT) - Microsoft's risk identification framework for red-teaming generative AI, with orchestrators, converters and scoring.
- [Vigil LLM](https://github.com/deadbits/vigil-llm) - Prompt injection and jailbreak detector that combines vector similarity, transformers and heuristic scanners.

## Sandboxes and permissions

Assume the model will eventually run the wrong command. These projects limit the blast radius by isolating execution or controlling which identity and tools an agent can use.

- [Agent Sandbox](https://github.com/kubernetes-sigs/agent-sandbox) - Kubernetes CRD and controller for running each agent in its own isolated, stateful pod with a stable identity.
- [Agent Surface Report](https://github.com/StefanYasin/agent-surface-report) - Audits a Windows host from an agent's point of view, mapping persistence hooks, stored logins, exposed ports and shell restrictions before you hand over the keyboard.
- [Bubblewrap](https://github.com/containers/bubblewrap) - Builds a new mount and user namespace for a command, which is how Flatpak and similar tools confine untrusted apps without root.
- [Cedar](https://github.com/cedar-policy/cedar) - AWS's authorization language and policy engine for fine-grained decisions about which agent or tool may perform an action.
- [E2B](https://github.com/e2b-dev/E2B) - Cloud sandboxes with filesystem, process and network control, designed for running model-generated code.
- [Firecracker](https://github.com/firecracker-microvm/firecracker) - MicroVM monitor from AWS that gives each workload a lightweight kernel boundary, the base under many code sandboxes.
- [gVisor](https://github.com/google/gvisor) - User-space application kernel that intercepts syscalls, adding a strong isolation layer around containerized agent code.
- [Kata Containers](https://github.com/kata-containers/kata-containers) - Container runtime that places each pod inside a lightweight VM, trading a little speed for a harder boundary.
- [LLM Sandbox](https://github.com/vndee/llm-sandbox) - Python library that runs generated code in a disposable container with limits on time, memory and network.
- [Microsandbox](https://github.com/superradcompany/microsandbox) - Local-first microVM runtime with a small API for starting isolated agent workspaces on a laptop or server.
- [nsjail](https://github.com/google/nsjail) - Linux process jail that combines namespaces, cgroups, rlimits and seccomp filters to contain a single command.
- [Open Policy Agent](https://github.com/open-policy-agent/opa) - General-purpose policy engine using Rego, commonly placed in front of tool calls and infrastructure APIs to enforce rules.
- [OpenFGA](https://github.com/openfga/openfga) - Zanzibar-style authorization service for modeling per-user and per-agent permissions over shared resources.

## MCP security and gateways

MCP gave agents a standard way to reach tools, and a standard way to inherit too much access. These servers, proxies and scanners put a boundary around that surface.

- [Agent Gateway](https://github.com/agentgateway/agentgateway) - Rust proxy for agent and MCP traffic, with Kubernetes-native config, auth and per-tool routing.
- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) - Docker CLI plugin that runs MCP servers as containers and exposes a single managed endpoint to clients.
- [IBM ContextForge](https://github.com/IBM/mcp-context-forge) - Registry and proxy that federates MCP, A2A and REST APIs behind one governed endpoint with OTel tracing.
- [MCP Firewall](https://github.com/StefanYasin/mcp-firewall) - Sits in the stdio path between client and server, enforcing a YAML allowlist, per-server call limits and an append-only JSONL record of tool traffic.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Browser-based debugger for MCP servers: list tools and resources, call them, and inspect the raw protocol traffic.
- [MCP Jungle](https://github.com/mcpjungle/MCPJungle) - Registry and proxy for discovering, grouping and exposing MCP servers through one endpoint.
- [MCP Remote](https://github.com/punkpeye/mcp-remote) - Bridge that lets stdio-only MCP clients reach remote HTTP or SSE servers without a local gateway.
- [MCP Shield](https://github.com/riseandignite/mcp-shield) - Scanner for MCP servers that flags tool poisoning, exfiltration channels and cross-origin escalation.
- [MetaMCP](https://github.com/metatool-ai/metamcp) - Composes several MCP servers behind one endpoint, with middleware, namespacing and a UI for wiring them together.
- [Microsoft MCP Gateway](https://github.com/microsoft/mcp-gateway) - Kubernetes reverse proxy and control plane that routes each MCP request to a ready server and manages its lifecycle.
- [Snyk Agent Scan](https://github.com/snyk/agent-scan) - Scans installed agents, MCP servers and skills for prompt injection and known vulnerabilities, formerly mcp-scan.
- [Supergateway](https://github.com/supercorp-ai/supergateway) - Bridges MCP transports in both directions, putting a stdio server behind HTTP or SSE, or reaching a remote server from a stdio-only client.
- [ToolHive](https://github.com/stacklok/toolhive) - Runs each MCP server in its own container with per-request identity, access policy and operational visibility.

## Fleet management and orchestration

One agent is a process. A fleet is a scheduling, scaling and state problem. These tools handle the plumbing.

- [AgentPulse](https://github.com/StefanYasin/agentpulse) - Turns the scheduler's jobs.json into a read-only status board with failure streaks, stale next-run timestamps and gateway heartbeat age.
- [Argo Workflows](https://github.com/argoproj/argo-workflows) - Kubernetes-native workflow engine for DAGs and steps, often used to schedule batch agent jobs and evaluation runs.
- [Dynamo](https://github.com/ai-dynamo/dynamo) - Orchestrates multi-node inference across vLLM, SGLang and TensorRT-LLM, adding routing and KV-cache aware scheduling above the engines.
- [Kagent](https://github.com/kagent-dev/kagent) - Kubernetes control plane for declaring, running and observing AI agents as custom resources.
- [KEDA](https://github.com/kedacore/keda) - Event-driven autoscaler that scales workers and model-serving pods from queues, cron schedules or custom metrics.
- [KServe](https://github.com/kserve/kserve) - Model serving platform for Kubernetes with autoscaling, canary rollouts and multi-framework runtimes.
- [KubeRay](https://github.com/kuberay-project/kuberay) - Operator for running Ray clusters on Kubernetes, including Ray Serve deployments for agent backends.
- [llm-d](https://github.com/llm-d/llm-d) - Kubernetes inference stack with prefix-aware routing and KV-cache management for serving models across many nodes.
- [Prefect](https://github.com/PrefectHQ/prefect) - Python workflow orchestrator with retries, scheduling and observability for long-running data and agent jobs.
- [Temporal](https://github.com/temporalio/temporal) - Durable execution service for long-running workflows, useful when agent runs must survive restarts and human waits.
- [Windmill](https://github.com/windmill-labs/windmill) - Self-hosted platform that turns scripts into scheduled workflows and internal UIs, with an execution log per run.

## Cost and usage tracking

Token spend is easy to create and hard to attribute. These projects meter, route and cap model usage.

- [Bifrost](https://github.com/maximhq/bifrost) - High-throughput AI gateway with provider failover, semantic caching and budget controls across 20+ providers.
- [Kong AI Gateway](https://github.com/Kong/kong) - Kong Gateway plus AI plugins for multi-provider proxying, token-based rate limits and spend controls.
- [Lago](https://github.com/getlago/lago) - Usage-based billing API that meters events, applies plans and produces invoices, usable for per-token or per-run pricing.
- [LiteLLM](https://github.com/BerriAI/litellm) - Proxy and Python SDK for 100+ model APIs with virtual keys, budgets, spend logs and fallback routing.
- [OpenMeter](https://github.com/openmeterio/openmeter) - Event metering backend that aggregates usage in real time and feeds it into billing or quota systems.
- [Portkey Gateway](https://github.com/Portkey-AI/gateway) - AI gateway with routing, caching, guardrails and request-level cost analytics across providers.
- [TokenCost](https://github.com/AgentOps-AI/tokencost) - Small library for estimating token costs across hundreds of models, handy inside evals and budget checks.

## Incident response

When an agent fails in production, the clock starts. These tools help you detect it, gather evidence and explain what happened.

- [Botkube](https://github.com/kubeshop/botkube) - Kubernetes monitoring bot that sends alerts into Slack, Teams or Discord and runs diagnostics from chat.
- [Cachet](https://github.com/cachethq/cachet) - Self-hosted status page for communicating outages and maintenance, with incident timelines and subscriber notifications.
- [EndpointWatch](https://github.com/StefanYasin/endpointwatch) - Windows live-response tool that streams process, network and persistence changes, checks indicators against threat feeds, and explains alerts in plain English.
- [Falco](https://github.com/falcosecurity/falco) - Runtime security engine that detects suspicious syscalls and container behavior from eBPF or kernel module events.
- [HolmesGPT](https://github.com/HolmesGPT/holmesgpt) - SRE agent that pulls logs, metrics and Kubernetes state into an investigation and explains likely root causes.
- [K8sGPT](https://github.com/k8sgpt-ai/k8sgpt) - CLI that sends Kubernetes cluster diagnostics to an LLM and returns prioritized problems with suggested fixes.
- [Keep](https://github.com/keephq/keep) - AIOps alert console that deduplicates, enriches and routes alerts from many monitoring sources.
- [Robusta](https://github.com/robusta-dev/robusta) - Kubernetes alerting and automation layer that groups noisy alerts and attaches pod, log and metric context.
- [Sentry](https://github.com/getsentry/sentry) - Error and performance monitoring for applications, including agent backends, with stack traces and release tracking.
- [Uptime Kuma](https://github.com/louislam/uptime-kuma) - Self-hosted uptime monitor with HTTP, TCP and push checks, status pages and notification integrations.

## What belongs here

An entry needs to help operate an agent in production. That means instrumentation, testing, runtime constraints, deployment at scale, usage metering or recovery. A public repository is required, and the project should be maintained enough that I would run it myself.

Not included:

- Frameworks whose main job is authoring agents. Those belong in [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents).
- Closed products with no public repository.
- General observability vendors without agent-specific support.
- Archived projects. The weekly review flags them for removal.

## Maintained by

This list is kept current by an automated weekly review. A GitHub Actions job re-fetches every link, asks the GitHub API whether any entry has been archived, and opens an issue when something breaks. The same pattern runs in [agentpulse](https://github.com/StefanYasin/agentpulse), the read-only dashboard I use to catch stale and failing scheduled jobs before they pile up.

## Contributing

Open a pull request with one entry per line, alphabetical within its section, and a description that says what the tool does for an operator. Run `python scripts/validate_list.py` and `python scripts/check_links.py` before pushing. If a project is archived or has not shipped in a year, leave it out.

## License

MIT. See [LICENSE](LICENSE).

---

Built and maintained by [Stefan Yasin](https://stefanyasin.github.io/). More work at [stefanyasin.github.io](https://stefanyasin.github.io/).
