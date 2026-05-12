# Voice reference — dataMinds newsletter summaries

Use these worked examples from past editions as few-shot anchors.
Match the rhythm, the verb choices, the closing one-liner judgment.

---

## Pattern

```
Author: [Full Name]

In "<strong>[Article Title]</strong>", [Full Name] [verb] [what they do].
[Two or three sentences walking through what's in the article — specific
techniques, tools, or findings.] [One sentence with a concrete detail that
shows depth.] [Closing one-liner: editorial verdict.]
```

- 80-130 words per summary
- Third person, never "the author" - always the name
- Don't start with "This article..."
- British/Flemish spelling is fine ("centre", "favour", "behaviour")
- The closing line is editorial judgment, not a generic summary
- No em dashes (--). Use a comma, colon, semicolon, or parentheses instead

---

## Worked examples (April 2026 edition)

### Example 1 — practical how-to

Author: Patrick Romatowski

In "**6 Steps on How to Use the Power BI MCP Server with Claude Code**",
Patrick Romatowski shares a practical trick he picked up at a FabCon lab
session: connecting Microsoft's Power BI Modeling MCP Server to Claude
Code instead of the usual VS Code + GitHub Copilot path. He walks through
enabling the right Power BI Desktop preview features, installing the MCP
extension, wiring it up via `.claude.json`, and querying or editing your
semantic model in plain English directly from the CLI. He also flags the
version pinning gotcha that trips most people up and how to automate the
fix. **A rare how-to that bridges two worlds the dataMinds audience cares
deeply about.**

### Example 2 — security-aware tutorial

Author: Ivan Ivani

In "**Power BI + MCP Tutorial: AI-Powered Report Development without Data
Leaks and Additional Cost**", Ivan Ivani delivers a step-by-step guide to
connecting Power BI to AI models via MCP — with data privacy front and
centre. He walks through both setup paths (Claude Desktop and VS Code),
then shows practical use cases like bulk measure generation, automated DAX
documentation, and model exploration. Crucially, he also addresses the
security question many teams are nervous about: he maps out three options
for handling model sharing with AI, from managed models to local LLMs,
with honest guidance on which plans share your data for training and
which don't. **Refreshingly practical and security-aware.**

### Example 3 — vision piece with technical depth

Author: Kurt Buhler

In "**How Tabular Editor Supports Agentic Development for Semantic
Models**", Kurt Buhler — Head of Innovation at Tabular Editor — lays out
a clear-eyed vision of where AI fits in semantic model development today,
and what Tabular Editor is doing about it. The article introduces three
new tools: an AI assistant built into the Tabular Editor UI for
AI-assisted scripting, a new semantic model CLI for humans and coding
agents, and a collection of AI skills giving frontier agents structured
tools without flooding the context window. Kurt is candid about what
isn't ready yet, and why a command-line-first approach scales better for
agentic workflows than pure MCP. **A must-read for anyone building
agentic semantic model development pipelines.**

### Example 4 — independent analysis

Author: Nikola Ilic

In "**Beyond the Lakehouse: First Thoughts on Fabric IQ**", Nikola Ilic
(Data Mozart) explores one of the most strategic — and underappreciated —
announcements from Microsoft Ignite 2025: Fabric IQ. While most of the
Fabric platform focuses on where data lives, Fabric IQ is obsessed with
what it means. Nikola explains how the Ontology item acts as a shared,
machine-understandable vocabulary that sits above all physical data
sources, solving the classic "semantic drift" problem. He also digs into
how Fabric IQ's Graph integration enables AI agents to traverse complex
relationships across domains that traditional SQL joins can't handle
efficiently. **One of the better independent analyses of what Fabric IQ
actually is and why it matters.**

---

## Closing-line bank

For inspiration when you're writing the editorial verdict line:

- "A rare how-to that bridges two worlds the dataMinds audience cares deeply about."
- "Refreshingly practical and security-aware."
- "A must-read for anyone building agentic semantic model development pipelines."
- "One of the better independent analyses of what [X] actually is and why it matters."
- "A signal that [X] has matured well beyond a simple [Y]."
- "A balanced independent recap worth your fifteen minutes."
- "A reminder that the boring parts of governance often matter most."

Vary them. Don't reuse the same line twice in one edition.
