# Devil's Advocate: Project Context & Architecture

This document is the **Single Source of Truth** for the Devil's Advocate framework. It defines the project's vision, core technical philosophy, and architectural boundaries.

## 1. 🔄 Maintenance & Lifecycle Policy (CRITICAL)
- **Mandatory Updates**: This document MUST be updated *immediately* upon any changes to `AGENTS.md`, `pyproject.toml`, or shifts in core orchestration logic.
- **Responsibility**: The `@fixer` agent is the sole entity authorized to update this file under the strict guidance of the Orchestrator.
- **Verification Rule**: Before starting any new architectural task, sub-agents MUST read this file to prevent context loss and over-engineering.

## 2. 🎯 Project Vision
To solve "AI complacency" (lazy orchestration, hallucinations, logical gaps) by forcing a strict, adversarial "Roast and Verify" loop. The framework demands that AI-generated work be challenged by an adversarial reviewer (`@oracle`) and cross-referenced before acceptance.

## 3. 🧠 Core Philosophy
1. **Keep It Simple**: Avoid massive complexity (e.g., Vector DBs). Use *LLM Context Caching* and parse markdown reports (`final-report.md`) for inter-session memory.
2. **Meta-Agentic Oversight ("AI within AI")**: A hierarchical split where strategic logic (Devil's Advocate) governs tactical execution. The Orchestrator runs in a protected Python CLI, managing the boundaries of standard OpenCode operations.
3. **Independent Architecture via MCP**: The project utilizes the open standard Model Context Protocol (MCP) rather than hardcoding proprietary vendor API calls, ensuring high extensibility to future tools (like Jira, GitHub) without modifying core orchestration logic.

## 4. 🛑 Hard Architectural Constraints
- **Orchestrator Prohibitions**: The Orchestrator is STRICTLY PROHIBITED from directly modifying files or running arbitrary `bash` commands. It MUST delegate these tasks.
- **MCP Access Governance**:
  - Only `@fixer` is authorized to trigger MCP tools that modify state (`write_file`, `bash`).
  - `@explorer` is restricted to read-only MCP tools (`read_file`, `grep`).
  - Executing terminal commands (`bash`) MUST be gated behind a Human-In-The-Loop (HITL) prompt in interactive modes, passing through safe middleware blocks in the Python CLI.

## 5. 🧱 Current Technical Architecture
- **Tech Stack**: Python (>=3.9), Typer (CLI interface), LiteLLM (provider-agnostic model routing), and MCP Python SDK.
- **MCP Middleware Pattern**: The Python CLI acts as an interceptor. Instead of allowing the LLM direct, unobstructed access to the OS, the CLI validates tool calls (requesting user confirmation) before dispatching them to MCP Servers (e.g., `@modelcontextprotocol/server-filesystem`).

## 6. 📁 Directory Structure
- `src/devils_advocate_cli/`: Core Python package containing the MCP Client middleware and Typer CLI logic.
  - `data/SKILL.md`: The declarative instructions bundle loaded via `importlib.resources`.
- `AGENTS.md`: The definitive "constitution" locking down agent roles, prohibitions, and conflict resolution protocols.
- `CONTEXT.md`: This file (Project vision, boundaries, and lifecycles).
- `.devils-advocate/`: The historical session storage directory serving as the framework's file-based memory.
- `pyproject.toml`: Modern Python packaging and dependency declarations.

## 7. 📜 Key Historical Decisions
- **Session 111000**: Decided to pursue a standalone Python CLI to enforce programmatic safety controls (HITL, Max Steps) which declarative Markdown cannot reliably guarantee.
- **Session 112000**: Resolved a debate on MCP complexity. Reverting to native `subprocess.run` was rejected as it reintroduces Arbitrary Code Execution risks. MCP is retained for its sandboxing and extensibility.
