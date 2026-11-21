
# AgentForge

**100 AI-powered tools. One open-source ecosystem.**

AgentForge is an extensible AI plugin ecosystem designed to give AI agents, developers, researchers, students, professionals and businesses access to useful capabilities through Agent Skills, Model Context Protocol (MCP), CLI tools and APIs.

## Features

- 100 tools across 10 professional domains
- MCP server integration
- Agent Skills support
- FastAPI-powered marketplace backend
- React + Vite marketplace frontend
- Searchable plugin catalogue
- Category-based discovery
- Tool execution interface
- JSON input and structured outputs
- Local-first architecture
- Extensible plugin registry
- Automated testing

## Plugin Categories

| Category | Purpose |
|---|---|
| SecurityForge | Cybersecurity and security analysis |
| CodeForge | Software development and code intelligence |
| ResearchForge | Research and academic productivity |
| AutoForge | Productivity and workflow automation |
| DataForge | Data processing and analytics |
| VisionForge | Computer vision and image analysis |
| BusinessForge | Business intelligence and marketing |
| ConnectForge | APIs and integrations |

## Project Structure

```text
AgentForge/
├── backend/
├── frontend/
├── registry/
├── plugins/
├── packages/
├── templates/
├── docs/
├── tests/
├── src/
├── skills/
├── .github/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── SECURITY.md
├── CHANGELOG.md
└── .gitignore
```

## Technology Stack

**Backend**
- Python
- FastAPI
- Pydantic
- MCP Python SDK

**Frontend**
- React
- Vite
- JavaScript

**AI Integration**
- Model Context Protocol
- Agent Skills
- Ollama-compatible local AI workflows

**Testing and Development**
- pytest
- Git
- GitHub Actions

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/YOUR-USERNAME/AgentForge.git
cd AgentForge
```

### 2. Set up the Python environment

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -e .
```

### 3. Run tests

```bash
pytest -v
```

### 4. Start the MCP server

```bash
agentforge-mcp
```

The MCP server uses standard input/output transport and should be launched by a compatible MCP client.

## Marketplace Setup

Open two terminal windows from the repository root.

### Backend

```bash
pip install -r backend/requirements.txt
uvicorn backend.app.main:app --reload --port 8000
```

Backend API:

http://localhost:8000

Interactive API documentation:

http://localhost:8000/docs

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Marketplace:

http://localhost:5173

## MCP Client Configuration

Example configuration for an MCP-compatible client:

```json
{
  "mcpServers": {
    "agentforge": {
      "command": "/ABSOLUTE/PATH/TO/AgentForge/.venv/bin/agentforge-mcp",
      "args": []
    }
  }
}
```

Replace the executable path with your actual local path.

## Creating Plugins

AgentForge uses a modular plugin architecture.

Each plugin should include:

- Unique name and version
- Category and description
- Installation instructions
- Input and output definitions
- Appropriate Agent Skill or MCP interface
- Tests and usage examples
- Security and permission documentation

See `docs/` and `templates/` for development resources.

## Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch.
3. Implement your plugin or improvement.
4. Add tests and documentation.
5. Submit a pull request.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before submitting.

## Security

AgentForge aims to use safe defaults, including restricted permissions and explicit user approval for consequential actions.

Please report vulnerabilities responsibly using the instructions in [SECURITY.md](SECURITY.md).

## Roadmap

- [x] Initial plugin ecosystem
- [x] 100-tool catalogue
- [x] MCP server
- [x] Agent Skills
- [x] Marketplace frontend and backend
- [x] Search and category discovery
- [ ] User authentication
- [ ] Community plugin submissions
- [ ] Plugin ratings and reviews
- [ ] Public marketplace deployment
- [ ] Additional integrations

## License

Released under the MIT License. See [LICENSE](LICENSE).

## Acknowledgements

Built for the open-source AI developer community.

## m8ven

[![M8ven Score](https://m8ven.ai/badge/mcp/sreevatsarajesh-agentforge-195quw?v=0bd7680324a2a029d91667ef40e17ad8)](https://m8ven.ai/mcp/sreevatsarajesh-agentforge-195quw?s=readme)

[![M8ven Score](https://m8ven.ai/badge/mcp/sreevatsarajesh-agentforge-195quw?v=0bd7680324a2a029d91667ef40e17ad8)](https://m8ven.ai/mcp/sreevatsarajesh-agentforge-195quw?s=readme)

**AgentForge — Build. Connect. Automate. Extend.**
