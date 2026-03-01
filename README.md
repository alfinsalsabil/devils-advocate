![Devil's Advocate Header](https://raw.githubusercontent.com/alfinsalsabil/devils-advocate/refs/heads/master/assets/Devil's%20Advocate%20Header.webp)
# Devil's Advocate for OpenCode 😈

[![License](https://img.shields.io/badge/license-MIT-blue.svg)](LICENSE)
[![OpenCode](https://img.shields.io/badge/OpenCode-compatible-success)](https://github.com/opencode)

Hey there! 👋 Just another "vibecoder" here. While building stuff with AI, I realized a hard truth: **everything an AI does (and even humans, let's be real) is prone to being missed, having mistakes, or just falling short.** 

That's why I built **Devil's Advocate**. It's a custom command and agent skill for OpenCode that refuses to take "I'm done" for an answer until it's been roasted by a specialized review loop.

---

## 🐛 The Headaches (The Problem)

We've all been there:
1. **Lazy Orchestration**: Sometimes the main agent tries to do everything itself instead of using the experts.
2. **Hallucinations**: AI confidently tells you a library works a certain way, but it actually changed 2 versions ago.
3. **The "Oops" Factor**: Small logic gaps that look fine at first glance but break when you actually run the code.

## 💡 The "Aha!" Moment: Forced Delegation & Roasting

The fix was simple but effective: **Don't trust the first draft.** 
Devil's Advocate forces OpenCode to delegate tasks to sub-agents, and then brings in `@oracle` to act as a "Devil's Advocate" to find every single flaw in their work. 

If `@oracle` finds a bug, we fix it. If it finds a missed requirement, we add it. Only then do you get the final report.

---

## Main Features (Phase 1-5)

*   **Phase 1: Parallel Delegation**: No more single-agent laziness. It forces work out to `@explorer`, `@fixer`, `@librarian`, and `@designer` simultaneously.
*   **Phase 2: Iterative Review Loop**: `@oracle` steps in to roast the sub-agents' output. It looks for weaknesses, gaps, and "missing" logic.
*   **Phase 3: Fact & Code Verification**: We don't just trust the roast. `@oracle`'s findings are cross-verified by `@explorer` (repo check) and `@librarian` (docs check) to kill hallucinations.
*   **Phase 4: Severity Classification**: Findings are ranked from **CRITICAL** to **LOW** so you know what actually matters.
*   **Phase 5: Comprehensive Report**: You get a full breakdown of every iteration, every finding, and every fix applied.

---

### 📋 Prerequisites
Devil's Advocate isn't a lone wolf—it's an orchestration beast that sits on top of the **oh-my-opencode-slim** stack. Before you start roasting your code, make sure you've got the foundation ready:

*   **The Engine:** [oh-my-opencode-slim](https://github.com/alvinunreal/oh-my-opencode-slim)

Go grab that first. Once you're set up there, come back and let's get to work.

---

## 🏗️ Architecture & Mechanism

### Markdown-as-Engine (The Brain)
We vibe with the **"Markdown-as-Engine"** approach. All our logic, agent protocols, and "roast" instructions live in structured Markdown files. It's flexible, readable, and acts as the perfect MCP (Model Context Protocol) bridge between your raw ideas and verified execution.

### The Roast (Review Loop)
The magic happens in the **Review Loop**. Nothing—and we mean *nothing*—gets a pass until `@oracle` tears it apart. We look for:
1.  **Logic Flaws**: Is the code actually smart?
2.  **Fact Checks**: No more hallucinations. We verify against real docs.
3.  **No Regressions**: We make sure your new stuff doesn't blow up your old stuff.

---

## Installation

### The Easy Way (Global)
To use this skill across all your projects:

1.  Clone the repo:
    ```bash
    git clone https://github.com/username/devils-advocate.git
    cd devils-advocate
    ```
2.  Blast the install script:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```

### The Manual Way
If you like to keep things tidy yourself, copy these files:
*   `commands/devils-advocate.md` -> `~/.config/opencode/commands/`
*   `skills/devils-advocate/SKILL.md` -> `~/.config/opencode/skills/devils-advocate/`

### Uninstallation
Changed your mind? No hard feelings:
```bash
chmod +x uninstall.sh
./uninstall.sh
```

---

## Usage

Once it's in your system, just call the command inside OpenCode:

```text
/devils-advocate <your_prompt_or_task>
```

**Example:**
```text
/devils-advocate add error handling to the fetchUser function
```

---

## Let's Make It Better

I'm just enjoying the vibecoding life and trying to make AI less "forgetful." If you've got ideas to make the review loop even more brutal, open an Issue or PR. Let's build something bulletproof together! 🛠️✨
