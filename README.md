# RaOne Aura

[![Python Version](https://img.shields.io/badge/python-3.12%2B-blue)](https://www.python.org/downloads/release/python-3120/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)

**An autonomous AI terminal agent, built by Anish Raj.**

RaOne Aura is an ultra-premium, command-line coding assistant powered by advanced language models. It transforms your terminal into a conversational, highly capable AI interface. With RaOne, you can use natural language to explore, modify, and interact with your entire codebase through a powerful suite of integrated tools, all wrapped in a stunning cyberpunk-inspired aesthetic.

---

### 🚀 Quick Install

**Windows (Recommended)**

Ensure you have `uv` installed, then run:

```bash
uv tool install raone-aura
```

*(If you are running the source directly via uv: `uv run aura`)*

---

## ⚡ Core Features

- **Cyberpunk Terminal UI**: An unparalleled, premium terminal interface featuring a mathematically rendered, real-time 3D rotating Tesseract animation, glowing neon accents, and meticulously designed color palettes.
- **Autonomous Agent**: RaOne breaks down complex requests, tracks progress with a built-in Todo system, and executes tasks step-by-step.
- **Full Codebase Access**: 
  - Read, write, and patch files across your project.
  - Search recursively using high-speed regex.
  - Execute stateful shell commands (Git, npm, python, etc.) directly from the chat.
- **Subagents & Delegation**: RaOne can delegate specific context-heavy tasks to specialized subagents.
- **Project-Aware Context**: Automatically scans your project's file structure, Git status, and active environment to understand your codebase immediately.
- **Safety First**: Configurable execution modes ensure you approve any critical file modifications or shell commands before they run.

---

## 🛠️ Usage

### Interactive Mode

Simply start the agent from your project directory:

```bash
aura
```

Once inside the RaOne Aura terminal:
- **Chat**: Type natural language requests (e.g., `"Refactor the authentication logic in src/auth.py"`).
- **File Referencing**: Use `@` to auto-complete and reference specific files in your prompt.
- **Direct Shell Commands**: Prefix commands with `!` to run them directly in your shell (e.g., `!git status`).
- **Shortcuts**:
  - `Ctrl+O`: Toggle the tool execution output view.
  - `Ctrl+T`: Toggle the AI's internal Todo list.
  - `Shift+Tab`: Toggle Auto-Approve mode for tool execution.

### Built-in Agent Profiles

RaOne ships with different operating modes depending on your needs:

- **`default`**: Requires manual approval for most file writes and shell commands. Safest.
- **`plan`**: Read-only mode for exploration and architecture planning.
- **`accept-edits`**: Auto-approves file modifications, but asks before running terminal commands.
- **`auto-approve`**: Full autonomous mode. Use with caution.

Start a specific profile using:
```bash
aura --agent accept-edits
```

---

## ⚙️ Configuration

RaOne Aura is highly configurable via a `config.toml` file (located in `~/.vibe/config.toml` or your project's `.vibe/config.toml`). 

You can configure:
- **LLM Providers**: Easily swap between local models (Ollama) or cloud providers.
- **Themes**: Tweak the terminal UI colors.
- **Tool Permissions**: Grant or revoke specific tool access (e.g., disabling shell access).
- **Custom System Prompts**: Override RaOne's default identity and behavior.

---

## 🧩 Skills & Plugins

Extend RaOne's capabilities by writing custom **Skills**. Skills can add new slash commands (like `/test` or `/review`) and specific tool sets. Drop your custom skills into `~/.vibe/skills/` and RaOne will automatically load them.

---

## 📜 License

Copyright (c) 2026 Anish Raj.

Licensed under the **MIT License**. See the [LICENSE](LICENSE) file for more information.
