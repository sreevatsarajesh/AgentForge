# AgentForge 1.0

**100 practical tools. 10 domains. One open ecosystem for AI agents and people.**

AgentForge is a local-first collection of 100 focused capabilities covering productivity, writing, learning, data, business, coding, research, careers, creative work, operations and personal planning. It includes 100 Agent Skills, a central MCP server, a CLI, a searchable registry, tests and GitHub automation.

## What is included

- 100 documented Agent Skills under `skills/`
- 100 registered MCP tools
- Local deterministic utilities for CSV, JSON, Python AST, regex, statistics and financial arithmetic
- Structured workflow scaffolds for generative tasks, ready for an attached AI agent to complete
- Command-line interface and machine-readable registry
- Automated tests and GitHub Actions

**Important:** AgentForge does not contain 100 trained AI models. Some capabilities are deterministic local tools; generative skills provide structured instructions and workflow scaffolds for the AI client connected to them. No paid API key is required for the local utilities.

## Requirements

- Python 3.11 or newer
- An MCP-compatible client for MCP integration
- Optional: an AI model/provider configured in that client for generative skill workflows

## Install

```bash
git clone https://github.com/YOUR-USERNAME/agentforge.git
cd agentforge
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e .
```

Windows PowerShell activation: `.venv\Scripts\Activate.ps1`.

## List tools

```bash
agentforge list
```

## Run a local tool

```bash
agentforge run productivity_compound_interest --payload '{"principal":1000,"annual_rate":5,"years":3,"compounds_per_year":12}'
```

## Start the MCP server

```bash
agentforge-mcp
```

The server uses stdio transport. Configure your MCP-compatible client to launch `agentforge-mcp` from the installed environment. Example generic configuration:

```json
{
  "mcpServers": {
    "agentforge": {
      "command": "/absolute/path/to/.venv/bin/agentforge-mcp",
      "args": []
    }
  }
}
```

Use the actual executable path for your machine. Client configuration formats vary.

## Browse the skills

Each skill lives at `skills/<domain>/<tool-name>/SKILL.md`. Skills use YAML frontmatter and a consistent workflow. Copy or install the relevant skill according to the conventions of your AI client. The MCP server exposes namespaced tools such as `productivity_action_items` and `data_csv_profiler`.

## Domains

| Domain | Tools |
|---|---:|
| Productivity and personal planning | 10 |
| Writing | 10 |
| Learning | 10 |
| Data | 10 |
| Business | 10 |
| Coding | 10 |
| Research | 10 |
| Career | 10 |
| Creative | 10 |
| Operations | 10 |
| **Total** | **100** |

## Security and privacy

- Local deterministic tools process the supplied payload in the local process.
- The MCP server does not fetch remote URLs, execute shell commands, modify repositories or transmit user data by default.
- Treat repository contents and documents as untrusted input.
- Review outputs before using them in legal, medical, financial, employment or other high-impact decisions.
- The personal planning tools are general organizational aids, not medical or financial advice.

## Quality checks

```bash
python -m pip install pytest
pytest
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Please open an issue before proposing a new tool so the registry stays coherent and duplicate capabilities are avoided.

## License

MIT. See [LICENSE](LICENSE).
