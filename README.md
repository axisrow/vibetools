# Awesome Vibe Coding Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> A curated list of tools for **vibe coders** — developers building software with AI assistants (Claude Code, Cursor, Copilot and friends). Star counts are auto-updated daily. **[Browse the searchable site →](https://axisrow.github.io/vibetools/)** · Built with GLM-5.2.

A list should be a **curation, not a collection**: every entry is hand-picked, has a live repository, and is relevant to AI-assisted development. See CONTRIBUTING.md to add a tool. Русская версия: README.ru.md.

## Contents

- [Featured](#featured)
- [AI Coding Agents and CLI](#ai-coding-agents-and-cli)
- [Cloud Coding Agents](#cloud-coding-agents)
- [Editor Integrations](#editor-integrations)
- [Code Review, Testing and Quality](#code-review-testing-and-quality)
- [DevOps and Cloud Automation](#devops-and-cloud-automation)
- [Security and Pentest Agents](#security-and-pentest-agents)
- [Browser and Web Automation](#browser-and-web-automation)
- [Design to Code and Frontend](#design-to-code-and-frontend)
- [App Builders and Low-Code](#app-builders-and-low-code)
- [Game Development](#game-development)
- [Context, Memory and Codebase Indexing](#context-memory-and-codebase-indexing)
- [MCP Servers and Clients](#mcp-servers-and-clients)
- [Agent Skills, Prompts and Rules](#agent-skills-prompts-and-rules)
- [AI Assistants](#ai-assistants)
- [Observability and Eval](#observability-and-eval)
- [Docs, Research and Knowledge Work](#docs-research-and-knowledge-work)
- [Learning and Resources](#learning-and-resources)
- [AI Infra and Model Platforms](#ai-infra-and-model-platforms)
- [Domain-Specific Agents](#domain-specific-agents)
- [Needs Review](#needs-review)

## Featured

Repo of the week (2-day growth): [caveman](https://github.com/JuliusBrussee/caveman#featured-week) — Claude Code skill that cuts 65% of tokens by talking like a caveman

## AI Coding Agents and CLI

- [OpenCode](https://github.com/sst/opencode) ![](https://img.shields.io/github/stars/sst/opencode?style=flat&color=yellow) - Open-source terminal AI coding agent with multi-provider model support.
- [Claude Code](https://github.com/anthropics/claude-code) ![](https://img.shields.io/github/stars/anthropics/claude-code?style=flat&color=yellow) - Agentic coding tool that lives in the terminal and understands your codebase.
- [cc-switch](https://github.com/farion1231/cc-switch) ![](https://img.shields.io/github/stars/farion1231/cc-switch?style=flat&color=yellow) - A cross-platform desktop All-in-One assistant for Claude Code, Codex, OpenCode, OpenClaw,.
- [gemini-cli](https://github.com/google-gemini/gemini-cli) ![](https://img.shields.io/github/stars/google-gemini/gemini-cli?style=flat&color=yellow) - An open-source AI agent that brings the power of Gemini directly into your terminal.
- [rtk](https://github.com/rtk-ai/rtk) ![](https://img.shields.io/github/stars/rtk-ai/rtk?style=flat&color=yellow) - CLI proxy that reduces LLM token consumption by 60-90% on common dev commands.
- [pi](https://github.com/earendil-works/pi) ![](https://img.shields.io/github/stars/earendil-works/pi?style=flat&color=yellow) - AI agent toolkit: unified LLM API, agent loop, TUI, coding agent CLI.
- [Goose](https://github.com/block/goose) ![](https://img.shields.io/github/stars/block/goose?style=flat&color=yellow) - Open-source extensible AI agent that can install, execute, edit and test code.
- [goose](https://github.com/aaif-goose/goose) ![](https://img.shields.io/github/stars/aaif-goose/goose?style=flat&color=yellow) - An open source, extensible AI agent that goes beyond code suggestions.
- [Aider](https://github.com/Aider-AI/aider) ![](https://img.shields.io/github/stars/Aider-AI/aider?style=flat&color=yellow) - AI pair programming in the terminal that edits code in any git repo.
- [CowAgent](https://github.com/zhayujie/CowAgent) ![](https://img.shields.io/github/stars/zhayujie/CowAgent?style=flat&color=yellow) - Open-source super AI assistant & Agent Harness.
- [nanobot](https://github.com/HKUDS/nanobot) ![](https://img.shields.io/github/stars/HKUDS/nanobot?style=flat&color=yellow) - Lightweight, open-source AI agent for your tools, chats, and workflows.
- [CodeWhale](https://github.com/Hmbown/CodeWhale) ![](https://img.shields.io/github/stars/Hmbown/CodeWhale?style=flat&color=yellow) - Open-source, community-driven agent harness.
- [vibe-kanban](https://github.com/BloopAI/vibe-kanban) ![](https://img.shields.io/github/stars/BloopAI/vibe-kanban?style=flat&color=yellow) - Get 10X more out of Claude Code, Codex or any coding agent.
- [agenticSeek](https://github.com/Fosowl/agenticSeek) ![](https://img.shields.io/github/stars/Fosowl/agenticSeek?style=flat&color=yellow) - Fully Local Manus AI.
- [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) ![](https://img.shields.io/github/stars/esengine/DeepSeek-Reasonix?style=flat&color=yellow) - DeepSeek-native AI coding agent for your terminal.
- [qwen-code](https://github.com/QwenLM/qwen-code) ![](https://img.shields.io/github/stars/QwenLM/qwen-code?style=flat&color=yellow) - An open-source AI coding agent that lives in your terminal.
- [cmux](https://github.com/manaflow-ai/cmux) ![](https://img.shields.io/github/stars/manaflow-ai/cmux?style=flat&color=yellow) - Open source Ghostty-based macOS terminal with vertical tabs and notifications for AI codin.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) ![](https://img.shields.io/github/stars/can1357/oh-my-pi?style=flat&color=yellow) - AI coding agent for the terminal - hash-anchored edits, LSP and subagents.
- [plandex](https://github.com/plandex-ai/plandex) ![](https://img.shields.io/github/stars/plandex-ai/plandex?style=flat&color=yellow) - Open source AI coding agent.
- [cc-connect](https://github.com/chenhg5/cc-connect) ![](https://img.shields.io/github/stars/chenhg5/cc-connect?style=flat&color=yellow) - Bridge local AI coding agents (Claude Code, Cursor, Gemini CLI, Codex) to messaging platfo.
- [superset](https://github.com/superset-sh/superset) ![](https://img.shields.io/github/stars/superset-sh/superset?style=flat&color=yellow) - Code Editor for the AI Agents Era - Run an army of Claude Code, Codex, etc.
- [llm](https://github.com/simonw/llm) ![](https://img.shields.io/github/stars/simonw/llm?style=flat&color=yellow) - Access large language models from the command line and pipe data into them.
- [claude-squad](https://github.com/smtg-ai/claude-squad) ![](https://img.shields.io/github/stars/smtg-ai/claude-squad?style=flat&color=yellow) - Manage multiple AI terminal agents like Claude Code, Codex, OpenCode, and Amp.
- [Kaku](https://github.com/tw93/Kaku) ![](https://img.shields.io/github/stars/tw93/Kaku?style=flat&color=yellow) - A fast, out-of-the-box terminal built for AI coding.
- [hapi](https://github.com/tiann/hapi) ![](https://img.shields.io/github/stars/tiann/hapi?style=flat&color=yellow) - App for Claude Code / Codex / Gemini / OpenCode, vibe coding anytime, anywhere.
- [cc-switch-cli](https://github.com/SaladDay/cc-switch-cli) ![](https://img.shields.io/github/stars/SaladDay/cc-switch-cli?style=flat&color=yellow) - Cross-platform CLI All-in-One assistant for Claude Code, Codex and Gemini.
- [agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) ![](https://img.shields.io/github/stars/agent-of-empires/agent-of-empires?style=flat&color=yellow) - Manage multiple Claude Code, OpenCode agents from either TUI or Web for easy access on mob.
- [zclaw](https://github.com/tnm/zclaw) ![](https://img.shields.io/github/stars/tnm/zclaw?style=flat&color=yellow) - Your personal AI assistant at all-in 888KiB (~35KB in app code).
- [Cougar-CLI](https://github.com/dulikaifazr/Cougar-CLI) ![](https://img.shields.io/github/stars/dulikaifazr/Cougar-CLI?style=flat&color=yellow) - Cougar CLI - An AI programming agent for the command line.
- [clawcodex](https://github.com/agentforce314/clawcodex) ![](https://img.shields.io/github/stars/agentforce314/clawcodex?style=flat&color=yellow) - Token efficient Claude Code full Python rebuild.
- [mycoder](https://github.com/bhouston/mycoder) ![](https://img.shields.io/github/stars/bhouston/mycoder?style=flat&color=yellow) - Simple to install, powerful command-line based AI agent system for coding.

## Cloud Coding Agents

- [OpenHands](https://github.com/All-Hands-AI/OpenHands) ![](https://img.shields.io/github/stars/All-Hands-AI/OpenHands?style=flat&color=yellow) - Autonomous coding agent that runs as a self-hosted always-on engineering team.
- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) ![](https://img.shields.io/github/stars/OpenHands/OpenHands?style=flat&color=yellow) - OpenHands: AI-Driven Development.
- [daytona](https://github.com/daytonaio/daytona) ![](https://img.shields.io/github/stars/daytonaio/daytona?style=flat&color=yellow) - Daytona is a Secure and Elastic Infrastructure for Running AI-Generated Code.
- [Bolt.new](https://github.com/stackblitz/bolt.new) ![](https://img.shields.io/github/stars/stackblitz/bolt.new?style=flat&color=yellow) - Prompt, run, edit and deploy full-stack web apps from the browser.
- [InsForge](https://github.com/InsForge/InsForge) ![](https://img.shields.io/github/stars/InsForge/InsForge?style=flat&color=yellow) - The all-in-one, open-source backend platform for agentic coding.
- [humanlayer](https://github.com/humanlayer/humanlayer) ![](https://img.shields.io/github/stars/humanlayer/humanlayer?style=flat&color=yellow) - The best way to get AI coding agents to solve hard problems in complex codebases.
- [vibesdk](https://github.com/cloudflare/vibesdk) ![](https://img.shields.io/github/stars/cloudflare/vibesdk?style=flat&color=yellow) - An open-source vibe coding platform that helps you build your own vibe-coding platform, bu.
- [costrict](https://github.com/zgsm-ai/costrict) ![](https://img.shields.io/github/stars/zgsm-ai/costrict?style=flat&color=yellow) - Costrict - strict AI coder for enterprises, quality first, including AI Agent, AI CodeRevi.
- [MonkeyCode](https://github.com/chaitin/MonkeyCode) ![](https://img.shields.io/github/stars/chaitin/MonkeyCode?style=flat&color=yellow) - AI coding platform for teams.
- [crystal](https://github.com/stravu/crystal) ![](https://img.shields.io/github/stars/stravu/crystal?style=flat&color=yellow) - Run multiple Codex and Claude Code AI sessions in parallel git worktrees.
- [fulling](https://github.com/FullAgent/fulling) ![](https://img.shields.io/github/stars/FullAgent/fulling?style=flat&color=yellow) - Fulling is an AI-powered Full-stack Engineer Agent.
- [vibekit](https://github.com/superagent-ai/vibekit) ![](https://img.shields.io/github/stars/superagent-ai/vibekit?style=flat&color=yellow) - Run Claude Code, Gemini, Codex — or any coding agent — in a clean, isolated sandbox with s.
- [claudebox](https://github.com/RchGrav/claudebox) ![](https://img.shields.io/github/stars/RchGrav/claudebox?style=flat&color=yellow) - The Ultimate Claude Code Docker Development Environment - Run Claude AI's coding assistant.

## Editor Integrations

- [Cline](https://github.com/cline/cline) ![](https://img.shields.io/github/stars/cline/cline?style=flat&color=yellow) - Autonomous coding agent that runs as a VS Code extension.
- [Continue](https://github.com/continuedev/continue) ![](https://img.shields.io/github/stars/continuedev/continue?style=flat&color=yellow) - Open-source AI code assistant extension for VS Code and JetBrains.
- [tabby](https://github.com/TabbyML/tabby) ![](https://img.shields.io/github/stars/TabbyML/tabby?style=flat&color=yellow) - Self-hosted AI coding assistant.
- [AionUi](https://github.com/iOfficeAI/AionUi) ![](https://img.shields.io/github/stars/iOfficeAI/AionUi?style=flat&color=yellow) - Free, local, open-source 24/7 Cowork app for OpenClaw, Hermes Agent, Claude Code, Codex, O.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) ![](https://img.shields.io/github/stars/RooCodeInc/Roo-Code?style=flat&color=yellow) - AI-powered coding agent for VS Code with custom modes and tool control.
- [avante.nvim](https://github.com/yetone/avante.nvim) ![](https://img.shields.io/github/stars/yetone/avante.nvim?style=flat&color=yellow) - Cursor-like AI coding experience inside Neovim.
- [sweep](https://github.com/sweepai/sweep) ![](https://img.shields.io/github/stars/sweepai/sweep?style=flat&color=yellow) - Sweep: AI coding assistant for JetBrains.
- [CopilotForXcode](https://github.com/github/CopilotForXcode) ![](https://img.shields.io/github/stars/github/CopilotForXcode?style=flat&color=yellow) - AI coding assistant for Xcode.
- [sketch](https://github.com/approximatelabs/sketch) ![](https://img.shields.io/github/stars/approximatelabs/sketch?style=flat&color=yellow) - AI code-writing assistant that understands data content.
- [deepseek-engineer](https://github.com/Doriandarko/deepseek-engineer) ![](https://img.shields.io/github/stars/Doriandarko/deepseek-engineer?style=flat&color=yellow) - A powerful coding assistant application that integrates with the DeepSeek API to process u.
- [claude-code.nvim](https://github.com/greggh/claude-code.nvim) ![](https://img.shields.io/github/stars/greggh/claude-code.nvim?style=flat&color=yellow) - Seamless integration between Claude Code AI assistant and Neovim.
- [codemcp](https://github.com/ezyang/codemcp) ![](https://img.shields.io/github/stars/ezyang/codemcp?style=flat&color=yellow) - Coding assistant MCP for Claude Desktop.
- [codefuse-chatbot](https://github.com/codefuse-ai/codefuse-chatbot) ![](https://img.shields.io/github/stars/codefuse-ai/codefuse-chatbot?style=flat&color=yellow) - An intelligent assistant serving the entire software development lifecycle, powered by a M.
- [vim-ai](https://github.com/madox2/vim-ai) ![](https://img.shields.io/github/stars/madox2/vim-ai?style=flat&color=yellow) - AI-powered code assistant for Vim.

## Code Review, Testing and Quality

- [Claude Code Action](https://github.com/anthropics/claude-code-action) ![](https://img.shields.io/github/stars/anthropics/claude-code-action?style=flat&color=yellow) - GitHub Action that lets Claude review PRs and fix issues in CI.
- [XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) ![](https://img.shields.io/github/stars/getsentry/XcodeBuildMCP?style=flat&color=yellow) - A Model Context Protocol (MCP) server and CLI that provides tools for agent use when worki.
- [APIAuto](https://github.com/TommyLemon/APIAuto) ![](https://img.shields.io/github/stars/TommyLemon/APIAuto?style=flat&color=yellow) - The most advanced HTTP API tool - zero-code testing, AI Q&A, code generation and docs.
- [rockpack](https://github.com/AlexSergey/rockpack) ![](https://img.shields.io/github/stars/AlexSergey/rockpack?style=flat&color=yellow) - Zero-config React with built-in SSR, automated quality gates, and AI-ready project structu.
- [claude-debugs-for-you](https://github.com/jasonjmcghee/claude-debugs-for-you) ![](https://img.shields.io/github/stars/jasonjmcghee/claude-debugs-for-you?style=flat&color=yellow) - Enable any LLM (e.g.

## DevOps and Cloud Automation

- [kestra](https://github.com/kestra-io/kestra) ![](https://img.shields.io/github/stars/kestra-io/kestra?style=flat&color=yellow) - Event Driven Orchestration & Scheduling Platform for Mission Critical Applications.
- [trigger.dev](https://github.com/triggerdotdev/trigger.dev) ![](https://img.shields.io/github/stars/triggerdotdev/trigger.dev?style=flat&color=yellow) - Trigger.dev – build and deploy fully‑managed AI agents and workflows.
- [infracost](https://github.com/infracost/infracost) ![](https://img.shields.io/github/stars/infracost/infracost?style=flat&color=yellow) - Cloud cost intelligence for engineers, AI coding agents, and CI/CD  Shift FinOps Left!.
- [nginx-ui](https://github.com/0xJacky/nginx-ui) ![](https://img.shields.io/github/stars/0xJacky/nginx-ui?style=flat&color=yellow) - Yet another WebUI for Nginx.
- [mcp](https://github.com/awslabs/mcp) ![](https://img.shields.io/github/stars/awslabs/mcp?style=flat&color=yellow) - Open source MCP Servers for AWS.
- [Chaterm](https://github.com/chaterm/Chaterm) ![](https://img.shields.io/github/stars/chaterm/Chaterm?style=flat&color=yellow) - Open source AI terminal for cloud and infrastructure management, enabling you to deploy, t.
- [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) ![](https://img.shields.io/github/stars/containers/kubernetes-mcp-server?style=flat&color=yellow) - Model Context Protocol (MCP) server for Kubernetes and OpenShift.

## Security and Pentest Agents

- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) ![](https://img.shields.io/github/stars/CloakHQ/CloakBrowser?style=flat&color=yellow) - Stealth Chromium that passes every bot detection test.
- [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) ![](https://img.shields.io/github/stars/mukul975/Anthropic-Cybersecurity-Skills?style=flat&color=yellow) - Provides 817 structured cybersecurity skills for AI agents across 6 frameworks.
- [PentestGPT](https://github.com/GreyDGL/PentestGPT) ![](https://img.shields.io/github/stars/GreyDGL/PentestGPT?style=flat&color=yellow) - Automated Penetration Testing Agentic Framework Powered by Large Language Models.
- [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) ![](https://img.shields.io/github/stars/0x4m4/hexstrike-ai?style=flat&color=yellow) - HexStrike AI MCP Agents is an advanced MCP server that lets AI agents (Claude, GPT, Copilo.
- [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) ![](https://img.shields.io/github/stars/mrexodia/ida-pro-mcp?style=flat&color=yellow) - AI-powered reverse engineering assistant that bridges IDA Pro with language models through.
- [Viper](https://github.com/FunnyWolf/Viper) ![](https://img.shields.io/github/stars/FunnyWolf/Viper?style=flat&color=yellow) - Adversary simulation and Red teaming platform with AI.
- [ENScan_GO](https://github.com/wgpsec/ENScan_GO) ![](https://img.shields.io/github/stars/wgpsec/ENScan_GO?style=flat&color=yellow) - Enterprise information collection tool - gathers ICP, APP and WeChat data via APIs.
- [EvilClippy](https://github.com/outflanknl/EvilClippy) ![](https://img.shields.io/github/stars/outflanknl/EvilClippy?style=flat&color=yellow) - A cross-platform assistant for creating malicious MS Office documents.
- [pentest-ai-agents](https://github.com/0xSteph/pentest-ai-agents) ![](https://img.shields.io/github/stars/0xSteph/pentest-ai-agents?style=flat&color=yellow) - Turn Claude Code into your offensive security research assistant.

## Browser and Web Automation

- [firecrawl](https://github.com/firecrawl/firecrawl) ![](https://img.shields.io/github/stars/firecrawl/firecrawl?style=flat&color=yellow) - The API to search, scrape, and interact with the web at scale.
- [browser-use](https://github.com/browser-use/browser-use) ![](https://img.shields.io/github/stars/browser-use/browser-use?style=flat&color=yellow) - Make websites accessible for AI agents.
- [Scrapling](https://github.com/D4Vinci/Scrapling) ![](https://img.shields.io/github/stars/D4Vinci/Scrapling?style=flat&color=yellow) - An adaptive Web Scraping framework that handles everything from a single request to a f.
- [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ![](https://img.shields.io/github/stars/ChromeDevTools/chrome-devtools-mcp?style=flat&color=yellow) - Chrome DevTools for coding agents.
- [OpenCLI](https://github.com/jackwener/OpenCLI) ![](https://img.shields.io/github/stars/jackwener/OpenCLI?style=flat&color=yellow) - Make Any Website into CLI & Use your logged-in browser by AI agent.
- [Stagehand](https://github.com/browserbase/stagehand) ![](https://img.shields.io/github/stars/browserbase/stagehand?style=flat&color=yellow) - SDK for building reliable browser agents with simple AI primitives.
- [lamda](https://github.com/firerpa/lamda) ![](https://img.shields.io/github/stars/firerpa/lamda?style=flat&color=yellow) - Android Full-Stack Device Control Platform: WebRTC/H.264 remote desktop, UI/OCR/image-matc.
- [browser-tools-mcp](https://github.com/AgentDeskAI/browser-tools-mcp) ![](https://img.shields.io/github/stars/AgentDeskAI/browser-tools-mcp?style=flat&color=yellow) - Monitor browser logs directly from Cursor and other MCP compatible IDEs.
- [firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ![](https://img.shields.io/github/stars/firecrawl/firecrawl-mcp-server?style=flat&color=yellow) - Official Firecrawl MCP Server - Adds powerful web scraping and search to Cursor, Claude.
- [BrowserMCP/mcp](https://github.com/BrowserMCP/mcp) ![](https://img.shields.io/github/stars/BrowserMCP/mcp?style=flat&color=yellow) - Browser MCP is a Model Context Provider (MCP) server that allows AI applications to contro.
- [exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ![](https://img.shields.io/github/stars/exa-labs/exa-mcp-server?style=flat&color=yellow) - Exa MCP for web search and web crawling!.
- [mcp-crawl4ai-rag](https://github.com/coleam00/mcp-crawl4ai-rag) ![](https://img.shields.io/github/stars/coleam00/mcp-crawl4ai-rag?style=flat&color=yellow) - Web Crawling and RAG Capabilities for AI Agents and AI Coding Assistants.
- [GreasyFork-Scripts](https://github.com/F9y4ng/GreasyFork-Scripts) ![](https://img.shields.io/github/stars/F9y4ng/GreasyFork-Scripts?style=flat&color=yellow) - The open source code of this project is used for userscripts (油猴脚本) for desktop browsers,.

## Design to Code and Frontend

- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) ![](https://img.shields.io/github/stars/VoltAgent/awesome-design-md?style=flat&color=yellow) - A collection of DESIGN.md files analysis by popular brand design systems.
- [open-design](https://github.com/nexu-io/open-design) ![](https://img.shields.io/github/stars/nexu-io/open-design?style=flat&color=yellow) - Local-first, open-source Claude Design alternative.
- [Front-End-Checklist](https://github.com/thedaviddias/Front-End-Checklist) ![](https://img.shields.io/github/stars/thedaviddias/Front-End-Checklist?style=flat&color=yellow) - The essential checklist for modern web development, for humans and AI agents.
- [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) ![](https://img.shields.io/github/stars/bytedance/UI-TARS-desktop?style=flat&color=yellow) - The Open-Source Multimodal AI Agent Stack: Connecting Cutting-Edge AI Models and Agent Inf.
- [onlook](https://github.com/onlook-dev/onlook) ![](https://img.shields.io/github/stars/onlook-dev/onlook?style=flat&color=yellow) - The Cursor for Designers • An Open-Source AI-First Design tool • Visually build, style, an.
- [ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) ![](https://img.shields.io/github/stars/JCodesMore/ai-website-cloner-template?style=flat&color=yellow) - Clone any website with one command using AI coding agents.
- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) ![](https://img.shields.io/github/stars/zarazhangrui/frontend-slides?style=flat&color=yellow) - Create beautiful slides on the web using a coding agent's frontend skills.
- [Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ![](https://img.shields.io/github/stars/GLips/Figma-Context-MCP?style=flat&color=yellow) - MCP server to provide Figma layout information to AI coding agents like Cursor.
- [gsap-skills](https://github.com/greensock/gsap-skills) ![](https://img.shields.io/github/stars/greensock/gsap-skills?style=flat&color=yellow) - Official AI skills for GSAP.
- [html-anything](https://github.com/nexu-io/html-anything) ![](https://img.shields.io/github/stars/nexu-io/html-anything?style=flat&color=yellow) - The agentic HTML editor — your local AI agent writes the HTML, you ship it.
- [cursor-talk-to-figma-mcp](https://github.com/grab/cursor-talk-to-figma-mcp) ![](https://img.shields.io/github/stars/grab/cursor-talk-to-figma-mcp?style=flat&color=yellow) - TalkToFigma: MCP integration between AI Agent (Cursor, Claude Code, Codex) and Figma, allo.
- [WordPress/agent-skills](https://github.com/WordPress/agent-skills) ![](https://img.shields.io/github/stars/WordPress/agent-skills?style=flat&color=yellow) - Expert-level WordPress knowledge for AI coding assistants - blocks, themes, plugins, and b.
- [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) ![](https://img.shields.io/github/stars/callstackincubator/agent-skills?style=flat&color=yellow) - A collection of agent-optimized React Native skills for AI coding assistants.

## App Builders and Low-Code

- [n8n](https://github.com/n8n-io/n8n) ![](https://img.shields.io/github/stars/n8n-io/n8n?style=flat&color=yellow) - Fair-code workflow automation platform with native AI capabilities.
- [langflow](https://github.com/langflow-ai/langflow) ![](https://img.shields.io/github/stars/langflow-ai/langflow?style=flat&color=yellow) - Langflow is a powerful tool for building and deploying AI-powered agents and workflows.
- [dify](https://github.com/langgenius/dify) ![](https://img.shields.io/github/stars/langgenius/dify?style=flat&color=yellow) - Production-ready platform for agentic workflow development.
- [Flowise](https://github.com/FlowiseAI/Flowise) ![](https://img.shields.io/github/stars/FlowiseAI/Flowise?style=flat&color=yellow) - Build AI Agents, Visually.
- [JeecgBoot](https://github.com/jeecgboot/JeecgBoot) ![](https://img.shields.io/github/stars/jeecgboot/JeecgBoot?style=flat&color=yellow) - AI 低代码平台「低代码 + 零代码」双驱动！低代码可一键生成前后端代码;零代码可 5 分钟搭建系统;AI Skills 一句话画流程、设计表单、生成整套系统。内置 AI聊天、知识.
- [activepieces](https://github.com/activepieces/activepieces) ![](https://img.shields.io/github/stars/activepieces/activepieces?style=flat&color=yellow) - AI Agents & MCPs & AI Workflow Automation • (~400 MCP servers for AI agents) • AI Automati.
- [n8n-mcp](https://github.com/czlonkowski/n8n-mcp) ![](https://img.shields.io/github/stars/czlonkowski/n8n-mcp?style=flat&color=yellow) - A MCP for Claude Desktop / Claude Code / Windsurf / Cursor to build n8n workflows for you.
- [MaxKB](https://github.com/1Panel-dev/MaxKB) ![](https://img.shields.io/github/stars/1Panel-dev/MaxKB?style=flat&color=yellow) - MaxKB is an open-source platform for building enterprise-grade agents.
- [bisheng](https://github.com/dataelement/bisheng) ![](https://img.shields.io/github/stars/dataelement/bisheng?style=flat&color=yellow) - BISHENG is an open LLM devops platform for next generation Enterprise AI applications.
- [refly](https://github.com/refly-ai/refly) ![](https://img.shields.io/github/stars/refly-ai/refly?style=flat&color=yellow) - The first open-source agent skills builder.
- [pyspur](https://github.com/PySpur-Dev/pyspur) ![](https://img.shields.io/github/stars/PySpur-Dev/pyspur?style=flat&color=yellow) - A visual playground for agentic workflows: Iterate over your agents 10x faster.
- [oinone-pamirs](https://github.com/oinone/oinone-pamirs) ![](https://img.shields.io/github/stars/oinone/oinone-pamirs?style=flat&color=yellow) - Oinone is an AI‑Powered low‑code framework that unifies AI and developers around a shared.
- [agents](https://github.com/inkeep/agents) ![](https://img.shields.io/github/stars/inkeep/agents?style=flat&color=yellow) - Create AI Agents in a No-Code Visual Builder or TypeScript SDK with full 2-way sync.

## Game Development

- [GDevelop](https://github.com/4ian/GDevelop) ![](https://img.shields.io/github/stars/4ian/GDevelop?style=flat&color=yellow) - Open-source, cross-platform 2D/3D/multiplayer game engine designed for everyone.
- [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) ![](https://img.shields.io/github/stars/Donchitos/Claude-Code-Game-Studios?style=flat&color=yellow) - Turn Claude Code into a full game dev studio — 49 AI agents, 72 workflow skills, and a com.

## Context, Memory and Codebase Indexing

- [claude-mem](https://github.com/thedotmack/claude-mem) ![](https://img.shields.io/github/stars/thedotmack/claude-mem?style=flat&color=yellow) - Persistent Context Across Sessions for Every Agent –  Captures everything your agent does.
- [ragflow](https://github.com/infiniflow/ragflow) ![](https://img.shields.io/github/stars/infiniflow/ragflow?style=flat&color=yellow) - RAGFlow is a leading open-source Retrieval-Augmented Generation (RAG) engine that fuses cu.
- [graphify](https://github.com/safishamsi/graphify) ![](https://img.shields.io/github/stars/safishamsi/graphify?style=flat&color=yellow) - AI coding assistant skill (Claude Code, Codex, OpenCode, Cursor, Gemini CLI, and more).
- [mem0](https://github.com/mem0ai/mem0) ![](https://img.shields.io/github/stars/mem0ai/mem0?style=flat&color=yellow) - Universal memory layer for AI Agents.
- [mempalace](https://github.com/MemPalace/mempalace) ![](https://img.shields.io/github/stars/MemPalace/mempalace?style=flat&color=yellow) - The best-benchmarked open-source AI memory system.
- [headroom](https://github.com/headroomlabs-ai/headroom) ![](https://img.shields.io/github/stars/headroomlabs-ai/headroom?style=flat&color=yellow) - Compress tool outputs, logs, files, and RAG chunks before they reach the LLM.
- [llama_index](https://github.com/run-llama/llama_index) ![](https://img.shields.io/github/stars/run-llama/llama_index?style=flat&color=yellow) - LlamaIndex is the leading document agent and OCR platform.
- [LightRAG](https://github.com/HKUDS/LightRAG) ![](https://img.shields.io/github/stars/HKUDS/LightRAG?style=flat&color=yellow) - Simple and Fast Retrieval-Augmented Generation.
- [Vane](https://github.com/ItzCrazyKns/Vane) ![](https://img.shields.io/github/stars/ItzCrazyKns/Vane?style=flat&color=yellow) - Vane is an AI-powered answering engine.
- [PageIndex](https://github.com/VectifyAI/PageIndex) ![](https://img.shields.io/github/stars/VectifyAI/PageIndex?style=flat&color=yellow) - PageIndex: Document Index for Vectorless, Reasoning-based RAG.
- [chroma](https://github.com/chroma-core/chroma) ![](https://img.shields.io/github/stars/chroma-core/chroma?style=flat&color=yellow) - Search infrastructure for AI.
- [cognee](https://github.com/topoteretes/cognee) ![](https://img.shields.io/github/stars/topoteretes/cognee?style=flat&color=yellow) - Cognee is the open-source AI memory platform for agents.
- [Repomix](https://github.com/yamadashy/repomix) ![](https://img.shields.io/github/stars/yamadashy/repomix?style=flat&color=yellow) - Pack your whole repository into a single file for AI consumption.
- [serena](https://github.com/oraios/serena) ![](https://img.shields.io/github/stars/oraios/serena?style=flat&color=yellow) - A powerful MCP toolkit for coding, providing semantic retrieval and editing capabilities.
- [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ![](https://img.shields.io/github/stars/DeusData/codebase-memory-mcp?style=flat&color=yellow) - High-performance code intelligence MCP server.
- [agentmemory](https://github.com/rohitg00/agentmemory) ![](https://img.shields.io/github/stars/rohitg00/agentmemory?style=flat&color=yellow) - Persistent memory for AI coding agents based on real-world benchmarks.
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) ![](https://img.shields.io/github/stars/open-metadata/OpenMetadata?style=flat&color=yellow) - The Open Context Layer for Data and AI ,  OpenMetadata is the open platform for building t.
- [claude-context](https://github.com/zilliztech/claude-context) ![](https://img.shields.io/github/stars/zilliztech/claude-context?style=flat&color=yellow) - Code search MCP for Claude Code.
- [code2prompt](https://github.com/mufeedvh/code2prompt) ![](https://img.shields.io/github/stars/mufeedvh/code2prompt?style=flat&color=yellow) - CLI that converts a codebase into a single Markdown prompt for LLMs.
- [semble](https://github.com/MinishLab/semble) ![](https://img.shields.io/github/stars/MinishLab/semble?style=flat&color=yellow) - Fast and Accurate Code Search for Agents.
- [byterover-cli](https://github.com/campfirein/byterover-cli) ![](https://img.shields.io/github/stars/campfirein/byterover-cli?style=flat&color=yellow) - ByteRover CLI (brv) - The portable memory layer for  autonomous coding agents (formerly Ci.
- [Zep](https://github.com/getzep/zep) ![](https://img.shields.io/github/stars/getzep/zep?style=flat&color=yellow) - Long-term memory service for conversational and agentic AI.
- [CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext) ![](https://img.shields.io/github/stars/CodeGraphContext/CodeGraphContext?style=flat&color=yellow) - An MCP server plus a CLI tool that indexes local code into a graph database to provide con.
- [RooFlow](https://github.com/GreatScottyMac/RooFlow) ![](https://img.shields.io/github/stars/GreatScottyMac/RooFlow?style=flat&color=yellow) - RooFlow - Enhanced Memory Bank System with Footgun Power  Next-gen Memory Bank system.

## MCP Servers and Clients

- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) ![](https://img.shields.io/github/stars/punkpeye/awesome-mcp-servers?style=flat&color=yellow) - Curated collection of Model Context Protocol servers.
- [MCP Servers](https://github.com/modelcontextprotocol/servers) ![](https://img.shields.io/github/stars/modelcontextprotocol/servers?style=flat&color=yellow) - Reference implementations of Model Context Protocol servers.
- [GitHub MCP Server](https://github.com/github/github-mcp-server) ![](https://img.shields.io/github/stars/github/github-mcp-server?style=flat&color=yellow) - GitHub's official MCP server for interacting with repos, issues and PRs.
- [FastMCP](https://github.com/PrefectHQ/fastmcp) ![](https://img.shields.io/github/stars/PrefectHQ/fastmcp?style=flat&color=yellow) - Fast, Pythonic framework for building MCP servers and clients.
- [fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) ![](https://img.shields.io/github/stars/tadata-org/fastapi_mcp?style=flat&color=yellow) - Expose your FastAPI endpoints as Model Context Protocol (MCP) tools, with Auth!.
- [mcp-use](https://github.com/mcp-use/mcp-use) ![](https://img.shields.io/github/stars/mcp-use/mcp-use?style=flat&color=yellow) - The fullstack MCP framework to develop MCP Apps for ChatGPT / Claude & MCP Servers for AI.
- [Awesome-MCP-ZH](https://github.com/yzfly/Awesome-MCP-ZH) ![](https://img.shields.io/github/stars/yzfly/Awesome-MCP-ZH?style=flat&color=yellow) - MCP 资源精选， MCP指南，Claude MCP，MCP Servers, MCP Clients.
- [DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP) ![](https://img.shields.io/github/stars/wonderwhy-er/DesktopCommanderMCP?style=flat&color=yellow) - This is MCP server for Claude that gives it terminal control, file system search and diff.
- [klavis](https://github.com/Klavis-AI/klavis) ![](https://img.shields.io/github/stars/Klavis-AI/klavis?style=flat&color=yellow) - Klavis AI:  MCP integration platforms that let AI agents use tools reliably at any scale.
- [metamcp](https://github.com/metatool-ai/metamcp) ![](https://img.shields.io/github/stars/metatool-ai/metamcp?style=flat&color=yellow) - MCP Aggregator, Orchestrator, Middleware, Gateway in one docker.

## Agent Skills, Prompts and Rules

- [prompts.chat](https://github.com/f/prompts.chat) ![](https://img.shields.io/github/stars/f/prompts.chat?style=flat&color=yellow) - Awesome ChatGPT Prompts - share, discover and collect prompts from the community.
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) ![](https://img.shields.io/github/stars/x1xhlol/system-prompts-and-models-of-ai-tools?style=flat&color=yellow) - FULL Augment Code, Claude Code, Cluely, CodeBuddy, Comet, Cursor, Devin AI, Junie, Kiro, L.
- [caveman](https://github.com/JuliusBrussee/caveman) ![](https://img.shields.io/github/stars/JuliusBrussee/caveman?style=flat&color=yellow) - Claude Code skill that cuts 65% of tokens by talking like a caveman.
- [ponytail](https://github.com/DietrichGebert/ponytail) ![](https://img.shields.io/github/stars/DietrichGebert/ponytail?style=flat&color=yellow) - Makes your AI agent think like the laziest senior dev in the room.
- [agent-skills](https://github.com/addyosmani/agent-skills) ![](https://img.shields.io/github/stars/addyosmani/agent-skills?style=flat&color=yellow) - Production-grade engineering skills for AI coding agents.
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) ![](https://img.shields.io/github/stars/ComposioHQ/awesome-claude-skills?style=flat&color=yellow) - A curated list of awesome Claude Skills, resources, and tools for customizing Claude AI wo.
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) ![](https://img.shields.io/github/stars/code-yeongyu/oh-my-openagent?style=flat&color=yellow) - Coding agent harness for complex codebases - for Codex and OpenClaw.
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) ![](https://img.shields.io/github/stars/shanraisshan/claude-code-best-practice?style=flat&color=yellow) - From vibe coding to agentic engineering - practice makes Claude perfect.
- [taste-skill](https://github.com/Leonxlnx/taste-skill) ![](https://img.shields.io/github/stars/Leonxlnx/taste-skill?style=flat&color=yellow) - Taste-Skill - gives your AI good taste.
- [system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) ![](https://img.shields.io/github/stars/asgeirtj/system_prompts_leaks?style=flat&color=yellow) - Extracted system prompts from Anthropic - Claude Fable 5, Opus 4.8, Claude Code, Claude De.
- [cherry-studio](https://github.com/CherryHQ/cherry-studio) ![](https://img.shields.io/github/stars/CherryHQ/cherry-studio?style=flat&color=yellow) - AI productivity studio with smart chat, autonomous agents, and 300+ assistants.
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) ![](https://img.shields.io/github/stars/hesreallyhim/awesome-claude-code?style=flat&color=yellow) - A curated list of awesome skills, hooks, slash-commands, agent orchestrators, applications.
- [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) ![](https://img.shields.io/github/stars/elder-plinius/CL4R1T4S?style=flat&color=yellow) - LEAKED SYSTEM PROMPTS FOR CHATGPT, CLAUDE, GEMINI, GROK, PERPLEXITY, CURSOR, LOVABLE, REPL.
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) ![](https://img.shields.io/github/stars/sickn33/antigravity-awesome-skills?style=flat&color=yellow) - Installable GitHub library of 1,800+ agentic skills for Claude Code, Cursor, Codex CLI, Ge.
- [awesome-copilot](https://github.com/github/awesome-copilot) ![](https://img.shields.io/github/stars/github/awesome-copilot?style=flat&color=yellow) - Community-contributed instructions, agents, skills, and configurations to help you make th.
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) ![](https://img.shields.io/github/stars/Imbad0202/academic-research-skills?style=flat&color=yellow) - Academic Research Skills for Claude Code: research → write → review → revise → finalize.
- [marketingskills](https://github.com/coreyhaines31/marketingskills) ![](https://img.shields.io/github/stars/coreyhaines31/marketingskills?style=flat&color=yellow) - Marketing skills for Claude Code and AI agents.
- [prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) ![](https://img.shields.io/github/stars/linshenkx/prompt-optimizer?style=flat&color=yellow) - An AI prompt optimizer for writing better prompts and getting better AI results.
- [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) ![](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat&color=yellow) - Turn any AI agent into an AI Scientist.
- [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) ![](https://img.shields.io/github/stars/VoltAgent/awesome-agent-skills?style=flat&color=yellow) - A curated collection of 1000+ agent skills from official dev teams and the community, comp.
- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) ![](https://img.shields.io/github/stars/OthmanAdi/planning-with-files?style=flat&color=yellow) - Persistent file-based planning for AI coding agents and long-running agentic tasks.
- [claude-skills](https://github.com/alirezarezvani/claude-skills) ![](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=flat&color=yellow) - Claude Code skills and agent skills plugins for 13 AI coding tools.
- [context-mode](https://github.com/mksglu/context-mode) ![](https://img.shields.io/github/stars/mksglu/context-mode?style=flat&color=yellow) - Context window optimization for AI coding agents.
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) ![](https://img.shields.io/github/stars/teng-lin/notebooklm-py?style=flat&color=yellow) - Unofficial Python API and agentic skill for Google NotebookLM.
- [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) ![](https://img.shields.io/github/stars/jnMetaCode/agency-agents-zh?style=flat&color=yellow) - Provides 266 plug-and-play AI expert roles for Claude Code, Cursor, Copilot and 15 more tools.
- [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) ![](https://img.shields.io/github/stars/yusufkaraaslan/Skill_Seekers?style=flat&color=yellow) - Convert documentation websites, GitHub repositories, and PDFs into Claude AI skills with a.
- [Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) ![](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&color=yellow) - ARIS  (Auto-Research-In-Sleep) — Lightweight Markdown-only skills for autonomous ML rese.
- [awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) ![](https://img.shields.io/github/stars/YouMind-OpenLab/awesome-nano-banana-pro-prompts?style=flat&color=yellow) - World's largest Nano Banana Pro prompt library — 10,000+ curated prompts with preview im.
- [LangGPT](https://github.com/langgptai/LangGPT) ![](https://img.shields.io/github/stars/langgptai/LangGPT?style=flat&color=yellow) - LangGPT: Empowering everyone to become a prompt expert!    结构化提示词（Structured Prompt）提出者.
- [chatgpt_system_prompt](https://github.com/LouisShark/chatgpt_system_prompt) ![](https://img.shields.io/github/stars/LouisShark/chatgpt_system_prompt?style=flat&color=yellow) - A collection of GPT system prompts and various prompt injection/leaking knowledge.
- [openskills](https://github.com/numman-ali/openskills) ![](https://img.shields.io/github/stars/numman-ali/openskills?style=flat&color=yellow) - Universal skills loader for AI coding agents - npm i -g openskills.
- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) ![](https://img.shields.io/github/stars/Orchestra-Research/AI-Research-SKILLs?style=flat&color=yellow) - Comprehensive open-source library of AI research and engineering skills for any AI model.
- [prompt-master](https://github.com/nidhinjs/prompt-master) ![](https://img.shields.io/github/stars/nidhinjs/prompt-master?style=flat&color=yellow) - A Claude skill that writes the accurate prompts for any AI tool.
- [awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro) ![](https://img.shields.io/github/stars/ZeroLu/awesome-nanobanana-pro?style=flat&color=yellow) - An awesome list of curated Nano Banana pro prompts and examples.
- [ChatGPT-Shortcut](https://github.com/rockbenben/ChatGPT-Shortcut) ![](https://img.shields.io/github/stars/rockbenben/ChatGPT-Shortcut?style=flat&color=yellow) - Maximize your efficiency and productivity.
- [awesome-prompts](https://github.com/ai-boost/awesome-prompts) ![](https://img.shields.io/github/stars/ai-boost/awesome-prompts?style=flat&color=yellow) - Curated list of chatgpt prompts from the top-rated GPTs in the GPTs Store.
- [ccpm](https://github.com/automazeio/ccpm) ![](https://img.shields.io/github/stars/automazeio/ccpm?style=flat&color=yellow) - Project management skill system for Agents that uses GitHub Issues and Git worktrees for p.
- [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) ![](https://img.shields.io/github/stars/freestylefly/awesome-gpt-image-2?style=flat&color=yellow) - Prompt as Code | GPT-Image2 工业级提示词引擎与模板库，470+ 个案例逆向工程，20+ 套工业级模板，并提炼出Skills，持续更新中.
- [awesome-gpt4o-images](https://github.com/jamez-bondos/awesome-gpt4o-images) ![](https://img.shields.io/github/stars/jamez-bondos/awesome-gpt4o-images?style=flat&color=yellow) - Awesome curated collection of images and prompts generated by GPT-4o and gpt-image-1.
- [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) ![](https://img.shields.io/github/stars/YouMind-OpenLab/awesome-gpt-image-2?style=flat&color=yellow) - World's largest GPT Image 2 prompt library, updated daily — 2000+ curated prompts with p.
- [Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering) ![](https://img.shields.io/github/stars/NirDiamant/Prompt_Engineering?style=flat&color=yellow) - Prompt engineering techniques with hands-on Jupyter Notebook tutorials.
- [SuperPrompt](https://github.com/NeoVertex1/SuperPrompt) ![](https://img.shields.io/github/stars/NeoVertex1/SuperPrompt?style=flat&color=yellow) - SuperPrompt is an attempt to engineer prompts that might help us understand AI agents.
- [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) ![](https://img.shields.io/github/stars/jnMetaCode/superpowers-zh?style=flat&color=yellow) - AI 编程超能力 · 中文增强版 — superpowers（116k+ ）完整汉化 + 6 个中国原创 skills，让 Claude Code / Copilot CLI.
- [ai-notes](https://github.com/swyxio/ai-notes) ![](https://img.shields.io/github/stars/swyxio/ai-notes?style=flat&color=yellow) - Notes for software engineers getting up to speed on new AI developments.
- [wonderful-prompts](https://github.com/langgptai/wonderful-prompts) ![](https://img.shields.io/github/stars/langgptai/wonderful-prompts?style=flat&color=yellow) - Curated Chinese ChatGPT prompts - usage guide to boost playability and usability.
- [Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) ![](https://img.shields.io/github/stars/promptslab/Awesome-Prompt-Engineering?style=flat&color=yellow) - This repository contains a hand-curated resources for Prompt Engineering with a focus on G.
- [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) ![](https://img.shields.io/github/stars/dontriskit/awesome-ai-system-prompts?style=flat&color=yellow) - Curated collection of system prompts for top AI tools.
- [ell](https://github.com/MadcowD/ell) ![](https://img.shields.io/github/stars/MadcowD/ell?style=flat&color=yellow) - A language model programming library.
- [Learning-Prompt](https://github.com/thinkingjimmy/Learning-Prompt) ![](https://img.shields.io/github/stars/thinkingjimmy/Learning-Prompt?style=flat&color=yellow) - Free prompt engineering online course.
- [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) ![](https://img.shields.io/github/stars/FlorianBruniaux/claude-code-ultimate-guide?style=flat&color=yellow) - The most comprehensive Claude Code guide: agentic workflows, hooks, skills, MCP servers, q.
- [agents-cli](https://github.com/google/agents-cli) ![](https://img.shields.io/github/stars/google/agents-cli?style=flat&color=yellow) - The CLI and skills that turn any coding assistant into an expert at creating, evaluating,.
- [ruler](https://github.com/intellectronica/ruler) ![](https://img.shields.io/github/stars/intellectronica/ruler?style=flat&color=yellow) - Ruler — apply the same rules to all coding agents.
- [vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template) ![](https://img.shields.io/github/stars/KhazP/vibe-coding-prompt-template?style=flat&color=yellow) - Templates and workflow for generating PRDs, Tech Designs, and MVP and more using LLMs for.
- [cc-skills-golang](https://github.com/samber/cc-skills-golang) ![](https://img.shields.io/github/stars/samber/cc-skills-golang?style=flat&color=yellow) - A collection of Golang agentic skills for coding assistants.
- [Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) ![](https://img.shields.io/github/stars/foryourhealth111-pixel/Vibe-Skills?style=flat&color=yellow) - Vibe-Skills is an all-in-one AI skills package.
- [best-skills](https://github.com/xstongxue/best-skills) ![](https://img.shields.io/github/stars/xstongxue/best-skills?style=flat&color=yellow) - High-quality Skills collection for Cursor, Claude Code, Codex and other agent tools.
- [Sunbeam](https://github.com/pomdtr/sunbeam) ![](https://img.shields.io/github/stars/pomdtr/sunbeam?style=flat&color=yellow) - Browse and search prompt libraries and convert them to any format.

## AI Assistants

- [ECC](https://github.com/affaan-m/ECC) ![](https://img.shields.io/github/stars/affaan-m/ECC?style=flat&color=yellow) - The agent harness performance optimization system.
- [hermes-agent](https://github.com/NousResearch/hermes-agent) ![](https://img.shields.io/github/stars/NousResearch/hermes-agent?style=flat&color=yellow) - The agent that grows with you.
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) ![](https://img.shields.io/github/stars/Significant-Gravitas/AutoGPT?style=flat&color=yellow) - AutoGPT is the vision of accessible AI for everyone, to use and to build on.
- [langchain](https://github.com/langchain-ai/langchain) ![](https://img.shields.io/github/stars/langchain-ai/langchain?style=flat&color=yellow) - The agent engineering platform.
- [deer-flow](https://github.com/bytedance/deer-flow) ![](https://img.shields.io/github/stars/bytedance/deer-flow?style=flat&color=yellow) - An open-source long-horizon SuperAgent harness that researches, codes, and creates.
- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) ![](https://img.shields.io/github/stars/FoundationAgents/MetaGPT?style=flat&color=yellow) - The Multi-Agent Framework: First AI Software Company, Towards Natural Language Programmi.
- [Claude Flow](https://github.com/ruvnet/claude-flow) ![](https://img.shields.io/github/stars/ruvnet/claude-flow?style=flat&color=yellow) - Orchestrate swarms of Claude Code agents on complex tasks.
- [ruflo](https://github.com/ruvnet/ruflo) ![](https://img.shields.io/github/stars/ruvnet/ruflo?style=flat&color=yellow) - The leading agent meta-harness.
- [crewAI](https://github.com/crewAIInc/crewAI) ![](https://img.shields.io/github/stars/crewAIInc/crewAI?style=flat&color=yellow) - Framework for orchestrating role-playing, autonomous AI agents.
- [agno](https://github.com/agno-agi/agno) ![](https://img.shields.io/github/stars/agno-agi/agno?style=flat&color=yellow) - Build, run, and manage agent platforms.
- [wshobson/agents](https://github.com/wshobson/agents) ![](https://img.shields.io/github/stars/wshobson/agents?style=flat&color=yellow) - Library of specialized Claude Code subagents for agentic workflows.
- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) ![](https://img.shields.io/github/stars/Yeachan-Heo/oh-my-claudecode?style=flat&color=yellow) - Teams-first Multi-agent orchestration for Claude Code.
- [langgraph](https://github.com/langchain-ai/langgraph) ![](https://img.shields.io/github/stars/langchain-ai/langgraph?style=flat&color=yellow) - Build resilient agents.
- [nanoclaw](https://github.com/nanocoai/nanoclaw) ![](https://img.shields.io/github/stars/nanocoai/nanoclaw?style=flat&color=yellow) - A lightweight alternative to OpenClaw that runs in containers for security.
- [composio](https://github.com/ComposioHQ/composio) ![](https://img.shields.io/github/stars/ComposioHQ/composio?style=flat&color=yellow) - Composio powers 1000+ toolkits, tool search, context management, authentication, and a san.
- [agentscope](https://github.com/agentscope-ai/agentscope) ![](https://img.shields.io/github/stars/agentscope-ai/agentscope?style=flat&color=yellow) - Build and run agents you can see, understand and trust.
- [haystack](https://github.com/deepset-ai/haystack) ![](https://img.shields.io/github/stars/deepset-ai/haystack?style=flat&color=yellow) - Open-source AI orchestration framework for building context-engineered, production-ready L.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) ![](https://img.shields.io/github/stars/humanlayer/12-factor-agents?style=flat&color=yellow) - Principles for building production-grade LLM-powered agent software.
- [adk-python](https://github.com/google/adk-python) ![](https://img.shields.io/github/stars/google/adk-python?style=flat&color=yellow) - An open-source, code-first Python toolkit for building, evaluating, and deploying sophisti.
- [eliza](https://github.com/elizaOS/eliza) ![](https://img.shields.io/github/stars/elizaOS/eliza?style=flat&color=yellow) - Open source agentic operating system.
- [camel](https://github.com/camel-ai/camel) ![](https://img.shields.io/github/stars/camel-ai/camel?style=flat&color=yellow) - CAMEL: The first and the best multi-agent framework.
- [PocketFlow-Tutorial-Codebase-Knowledge](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) ![](https://img.shields.io/github/stars/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge?style=flat&color=yellow) - Pocket Flow: Codebase to Tutorial.
- [PocketFlow](https://github.com/The-Pocket/PocketFlow) ![](https://img.shields.io/github/stars/The-Pocket/PocketFlow?style=flat&color=yellow) - Pocket Flow: 100-line LLM framework.
- [evolver](https://github.com/EvoMap/evolver) ![](https://img.shields.io/github/stars/EvoMap/evolver?style=flat&color=yellow) - The GEP-powered self-evolving engine for AI agents.
- [adk-go](https://github.com/google/adk-go) ![](https://img.shields.io/github/stars/google/adk-go?style=flat&color=yellow) - An open-source, code-first Go toolkit for building, evaluating, and deploying sophisticate.
- [PraisonAI](https://github.com/MervinPraison/PraisonAI) ![](https://img.shields.io/github/stars/MervinPraison/PraisonAI?style=flat&color=yellow) - PraisonAI  — Hire a 24/7 AI Workforce.
- [swarms](https://github.com/kyegomez/swarms) ![](https://img.shields.io/github/stars/kyegomez/swarms?style=flat&color=yellow) - The Enterprise-Grade Production-Ready Multi-Agent Orchestration Framework.
- [openagent](https://github.com/the-open-agent/openagent) ![](https://img.shields.io/github/stars/the-open-agent/openagent?style=flat&color=yellow) - Next-generation personal AI assistant powered by LLM, RAG and agent loops.
- [AdalFlow](https://github.com/SylphAI-Inc/AdalFlow) ![](https://img.shields.io/github/stars/SylphAI-Inc/AdalFlow?style=flat&color=yellow) - AdalFlow: The library to build & auto-optimize LLM applications.
- [eve](https://github.com/vercel/eve) ![](https://img.shields.io/github/stars/vercel/eve?style=flat&color=yellow) - The Framework for Building Agents.
- [core](https://github.com/cheshire-cat-ai/core) ![](https://img.shields.io/github/stars/cheshire-cat-ai/core?style=flat&color=yellow) - AI agent microservice.
- [helixent](https://github.com/MagicCube/helixent) ![](https://img.shields.io/github/stars/MagicCube/helixent?style=flat&color=yellow) - Helixent is a small library for building ReAct-style AI agent loops based on the Bun stack.

## Observability and Eval

- [posthog](https://github.com/PostHog/posthog) ![](https://img.shields.io/github/stars/PostHog/posthog?style=flat&color=yellow) - PostHog is an all-in-one developer platform for building successful products.
- [Langfuse](https://github.com/langfuse/langfuse) ![](https://img.shields.io/github/stars/langfuse/langfuse?style=flat&color=yellow) - Open-source LLM observability, evals, prompt management and tracing.
- [mlflow](https://github.com/mlflow/mlflow) ![](https://img.shields.io/github/stars/mlflow/mlflow?style=flat&color=yellow) - The open source AI engineering platform for agents, LLMs, and ML models.
- [Promptfoo](https://github.com/promptfoo/promptfoo) ![](https://img.shields.io/github/stars/promptfoo/promptfoo?style=flat&color=yellow) - Test and red-team prompts, agents and RAG across many providers.
- [opik](https://github.com/comet-ml/opik) ![](https://img.shields.io/github/stars/comet-ml/opik?style=flat&color=yellow) - Debug, evaluate, and monitor your LLM applications, RAG systems, and agentic workflows wit.
- [openobserve](https://github.com/openobserve/openobserve) ![](https://img.shields.io/github/stars/openobserve/openobserve?style=flat&color=yellow) - Open source observability platform for logs, metrics, traces, frontend monitoring, pipelin.
- [RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) ![](https://img.shields.io/github/stars/raga-ai-hub/RagaAI-Catalyst?style=flat&color=yellow) - Python SDK for Agent AI Observability, Monitoring and Evaluation Framework.
- [phoenix](https://github.com/Arize-ai/phoenix) ![](https://img.shields.io/github/stars/Arize-ai/phoenix?style=flat&color=yellow) - AI Observability & Evaluation.
- [codeburn](https://github.com/getagentseal/codeburn) ![](https://img.shields.io/github/stars/getagentseal/codeburn?style=flat&color=yellow) - Free, local tool to track AI coding token usage and cost across 31 tools and agents (Claud.
- [evidently](https://github.com/evidentlyai/evidently) ![](https://img.shields.io/github/stars/evidentlyai/evidently?style=flat&color=yellow) - Evidently is ​​an open-source ML and LLM observability framework.
- [openllmetry](https://github.com/traceloop/openllmetry) ![](https://img.shields.io/github/stars/traceloop/openllmetry?style=flat&color=yellow) - Open-source observability for your GenAI or LLM application, based on OpenTelemetry.
- [aim](https://github.com/aimhubio/aim) ![](https://img.shields.io/github/stars/aimhubio/aim?style=flat&color=yellow) - Aim  — An easy-to-use & supercharged open-source experiment tracker.
- [Helicone](https://github.com/Helicone/helicone) ![](https://img.shields.io/github/stars/Helicone/helicone?style=flat&color=yellow) - Open-source LLM observability with monitoring, eval and experiments.
- [logfire](https://github.com/pydantic/logfire) ![](https://img.shields.io/github/stars/pydantic/logfire?style=flat&color=yellow) - AI observability platform for production LLM and agent systems.
- [agenta](https://github.com/Agenta-AI/agenta) ![](https://img.shields.io/github/stars/Agenta-AI/agenta?style=flat&color=yellow) - The open-source LLMOps platform: prompt playground, prompt management, LLM evaluation, and.
- [OpenLit](https://github.com/openlit/openlit) ![](https://img.shields.io/github/stars/openlit/openlit?style=flat&color=yellow) - OpenTelemetry-native LLM observability, GPU monitoring and guardrails.
- [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) ![](https://img.shields.io/github/stars/UKGovernmentBEIS/inspect_ai?style=flat&color=yellow) - Framework for large language model evaluations by the AI Safety Institute.
- [trench](https://github.com/FrigadeHQ/trench) ![](https://img.shields.io/github/stars/FrigadeHQ/trench?style=flat&color=yellow) - Trench — Open-Source Analytics Infrastructure.
- [ClaudeBar](https://github.com/tddworks/ClaudeBar) ![](https://img.shields.io/github/stars/tddworks/ClaudeBar?style=flat&color=yellow) - A macOS menu bar application that monitors AI coding assistant usage quotas.
- [sniffly](https://github.com/chiphuyen/sniffly) ![](https://img.shields.io/github/stars/chiphuyen/sniffly?style=flat&color=yellow) - Claude Code dashboard with usage stats, error analysis, and sharable feature.
- [prompty](https://github.com/microsoft/prompty) ![](https://img.shields.io/github/stars/microsoft/prompty?style=flat&color=yellow) - Prompty makes it easy to create, manage, debug, and evaluate LLM prompts for your AI appli.
- [langtrace](https://github.com/Scale3-Labs/langtrace) ![](https://img.shields.io/github/stars/Scale3-Labs/langtrace?style=flat&color=yellow) - Langtrace  is an open-source,  Open Telemetry based end-to-end observability tool for LLM.
- [langkit](https://github.com/whylabs/langkit) ![](https://img.shields.io/github/stars/whylabs/langkit?style=flat&color=yellow) - LangKit: An open-source toolkit for monitoring Large Language Models (LLMs).

## Docs, Research and Knowledge Work

- [gpt_academic](https://github.com/binary-husky/gpt_academic) ![](https://img.shields.io/github/stars/binary-husky/gpt_academic?style=flat&color=yellow) - Practical UI for GPT/GLM LLMs - optimized for paper reading, polishing and writing.
- [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) ![](https://img.shields.io/github/stars/Egonex-AI/Understand-Anything?style=flat&color=yellow) - Graphs that teach > graphs that impress.
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) ![](https://img.shields.io/github/stars/shareAI-lab/learn-claude-code?style=flat&color=yellow) - Bash is all you need -  A nano claude code–like 「agent harness」, built from 0 to 1.
- [TrendRadar](https://github.com/sansan0/TrendRadar) ![](https://img.shields.io/github/stars/sansan0/TrendRadar?style=flat&color=yellow) - AI-driven public opinion and trend monitor with multi-platform aggregation and alerts.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) ![](https://img.shields.io/github/stars/Fission-AI/OpenSpec?style=flat&color=yellow) - Spec-driven development (SDD) for AI coding assistants.
- [context7](https://github.com/upstash/context7) ![](https://img.shields.io/github/stars/upstash/context7?style=flat&color=yellow) - Context7 Platform -- Up-to-date code documentation for LLMs and AI code editors.
- [storm](https://github.com/stanford-oval/storm) ![](https://img.shields.io/github/stars/stanford-oval/storm?style=flat&color=yellow) - An LLM-powered knowledge curation system that researches a topic and generates a full-leng.
- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) ![](https://img.shields.io/github/stars/assafelovic/gpt-researcher?style=flat&color=yellow) - An autonomous agent that conducts deep research on any data using any LLM providers.
- [DeepTutor](https://github.com/HKUDS/DeepTutor) ![](https://img.shields.io/github/stars/HKUDS/DeepTutor?style=flat&color=yellow) - DeepTutor: Agent-native Personalized Tutoring.
- [GLM-5](https://github.com/zai-org/GLM-5) ![](https://img.shields.io/github/stars/zai-org/GLM-5?style=flat&color=yellow) - GLM-5: From Vibe Coding to Agentic Engineering.
- [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) ![](https://img.shields.io/github/stars/zarazhangrui/codebase-to-course?style=flat&color=yellow) - A Claude Code skill that turns any codebase into a beautiful, interactive single-page HTML.
- [deep-research](https://github.com/u14app/deep-research) ![](https://img.shields.io/github/stars/u14app/deep-research?style=flat&color=yellow) - Use any LLMs (Large Language Models) for Deep Research.
- [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) ![](https://img.shields.io/github/stars/Galaxy-Dawn/claude-scholar?style=flat&color=yellow) - Semi-automated research assistant for academic research and software development.
- [agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) ![](https://img.shields.io/github/stars/Leonxlnx/agentic-ai-prompt-research?style=flat&color=yellow) - Research into how agentic AI coding assistants work.
- [apple-docs-mcp](https://github.com/kimsungwhee/apple-docs-mcp) ![](https://img.shields.io/github/stars/kimsungwhee/apple-docs-mcp?style=flat&color=yellow) - MCP server for Apple Developer Documentation - Search iOS/macOS/SwiftUI/UIKit docs, WWDC v.

## Learning and Resources

- [generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners) ![](https://img.shields.io/github/stars/microsoft/generative-ai-for-beginners?style=flat&color=yellow) - Lessons to get started building with Generative AI.
- [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) ![](https://img.shields.io/github/stars/rasbt/LLMs-from-scratch?style=flat&color=yellow) - Implement a ChatGPT-like LLM in PyTorch from scratch, step by step.
- [llm-course](https://github.com/mlabonne/llm-course) ![](https://img.shields.io/github/stars/mlabonne/llm-course?style=flat&color=yellow) - Course to get into Large Language Models (LLMs) with roadmaps and Colab notebooks.
- [Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) ![](https://img.shields.io/github/stars/dair-ai/Prompt-Engineering-Guide?style=flat&color=yellow) - Guides, papers, lessons, notebooks and resources for prompt engineering, context enginee.
- [ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) ![](https://img.shields.io/github/stars/microsoft/ai-agents-for-beginners?style=flat&color=yellow) - Lessons to get started building AI agents.
- [hello-agents](https://github.com/datawhalechina/hello-agents) ![](https://img.shields.io/github/stars/datawhalechina/hello-agents?style=flat&color=yellow) - Building AI agents from scratch - principles and practice tutorial.
- [BMAD-METHOD](https://github.com/bmad-code-org/bmad-method) ![](https://img.shields.io/github/stars/bmad-code-org/bmad-method?style=flat&color=yellow) - Agentic methodology and IDE prompts for full-cycle AI product development.
- [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) ![](https://img.shields.io/github/stars/rohitg00/ai-engineering-from-scratch?style=flat&color=yellow) - Learn it.
- [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) ![](https://img.shields.io/github/stars/ashishpatel26/500-AI-Agents-Projects?style=flat&color=yellow) - The 500 AI Agents Projects is a curated collection of AI agent use cases across various in.
- [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) ![](https://img.shields.io/github/stars/e2b-dev/awesome-ai-agents?style=flat&color=yellow) - Curated list of autonomous AI agents and agent frameworks.
- [awesome-generative-ai-guide](https://github.com/aishwaryanr/awesome-generative-ai-guide) ![](https://img.shields.io/github/stars/aishwaryanr/awesome-generative-ai-guide?style=flat&color=yellow) - A one stop repository for generative AI research updates, interview resources, notebooks a.
- [Hands-On-Large-Language-Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) ![](https://img.shields.io/github/stars/HandsOnLLM/Hands-On-Large-Language-Models?style=flat&color=yellow) - Official code repo for the O'Reilly Book - "Hands-On Large Language Models".
- [vibe-coding-cn](https://github.com/2025Emma/vibe-coding-cn) ![](https://img.shields.io/github/stars/2025Emma/vibe-coding-cn?style=flat&color=yellow) - Curated list of vibe coding resources (Chinese).
- [ml-engineering](https://github.com/stas00/ml-engineering) ![](https://img.shields.io/github/stars/stas00/ml-engineering?style=flat&color=yellow) - Machine Learning Engineering Open Book.
- [Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) ![](https://img.shields.io/github/stars/BradyFU/Awesome-Multimodal-Large-Language-Models?style=flat&color=yellow) - Latest advances on Multimodal Large Language Models - surveys and benchmarks.
- [easy-vibe](https://github.com/datawhalechina/easy-vibe) ![](https://img.shields.io/github/stars/datawhalechina/easy-vibe?style=flat&color=yellow) - Vibe coding course - build apps step by step from beginner to master.
- [generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) ![](https://img.shields.io/github/stars/GoogleCloudPlatform/generative-ai?style=flat&color=yellow) - Sample code and notebooks for Generative AI on Google Cloud, with Gemini Enterprise Agent.
- [ai-guide](https://github.com/liyupi/ai-guide) ![](https://img.shields.io/github/stars/liyupi/ai-guide?style=flat&color=yellow) - AI resources hub and vibe coding tutorial - DeepSeek, GPT, Gemini, Claude and GLM guides.
- [mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners) ![](https://img.shields.io/github/stars/microsoft/mcp-for-beginners?style=flat&color=yellow) - This open-source curriculum introduces the fundamentals of Model Context Protocol (MCP) th.
- [context-engineering-intro](https://github.com/coleam00/context-engineering-intro) ![](https://img.shields.io/github/stars/coleam00/context-engineering-intro?style=flat&color=yellow) - Context engineering is the new vibe coding - it's the way to actually make AI coding assis.
- [open-llms](https://github.com/eugeneyan/open-llms) ![](https://img.shields.io/github/stars/eugeneyan/open-llms?style=flat&color=yellow) - A list of open LLMs available for commercial use.
- [awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) ![](https://img.shields.io/github/stars/steven2358/awesome-generative-ai?style=flat&color=yellow) - A curated list of modern Generative Artificial Intelligence projects and services.
- [LLMSurvey](https://github.com/RUCAIBox/LLMSurvey) ![](https://img.shields.io/github/stars/RUCAIBox/LLMSurvey?style=flat&color=yellow) - The official GitHub page for the survey paper "A Survey of Large Language Models".
- [awesome-chatgpt-zh](https://github.com/EmbraceAGI/awesome-chatgpt-zh) ![](https://img.shields.io/github/stars/EmbraceAGI/awesome-chatgpt-zh?style=flat&color=yellow) - ChatGPT 中文指南，ChatGPT 中文调教指南，指令指南，应用开发指南，精选资源清单，更好的使用 chatGPT 让你的生产力 up up up!.
- [llm-engineer-toolkit](https://github.com/KalyanKS-NLP/llm-engineer-toolkit) ![](https://img.shields.io/github/stars/KalyanKS-NLP/llm-engineer-toolkit?style=flat&color=yellow) - A curated list of  120+ LLM libraries category wise.
- [LLMsPracticalGuide](https://github.com/Mooler0410/LLMsPracticalGuide) ![](https://img.shields.io/github/stars/Mooler0410/LLMsPracticalGuide?style=flat&color=yellow) - A curated list of practical guide resources of LLMs (LLMs Tree, Examples, Papers).
- [anomaly-detection-resources](https://github.com/yzhao062/anomaly-detection-resources) ![](https://img.shields.io/github/stars/yzhao062/anomaly-detection-resources?style=flat&color=yellow) - Anomaly detection related books, papers, videos, and toolboxes.
- [awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) ![](https://img.shields.io/github/stars/WangRongsheng/awesome-LLM-resources?style=flat&color=yellow) - Summary of the world's best LLM resources - agents, coding, MCP, multimodal.
- [learn-ai-engineering](https://github.com/ashishps1/learn-ai-engineering) ![](https://img.shields.io/github/stars/ashishps1/learn-ai-engineering?style=flat&color=yellow) - Learn AI and LLMs from scratch using free resources.
- [vibe-vibe](https://github.com/datawhalechina/vibe-vibe) ![](https://img.shields.io/github/stars/datawhalechina/vibe-vibe?style=flat&color=yellow) - AI for All: The First Systematic Vibe Coding Tutorial | From Zero to Full-Stack, Bring You.
- [awesome-ai-tools](https://github.com/mahseema/awesome-ai-tools) ![](https://img.shields.io/github/stars/mahseema/awesome-ai-tools?style=flat&color=yellow) - A curated list of Artificial Intelligence Top Tools.
- [awesome-vibe-coding](https://github.com/filipecalegario/awesome-vibe-coding) ![](https://img.shields.io/github/stars/filipecalegario/awesome-vibe-coding?style=flat&color=yellow) - A curated list of vibe coding references, collaborating with AI to write code.
- [vibe-coding](https://github.com/EnzeD/vibe-coding) ![](https://img.shields.io/github/stars/EnzeD/vibe-coding?style=flat&color=yellow) - Vibe coding resources and practices collection.
- [aicodeguide](https://github.com/automata/aicodeguide) ![](https://img.shields.io/github/stars/automata/aicodeguide?style=flat&color=yellow) - AI Code Guide is a roadmap to start coding with AI.
- [awesome-ai-coding-tools](https://github.com/ai-for-developers/awesome-ai-coding-tools) ![](https://img.shields.io/github/stars/ai-for-developers/awesome-ai-coding-tools?style=flat&color=yellow) - A curated list of AI-powered coding tools.

## AI Infra and Model Platforms

- [ollama](https://github.com/ollama/ollama) ![](https://img.shields.io/github/stars/ollama/ollama?style=flat&color=yellow) - Get up and running with Kimi-K2.6, GLM-5.1, MiniMax, DeepSeek, gpt-oss, Qwen, Gemma and ot.
- [transformers](https://github.com/huggingface/transformers) ![](https://img.shields.io/github/stars/huggingface/transformers?style=flat&color=yellow) - Transformers: the model-definition framework for state-of-the-art machine learning model.
- [open-webui](https://github.com/open-webui/open-webui) ![](https://img.shields.io/github/stars/open-webui/open-webui?style=flat&color=yellow) - User-friendly AI Interface (Supports Ollama, OpenAI API, ...).
- [vllm](https://github.com/vllm-project/vllm) ![](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&color=yellow) - A high-throughput and memory-efficient inference and serving engine for LLMs.
- [LlamaFactory](https://github.com/hiyouga/LlamaFactory) ![](https://img.shields.io/github/stars/hiyouga/LlamaFactory?style=flat&color=yellow) - Unified Efficient Fine-Tuning of 100+ LLMs & VLMs (ACL 2024).
- [unsloth](https://github.com/unslothai/unsloth) ![](https://img.shields.io/github/stars/unslothai/unsloth?style=flat&color=yellow) - Unsloth Studio is a web UI for training and running open models like Gemma 4, Qwen3.6, Dee.
- [anything-llm](https://github.com/Mintplex-Labs/anything-llm) ![](https://img.shields.io/github/stars/Mintplex-Labs/anything-llm?style=flat&color=yellow) - Stop renting your intelligence.
- [llm-app](https://github.com/pathwaycom/llm-app) ![](https://img.shields.io/github/stars/pathwaycom/llm-app?style=flat&color=yellow) - Ready-to-run cloud templates for RAG, AI pipelines, and enterprise search with live data.
- [litellm](https://github.com/BerriAI/litellm) ![](https://img.shields.io/github/stars/BerriAI/litellm?style=flat&color=yellow) - Python SDK, Proxy Server (AI Gateway) to call 100+ LLM APIs in OpenAI (or native) format,.
- [LocalAI](https://github.com/mudler/LocalAI) ![](https://img.shields.io/github/stars/mudler/LocalAI?style=flat&color=yellow) - LocalAI is the open-source AI engine.
- [milvus](https://github.com/milvus-io/milvus) ![](https://img.shields.io/github/stars/milvus-io/milvus?style=flat&color=yellow) - Milvus is a high-performance, cloud-native vector database built for scalable vector ANN s.
- [jan](https://github.com/janhq/jan) ![](https://img.shields.io/github/stars/janhq/jan?style=flat&color=yellow) - Jan is an open source alternative to ChatGPT that runs 100% offline on your computer.
- [ray](https://github.com/ray-project/ray) ![](https://img.shields.io/github/stars/ray-project/ray?style=flat&color=yellow) - Ray is an AI compute engine.
- [quivr](https://github.com/QuivrHQ/quivr) ![](https://img.shields.io/github/stars/QuivrHQ/quivr?style=flat&color=yellow) - Opiniated RAG for integrating GenAI in your apps    Focus on your product rather than the.
- [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ![](https://img.shields.io/github/stars/chatchat-space/Langchain-Chatchat?style=flat&color=yellow) - Langchain-Chatchat（原Langchain-ChatGLM）基于 Langchain 与 ChatGLM, Qwen 与 Llama 等语言模型的 RAG 与 Ag.
- [langextract](https://github.com/google/langextract) ![](https://img.shields.io/github/stars/google/langextract?style=flat&color=yellow) - A Python library for extracting structured information from unstructured text using LLMs w.
- [Qwen](https://github.com/QwenLM/Qwen) ![](https://img.shields.io/github/stars/QwenLM/Qwen?style=flat&color=yellow) - The official repo of Qwen (通义千问) chat & pretrained large language model proposed by Alibab.
- [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) ![](https://img.shields.io/github/stars/ymcui/Chinese-LLaMA-Alpaca?style=flat&color=yellow) - Chinese LLaMA and Alpaca LLMs with local CPU/GPU training and deployment.
- [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) ![](https://img.shields.io/github/stars/NVIDIA/Megatron-LM?style=flat&color=yellow) - Ongoing research training transformer models at scale.
- [ChatGLM2-6B](https://github.com/zai-org/ChatGLM2-6B) ![](https://img.shields.io/github/stars/zai-org/ChatGLM2-6B?style=flat&color=yellow) - ChatGLM2-6B: An Open Bilingual Chat LLM | 开源双语对话语言模型.
- [ggml](https://github.com/ggml-org/ggml) ![](https://img.shields.io/github/stars/ggml-org/ggml?style=flat&color=yellow) - Tensor library for machine learning.
- [DeepLearningExamples](https://github.com/NVIDIA/DeepLearningExamples) ![](https://img.shields.io/github/stars/NVIDIA/DeepLearningExamples?style=flat&color=yellow) - State-of-the-Art Deep Learning scripts organized by models - easy to train and deploy with.
- [outlines](https://github.com/dottxt-ai/outlines) ![](https://img.shields.io/github/stars/dottxt-ai/outlines?style=flat&color=yellow) - Structured Outputs.
- [litgpt](https://github.com/Lightning-AI/litgpt) ![](https://img.shields.io/github/stars/Lightning-AI/litgpt?style=flat&color=yellow) - Provides 20+ high-performance LLMs with recipes to pretrain, finetune and deploy at scale.
- [txtai](https://github.com/neuml/txtai) ![](https://img.shields.io/github/stars/neuml/txtai?style=flat&color=yellow) - All-in-one AI framework for semantic search, LLM orchestration and language model workfl.
- [HRM](https://github.com/sapientinc/HRM) ![](https://img.shields.io/github/stars/sapientinc/HRM?style=flat&color=yellow) - Hierarchical Reasoning Model Official Release.
- [MOSS](https://github.com/OpenMOSS/MOSS) ![](https://img.shields.io/github/stars/OpenMOSS/MOSS?style=flat&color=yellow) - An open-source tool-augmented conversational language model from Fudan University.
- [promptflow](https://github.com/microsoft/promptflow) ![](https://img.shields.io/github/stars/microsoft/promptflow?style=flat&color=yellow) - Build high-quality LLM apps - from prototyping, testing to production deployment and monit.
- [petals](https://github.com/bigscience-workshop/petals) ![](https://img.shields.io/github/stars/bigscience-workshop/petals?style=flat&color=yellow) - Run LLMs at home, BitTorrent-style.
- [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) ![](https://img.shields.io/github/stars/OpenRLHF/OpenRLHF?style=flat&color=yellow) - An Easy-to-use, Scalable and High-performance Agentic RL Framework based on Ray (PPO & DAP.
- [PowerInfer](https://github.com/Tiiny-AI/PowerInfer) ![](https://img.shields.io/github/stars/Tiiny-AI/PowerInfer?style=flat&color=yellow) - High-speed Large Language Model Serving for Local Deployment.
- [deeplake](https://github.com/activeloopai/deeplake) ![](https://img.shields.io/github/stars/activeloopai/deeplake?style=flat&color=yellow) - Deeplake is AI Data Runtime for Agents.
- [optimate](https://github.com/nebuly-ai/optimate) ![](https://img.shields.io/github/stars/nebuly-ai/optimate?style=flat&color=yellow) - A collection of libraries to optimise AI model performances.
- [unstract](https://github.com/Zipstack/unstract) ![](https://img.shields.io/github/stars/Zipstack/unstract?style=flat&color=yellow) - LLM-Driven Extraction of Unstructured Data — Built for API Deployments & ETL Pipeline Work.
- [osaurus](https://github.com/osaurus-ai/osaurus) ![](https://img.shields.io/github/stars/osaurus-ai/osaurus?style=flat&color=yellow) - Own your AI.
- [plano](https://github.com/katanemo/plano) ![](https://img.shields.io/github/stars/katanemo/plano?style=flat&color=yellow) - Plano is an AI-native proxy and data plane for agentic apps — with built-in orchestration,.
- [bifrost](https://github.com/maximhq/bifrost) ![](https://img.shields.io/github/stars/maximhq/bifrost?style=flat&color=yellow) - Fastest enterprise AI gateway (50x faster than LiteLLM) with adaptive load balancer, clust.
- [lemonade](https://github.com/lemonade-sdk/lemonade) ![](https://img.shields.io/github/stars/lemonade-sdk/lemonade?style=flat&color=yellow) - Lemonade helps users discover and run local AI apps by serving optimized LLMs right from t.

## Domain-Specific Agents

- [TradingAgents](https://github.com/TauricResearch/TradingAgents) ![](https://img.shields.io/github/stars/TauricResearch/TradingAgents?style=flat&color=yellow) - TradingAgents: Multi-Agents LLM Financial Trading Framework.
- [daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) ![](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=flat&color=yellow) - LLM 驱动的多市场股票智能分析系统：多源行情、实时新闻、决策看板与自动推送，支持零成本定时运行。  LLM-powered multi-market stock analysis.
- [LibreChat](https://github.com/danny-avila/LibreChat) ![](https://img.shields.io/github/stars/danny-avila/LibreChat?style=flat&color=yellow) - Enhanced ChatGPT Clone: Features Agents, MCP, Skills, DeepSeek, Anthropic, AWS, OpenAI, Re.
- [OpenMontage](https://github.com/calesthio/OpenMontage) ![](https://img.shields.io/github/stars/calesthio/OpenMontage?style=flat&color=yellow) - World's first open-source, agentic video production system.
- [FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) ![](https://img.shields.io/github/stars/Fincept-Corporation/FinceptTerminal?style=flat&color=yellow) - FinceptTerminal is a modern finance application offering advanced market analytics, invest.
- [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) ![](https://img.shields.io/github/stars/AI4Finance-Foundation/FinGPT?style=flat&color=yellow) - FinGPT: Open-Source Financial Large Language Models!  Revolutionize     We release the tr.
- [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) ![](https://img.shields.io/github/stars/stefan-jansen/machine-learning-for-trading?style=flat&color=yellow) - Code for Machine Learning for Trading, 3rd edition — from data sourcing to live execution.
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) ![](https://img.shields.io/github/stars/xpzouying/xiaohongshu-mcp?style=flat&color=yellow) - MCP for xiaohongshu.com.
- [ai-berkshire](https://github.com/xbtlin/ai-berkshire) ![](https://img.shields.io/github/stars/xbtlin/ai-berkshire?style=flat&color=yellow) - AI 时代的伯克希尔：基于 Claude Code / Codex 的价值投资研究框架。巴菲特·芒格·段永平·李录四大师方法论 + 多Agent并行研究。| AI-era Berk.
- [QuantDinger](https://github.com/brokermr810/QuantDinger) ![](https://img.shields.io/github/stars/brokermr810/QuantDinger?style=flat&color=yellow) - AI quantitative trading platform for crypto, stocks, and forex with backtesting, live trad.
- [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) ![](https://img.shields.io/github/stars/AI4Finance-Foundation/FinRobot?style=flat&color=yellow) - FinRobot: An Open-Source AI Agent Platform for Financial Analysis using LLMs.
- [claude-ads](https://github.com/AgriciDaniel/claude-ads) ![](https://img.shields.io/github/stars/AgriciDaniel/claude-ads?style=flat&color=yellow) - Comprehensive paid advertising audit & optimization skill for Claude Code.
- [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit) ![](https://img.shields.io/github/stars/JerBouma/FinanceToolkit?style=flat&color=yellow) - Transparent and Efficient Financial Analysis.
- [arc-kit](https://github.com/tractorjuice/arc-kit) ![](https://img.shields.io/github/stars/tractorjuice/arc-kit?style=flat&color=yellow) - The Enterprise Architecture Governance Harness — strategy, architecture, delivery, and ass.
- [aso-skills](https://github.com/Eronred/aso-skills) ![](https://img.shields.io/github/stars/Eronred/aso-skills?style=flat&color=yellow) - AI agent skills for App Store Optimization (ASO) and app marketing.
- [ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) ![](https://img.shields.io/github/stars/zubair-trabzada/ai-legal-claude?style=flat&color=yellow) - AI Legal Assistant skill for Claude Code.
- [mathcode](https://github.com/math-ai-org/mathcode) ![](https://img.shields.io/github/stars/math-ai-org/mathcode?style=flat&color=yellow) - MathCode: A Frontier Mathematical Coding Agent.

## Needs Review

- [ChatTTS](https://github.com/2noise/ChatTTS) ![](https://img.shields.io/github/stars/2noise/ChatTTS?style=flat&color=yellow) - A generative speech model for daily dialogue.
- [gemini-voyager](https://github.com/Nagi-ovo/gemini-voyager) ![](https://img.shields.io/github/stars/Nagi-ovo/gemini-voyager?style=flat&color=yellow) - An all-in-one enhancement suite for Google Gemini & AI Studio - timeline navigation, folde.
- [FunASR](https://github.com/modelscope/FunASR) ![](https://img.shields.io/github/stars/modelscope/FunASR?style=flat&color=yellow) - Industrial-grade speech recognition toolkit: 170x realtime, 50+ languages, speaker diariza.
- [nuclear](https://github.com/nukeop/nuclear) ![](https://img.shields.io/github/stars/nukeop/nuclear?style=flat&color=yellow) - Streaming music player that finds free music for you.
- [CVPR2024-Paper-Code-Interpretation](https://github.com/extreme-assistant/CVPR2024-Paper-Code-Interpretation) ![](https://img.shields.io/github/stars/extreme-assistant/CVPR2024-Paper-Code-Interpretation?style=flat&color=yellow) - CVPR papers collection with code and interpretations.
- [XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader) ![](https://img.shields.io/github/stars/JoeanAmier/XHS-Downloader?style=flat&color=yellow) - XiaoHongShu (RedNote) link extractor and content downloader.
- [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) ![](https://img.shields.io/github/stars/xinnan-tech/xiaozhi-esp32-server?style=flat&color=yellow) - Backend service for xiaozhi-esp32 - build an ESP32 device control server.
- [VAR](https://github.com/FoundationVision/VAR) ![](https://img.shields.io/github/stars/FoundationVision/VAR?style=flat&color=yellow) - Visual Autoregressive Modeling - next-scale prediction for image generation.
- [ICCV2023-Paper-Code-Interpretation](https://github.com/extreme-assistant/ICCV2023-Paper-Code-Interpretation) ![](https://img.shields.io/github/stars/extreme-assistant/ICCV2023-Paper-Code-Interpretation?style=flat&color=yellow) - ICCV2021/2019/2017 论文/代码/解读/直播合集，极市团队整理.
- [deepseek_ocr_app](https://github.com/rdumasia303/deepseek_ocr_app) ![](https://img.shields.io/github/stars/rdumasia303/deepseek_ocr_app?style=flat&color=yellow) - A quick vibe coded app for deepseek OCR.
- [natively-cluely-ai-assistant](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant) ![](https://img.shields.io/github/stars/Natively-AI-assistant/natively-cluely-ai-assistant?style=flat&color=yellow) - Natively — Free open-source AI meeting assistant, interview copilot, and note taker.
- [global-stock-data](https://github.com/simonlin1212/global-stock-data) ![](https://img.shields.io/github/stars/simonlin1212/global-stock-data?style=flat&color=yellow) - US & HK Stock Full-Stack Data Toolkit for AI Coding Assistants.

## Contributing

Found a great tool or built one? Add it via a Pull Request — see CONTRIBUTING.md for the rules (one tool per PR, live repo, neutral description). Star counts are refreshed daily by a GitHub Action. Licensed under CC0-1.0.
