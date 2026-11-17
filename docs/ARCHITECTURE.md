# Architecture

AgentForge has four layers: client applications, integration interfaces, shared local tooling and domain-specific capabilities. The MCP server dynamically registers the 100 registry entries. The CLI and MCP server both call the same execution engine. Agent Skills provide model-facing workflows and point to the corresponding MCP tool.

The registry is the source of truth for tool names, descriptions, categories and skill paths. Add new tools by updating the registry generator/source data, adding implementation behavior where appropriate, writing the skill, and adding tests.
