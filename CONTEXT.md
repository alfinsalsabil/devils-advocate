# Devil's Advocate: Project Context & Architecture

This document serves as the **Single Source of Truth** for the Devil's Advocate framework. It defines the project's vision, core technical philosophy, and architectural boundaries.

## 1. 🔄 Maintenance & Lifecycle Policy (CRITICAL)
- **Mandatory Updates**: This document MUST be updated *immediately* upon any changes to `AGENTS.md`, `pyproject.toml`, or shifts in core orchestration logic.
- **Responsibility**: The `@fixer` agent is the sole entity authorized to update this file under the strict guidance of the Orchestrator.
- **Verification Rule**: Before starting any new architectural task, sub-agents MUST read this file to prevent context loss and over-engineering.

## 2. 🎯 Project Vision
To solve "AI complacency" (lazy orchestration, hallucinations, logical gaps) by forcing a strict, adversarial "Roast and Verify" loop. The framework demands that AI-generated work be challenged by an adversarial reviewer (`@oracle`) and cross-referenced before acceptance.

## 3. 🧠 Core Philosophy
1. **Keep It Simple**: Avoid unnecessary complexity. Use *LLM Context Caching* and parse markdown reports for inter-session memory.
2. **Meta-Agentic Oversight ("AI within AI")**: A hierarchical split where strategic logic (Devil's Advocate) governs tactical execution. The Orchestrator manages the boundaries of all operations.
3. **Flat Architecture**: The project follows a flat directory structure to maintain simplicity and direct access to core components without nested monorepo complexities.
4. **Independent Architecture via MCP**: The project utilizes the Model Context Protocol (MCP) to ensure high extensibility to future tools without modifying core orchestration logic.

## 4. 🛑 Hard Architectural Constraints
- **Orchestrator Prohibitions**: The Orchestrator is STRICTLY PROHIBITED from directly modifying files or running arbitrary `bash` commands. It MUST delegate these tasks.
- **Execution Governance**:
  - Only `@fixer` is authorized to trigger tools that modify state (`write`, `edit`, `bash`).
  - `@explorer` is restricted to read-only tools (`read`, `grep`, `glob`).
  - Executing terminal commands (`bash`) MUST be gated behind a Human-In-The-Loop (HITL) prompt in interactive modes.

## 5. 🧱 Current Technical Architecture
- **Tech Stack**: Python (>=3.9), Typer (CLI interface), LiteLLM (provider-agnostic model routing), and MCP (Model Context Protocol).
- **Flat Directory Model**: This repository uses a **Flat Directory architecture**. All core folders (`src/`, `commands/`, `skills/`) reside at the project root. Disregard any legacy references to a nested `devils-advocate/` monorepo subfolder. This ensures a unified workspace for both the framework and its extensible modules.

## 6. 📁 Directory Structure (Flat Layout)
- `src/`: Core framework source code and CLI logic.
- `commands/`: Directory for framework-specific command implementations.
- `skills/`: Contains specialized skill definitions for the agents.
- `AGENTS.md`: The definitive "constitution" defining agent roles, prohibitions, and conflict resolution protocols.
- `CONTEXT.md`: This file (Project vision, boundaries, and lifecycles).
- `pyproject.toml`: Python packaging and dependency declarations.
- `README.md`: Project overview and installation instructions.
- `codemap.md`: High-level map of the codebase for agent navigation.

## 7. 📜 Key Historical Decisions
- **Session 111000**: Decided to pursue a standalone Python CLI to enforce programmatic safety controls (HITL, Max Steps).
- **Session 112000**: Resolved to use MCP for sandboxing and extensibility instead of raw `subprocess.run`.
- **Session 113000**: Transitioned from a nested monorepo structure to a **Flat Directory** architecture to simplify path management and developer experience.
