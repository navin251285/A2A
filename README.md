# A2A: Agent-to-Agent Learning Repository

This repository is a progressive, hands-on curriculum for building Agent-to-Agent (A2A) systems and understanding how A2A orchestration works with MCP-style tool invocation.

## Repository Goal

The repo is organized as a step-by-step path:
- Start with reusable agents and capability discovery
- Move into routing and invocation
- Expand into multi-agent workflow patterns
- Add async, streaming, notifications, and human approval
- Add security layers (API key, JWT)
- Compare A2A orchestration vs MCP-only tool execution

Most modules include:
- Source notebooks (original working notebooks)
- Python services/controllers (`.py`)
- Tutorial notebooks (`*_tutorial.ipynb`) for guided learning

## Folder Map

### 00_Agents
Reusable baseline agents and delay variants.
- Math and finance agent services
- Tool discovery and invoke endpoints
- Foundation tutorial: `00_agents_tutorial.ipynb`

### 01_capability_discovery
Runtime discovery of agent identity and tools.
- Capability registry construction
- Tutorial: `01_capability_discovery_tutorial.ipynb`

### 02_ Agent Routing
Route user query to the most suitable discovered capability.
- Rule-based routing over tool metadata
- Tutorial: `02_agent_routing_tutorial.ipynb`

### 03_agent_invocation
Execute selected agent/tool with structured payloads.
- Discovery -> route -> payload -> invoke pipeline
- Tutorial: `03_agent_invocation_tutorial.ipynb`

### 04_multi_agent_workflow
Sequential multi-step orchestration with result chaining.
- Plan + execute loop
- State/result injection between steps
- Tutorial: `04_multi_agent_workflow_tutorial.ipynb`

### 05_Negotiation
Broadcast-style execution and post-response selection.
- Query multiple candidates
- Evaluate and choose best valid response
- Tutorial: `05_negotiation_tutorial.ipynb`

### 06_Multi-Agent_Workflow
More explicit workflow architecture and control components.
- Planner/router/executor/memory concepts
- Tutorial: `06_multi_agent_workflow_tutorial.ipynb`

### 07_Asynchronous _Long-Running_A2A
Deferred execution patterns for long-running tasks.
- Submit/status model
- Polling-oriented async control
- Tutorial: `07_asynchronous_long_running_a2a_tutorial.ipynb`

### 08_streaming_a2a
Incremental response delivery patterns.
- Streaming HTTP, SSE-style, websocket-style clients
- Tutorials/notebooks: `08_streaming_a2a_tutorial.ipynb`, `streaming_clients.ipynb`

### 09_Push-Notification
Background task completion signaling.
- Submit + result retrieval with push/poll patterns
- Tutorial: `09_push_notification_tutorial.ipynb`

### 10_Human_in_loop
Approval-gated orchestration.
- Pending approval states
- Approve/reject transition handling
- Tutorial: `10_human_in_loop_tutorial.ipynb`

### 11_authentication_authorizatoin_key_based
Key-based request authentication.
- `x-api-key` protected invocation pattern
- Tutorial: `11_authentication_authorizatoin_key_based_tutorial.ipynb`

### 12_JWT_authentication_authorizatoin
JWT-style token-based auth flow.
- Token verification and protected execution
- Tutorial: `12_jwt_authentication_authorizatoin_tutorial.ipynb`

### A2A_vs_MCP
Comparative architectural notebooks.
- MCP-only single-tool style vs A2A+MCP orchestration
- Capstone tutorial: `13_a2a_vs_mcp_tutorial.ipynb`

## Recommended Learning Order

1. `00_Agents`
2. `01_capability_discovery`
3. `02_ Agent Routing`
4. `03_agent_invocation`
5. `04_multi_agent_workflow`
6. `05_Negotiation`
7. `06_Multi-Agent_Workflow`
8. `07_Asynchronous _Long-Running_A2A`
9. `08_streaming_a2a`
10. `09_Push-Notification`
11. `10_Human_in_loop`
12. `11_authentication_authorizatoin_key_based`
13. `12_JWT_authentication_authorizatoin`
14. `A2A_vs_MCP`

## How to Use This Repo

1. Open a folder module and run its source notebook to see original implementation.
2. Open the corresponding tutorial notebook (`*_tutorial.ipynb`) for a guided explanation.
3. Prefer local/offline simulation cells first if services are not running.
4. Then run live-service cells after starting required agents/controllers.

## File Types You Should Focus On

- `.ipynb`: learning flow and experiments
- `.py`: service/controller logic

This repo intentionally avoids requiring environment/cache artifacts for understanding the architecture.

## Notes

- Folder names are kept as-is to match the original learning progression.
- Some folders include backups or alternate variants for experimentation.
- Security/auth modules are educational examples and should be hardened for production use.
