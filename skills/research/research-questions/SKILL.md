---
name: research-questions
description: Develop focused, feasible and researchable questions from a topic.
---

# Research Question Generator

## When to use
Use this skill when a user requests: develop focused, feasible and researchable questions from a topic.

## Inputs
Collect the source material, goal, audience, constraints, preferred format and relevant assumptions. Ask only for missing information that materially changes the result.

## Workflow
1. Restate the intended outcome internally and identify constraints.
2. Separate user-provided facts from assumptions.
3. Use the `research_research_questions` MCP tool when deterministic processing or structured output is useful.
4. Produce a complete, directly usable result with clear headings or fields.
5. Flag missing evidence, uncertainty and any calculations or assumptions.
6. Check the output against the user's requested format and constraints.

## Output quality
Be specific, concise and actionable. Never invent facts, sources, credentials, measurements or completed actions. Preserve important caveats. For high-impact professional, financial, legal or health decisions, provide organizational support rather than pretending to replace a qualified professional.

## Tool interface
MCP tool: `research_research_questions`
Input: a JSON object named `payload` containing the task material and optional settings.
