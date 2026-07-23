# Awesome Vibe Coding Tools [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Кураторский список инструментов для **вайбкодеров** — разработчиков, которые пишут код с AI-ассистентами (Claude Code, Cursor, Copilot и компания). Число звёзд обновляется автоматически раз в сутки. **[Открыть сайт с поиском →](https://axisrow.github.io/vibetools/)** · Создано на GLM-5.2.

Список должен быть **кураторским, а не коллекционным**: каждая запись отобрана вручную, репозиторий жив, и инструмент относится к AI-разработке. Как добавить утилиту — см. CONTRIBUTING.md. English version: README.md.

## Содержание

- [AI-агенты кодинга и CLI](#ai-агенты-кодинга-и-cli)
- [Облачные coding-агенты](#облачные-coding-агенты)
- [Интеграции в редакторы](#интеграции-в-редакторы)
- [Ревью, тестирование и качество кода](#ревью-тестирование-и-качество-кода)
- [DevOps и облачная автоматизация](#devops-и-облачная-автоматизация)
- [Security и pentest-агенты](#security-и-pentest-агенты)
- [Браузерная и web-автоматизация](#браузерная-и-web-автоматизация)
- [Design-to-code и фронтенд](#design-to-code-и-фронтенд)
- [App builders и low-code](#app-builders-и-low-code)
- [Разработка игр](#разработка-игр)
- [Контекст, память и индексирование кода](#контекст-память-и-индексирование-кода)
- [MCP-серверы и клиенты](#mcp-серверы-и-клиенты)
- [Skills, промпты и правила агентов](#skills-промпты-и-правила-агентов)
- [AI-ассистенты](#ai-ассистенты)
- [Наблюдаемость и eval](#наблюдаемость-и-eval)
- [Документация, research и knowledge work](#документация-research-и-knowledge-work)
- [Обучение и ресурсы](#обучение-и-ресурсы)
- [AI-инфра и модельные платформы](#ai-инфра-и-модельные-платформы)
- [Доменные AI-агенты](#доменные-ai-агенты)
- [Требует ревью](#требует-ревью)

## AI-агенты кодинга и CLI

- [OpenCode](https://github.com/sst/opencode) ![](https://img.shields.io/github/stars/sst/opencode?style=flat&color=yellow) - Open-source AI-агент для терминала с поддержкой любых провайдеров моделей.
- [Claude Code](https://github.com/anthropics/claude-code) ![](https://img.shields.io/github/stars/anthropics/claude-code?style=flat&color=yellow) - Агент-кодер от Anthropic, живёт в терминале и понимает вашу кодовую базу.
- [cc-switch](https://github.com/farion1231/cc-switch) ![](https://img.shields.io/github/stars/farion1231/cc-switch?style=flat&color=yellow) - Кроссплатформенный desktop All-in-One для Claude Code, Codex, OpenCode.
- [gemini-cli](https://github.com/google-gemini/gemini-cli) ![](https://img.shields.io/github/stars/google-gemini/gemini-cli?style=flat&color=yellow) - Open-source AI-агент: brings Gemini прямо в терминал.
- [pi](https://github.com/earendil-works/pi) ![](https://img.shields.io/github/stars/earendil-works/pi?style=flat&color=yellow) - AI-агент тулкит: единый LLM API, agent loop, TUI, CLI кодинг-агент.
- [rtk](https://github.com/rtk-ai/rtk) ![](https://img.shields.io/github/stars/rtk-ai/rtk?style=flat&color=yellow) - CLI-прокси: снижает потребление токенов LLM на 60–90% в dev-командах.
- [Goose](https://github.com/block/goose) ![](https://img.shields.io/github/stars/block/goose?style=flat&color=yellow) - Открытый расширяемый AI-агент: умеет устанавливать, запускать, править и тестировать код.
- [goose](https://github.com/aaif-goose/goose) ![](https://img.shields.io/github/stars/aaif-goose/goose?style=flat&color=yellow) - An open source, extensible AI agent that goes beyond code suggestions - install, execute, edit, and test with any LLM.
- [Aider](https://github.com/Aider-AI/aider) ![](https://img.shields.io/github/stars/Aider-AI/aider?style=flat&color=yellow) - AI-парное программирование в терминале, правит код в любом git-репозитории.
- [nanobot](https://github.com/HKUDS/nanobot) ![](https://img.shields.io/github/stars/HKUDS/nanobot?style=flat&color=yellow) - Легковесный open-source AI-агент для инструментов, чатов и воркфлоу.
- [CowAgent](https://github.com/zhayujie/CowAgent) ![](https://img.shields.io/github/stars/zhayujie/CowAgent?style=flat&color=yellow) - Open-source супер-AI-ассистент и agent-харнес.
- [CodeWhale](https://github.com/Hmbown/CodeWhale) ![](https://img.shields.io/github/stars/Hmbown/CodeWhale?style=flat&color=yellow) - Open-source community-driven agent-харнес.
- [DeepSeek-Reasonix](https://github.com/esengine/DeepSeek-Reasonix) ![](https://img.shields.io/github/stars/esengine/DeepSeek-Reasonix?style=flat&color=yellow) - DeepSeek-native AI-агент кодинга для терминала.
- [vibe-kanban](https://github.com/BloopAI/vibe-kanban) ![](https://img.shields.io/github/stars/BloopAI/vibe-kanban?style=flat&color=yellow) - Получите в 10 раз больше от Claude Code, Codex и любого кодинг-агента.
- [agenticSeek](https://github.com/Fosowl/agenticSeek) ![](https://img.shields.io/github/stars/Fosowl/agenticSeek?style=flat&color=yellow) - Полностью локальный аналог Manus AI.
- [qwen-code](https://github.com/QwenLM/qwen-code) ![](https://img.shields.io/github/stars/QwenLM/qwen-code?style=flat&color=yellow) - Open-source AI-агент кодинга в терминале.
- [cmux](https://github.com/manaflow-ai/cmux) ![](https://img.shields.io/github/stars/manaflow-ai/cmux?style=flat&color=yellow) - Open-source терминал macOS на Ghostty с вкладками для AI-кодинга.
- [oh-my-pi](https://github.com/can1357/oh-my-pi) ![](https://img.shields.io/github/stars/can1357/oh-my-pi?style=flat&color=yellow) - AI Coding agent for the terminal — hash-anchored edits, optimized tool harness, LSP, Python, browser, subagents, and more.
- [plandex](https://github.com/plandex-ai/plandex) ![](https://img.shields.io/github/stars/plandex-ai/plandex?style=flat&color=yellow) - Open-source AI-агент кодинга.
- [cc-connect](https://github.com/chenhg5/cc-connect) ![](https://img.shields.io/github/stars/chenhg5/cc-connect?style=flat&color=yellow) - Мост от локальных AI-агентов (Claude Code, Cursor) к мессенджерам.
- [superset](https://github.com/superset-sh/superset) ![](https://img.shields.io/github/stars/superset-sh/superset?style=flat&color=yellow) - Редактор кода эпохи AI-агентов — армия Claude Code, Codex и др.
- [llm](https://github.com/simonw/llm) ![](https://img.shields.io/github/stars/simonw/llm?style=flat&color=yellow) - Доступ к большим языковым моделям из командной строки и пайплайнов.
- [claude-squad](https://github.com/smtg-ai/claude-squad) ![](https://img.shields.io/github/stars/smtg-ai/claude-squad?style=flat&color=yellow) - Управление несколькими AI-терминал-агентами (Claude Code, Codex, OpenCode).
- [Kaku](https://github.com/tw93/Kaku) ![](https://img.shields.io/github/stars/tw93/Kaku?style=flat&color=yellow) - Быстрый готовый терминал для AI-кодинга.
- [hapi](https://github.com/tiann/hapi) ![](https://img.shields.io/github/stars/tiann/hapi?style=flat&color=yellow) - Апп для Claude Code/Codex/Gemini/OpenCode — vibe coding где угодно.
- [cc-switch-cli](https://github.com/SaladDay/cc-switch-cli) ![](https://img.shields.io/github/stars/SaladDay/cc-switch-cli?style=flat&color=yellow) - CLI-версия cc-switch.
- [agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) ![](https://img.shields.io/github/stars/agent-of-empires/agent-of-empires?style=flat&color=yellow) - Управление несколькими Claude Code/OpenCode агентами из TUI или Web.
- [zclaw](https://github.com/tnm/zclaw) ![](https://img.shields.io/github/stars/tnm/zclaw?style=flat&color=yellow) - Личный AI-ассистент на 888 KiB (~35 КБ кода).
- [Cougar-CLI](https://github.com/dulikaifazr/Cougar-CLI) ![](https://img.shields.io/github/stars/dulikaifazr/Cougar-CLI?style=flat&color=yellow) - AI-программирующий агент для командной строки.
- [clawcodex](https://github.com/agentforce314/clawcodex) ![](https://img.shields.io/github/stars/agentforce314/clawcodex?style=flat&color=yellow) - Эффективный по токенам полный Python-ребилд Claude Code.
- [mycoder](https://github.com/bhouston/mycoder) ![](https://img.shields.io/github/stars/bhouston/mycoder?style=flat&color=yellow) - Простой в установке мощный консольный AI-агент для кодинга.

## Облачные coding-агенты

- [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands) ![](https://img.shields.io/github/stars/OpenHands/OpenHands?style=flat&color=yellow) - OpenHands — разработка на базе AI.
- [OpenHands](https://github.com/All-Hands-AI/OpenHands) ![](https://img.shields.io/github/stars/All-Hands-AI/OpenHands?style=flat&color=yellow) - Автономный агент-кодер — самохостинговая инженерная команда, работающая 24/7.
- [daytona](https://github.com/daytonaio/daytona) ![](https://img.shields.io/github/stars/daytonaio/daytona?style=flat&color=yellow) - Безопасная эластичная инфраструктура для AI-сгенерированного кода.
- [Bolt.new](https://github.com/stackblitz/bolt.new) ![](https://img.shields.io/github/stars/stackblitz/bolt.new?style=flat&color=yellow) - Создание, запуск, правка и деплой full-stack веб-приложений из браузера.
- [InsForge](https://github.com/InsForge/InsForge) ![](https://img.shields.io/github/stars/InsForge/InsForge?style=flat&color=yellow) - Open-source бэкенд-платформа для агентного кодинга.
- [humanlayer](https://github.com/humanlayer/humanlayer) ![](https://img.shields.io/github/stars/humanlayer/humanlayer?style=flat&color=yellow) - Помогает AI-агентам решать сложные задачи в больших кодовых базах.
- [vibesdk](https://github.com/cloudflare/vibesdk) ![](https://img.shields.io/github/stars/cloudflare/vibesdk?style=flat&color=yellow) - Open-source платформа vibe coding для построения своего vibe-кодинг-инструмента.
- [costrict](https://github.com/zgsm-ai/costrict) ![](https://img.shields.io/github/stars/zgsm-ai/costrict?style=flat&color=yellow) - Строгий AI-кодер для предприятий: качество прежде всего.
- [MonkeyCode](https://github.com/chaitin/MonkeyCode) ![](https://img.shields.io/github/stars/chaitin/MonkeyCode?style=flat&color=yellow) - AI-платформа кодинга для команд.
- [crystal](https://github.com/stravu/crystal) ![](https://img.shields.io/github/stars/stravu/crystal?style=flat&color=yellow) - (Crystal is now Nimbalyst) Run multiple Codex and Claude Code AI sessions in parallel git worktrees. Test, compare approaches & manage AI-assisted development workflows in one desktop app.
- [fulling](https://github.com/FullAgent/fulling) ![](https://img.shields.io/github/stars/FullAgent/fulling?style=flat&color=yellow) - Fulling — AI-powered full-stack инженер-агент.
- [vibekit](https://github.com/superagent-ai/vibekit) ![](https://img.shields.io/github/stars/superagent-ai/vibekit?style=flat&color=yellow) - Запуск Claude Code, Gemini, Codex и любого агента в чистой изолированной песочнице.
- [claudebox](https://github.com/RchGrav/claudebox) ![](https://img.shields.io/github/stars/RchGrav/claudebox?style=flat&color=yellow) - Docker-среда разработки для Claude Code.

## Интеграции в редакторы

- [Cline](https://github.com/cline/cline) ![](https://img.shields.io/github/stars/cline/cline?style=flat&color=yellow) - Автономный агент-кодер в виде расширения для VS Code.
- [Continue](https://github.com/continuedev/continue) ![](https://img.shields.io/github/stars/continuedev/continue?style=flat&color=yellow) - Открытый AI-ассистент для кода в VS Code и JetBrains.
- [tabby](https://github.com/TabbyML/tabby) ![](https://img.shields.io/github/stars/TabbyML/tabby?style=flat&color=yellow) - Self-hosted AI-ассистент кодинга.
- [AionUi](https://github.com/iOfficeAI/AionUi) ![](https://img.shields.io/github/stars/iOfficeAI/AionUi?style=flat&color=yellow) - Free локальный 24/7 Cowork-апп для Claude Code, Codex, OpenCode.
- [Roo Code](https://github.com/RooCodeInc/Roo-Code) ![](https://img.shields.io/github/stars/RooCodeInc/Roo-Code?style=flat&color=yellow) - AI-агент-кодер для VS Code с кастомными режимами и контролем инструментов.
- [avante.nvim](https://github.com/yetone/avante.nvim) ![](https://img.shields.io/github/stars/yetone/avante.nvim?style=flat&color=yellow) - AI-кодинг в духе Cursor прямо внутри Neovim.
- [sweep](https://github.com/sweepai/sweep) ![](https://img.shields.io/github/stars/sweepai/sweep?style=flat&color=yellow) - AI-ассистент кодинга для JetBrains.
- [CopilotForXcode](https://github.com/github/CopilotForXcode) ![](https://img.shields.io/github/stars/github/CopilotForXcode?style=flat&color=yellow) - AI-ассистент кодинга для Xcode.
- [sketch](https://github.com/approximatelabs/sketch) ![](https://img.shields.io/github/stars/approximatelabs/sketch?style=flat&color=yellow) - AI-ассистент написания кода, понимающий содержимое данных.
- [deepseek-engineer](https://github.com/Doriandarko/deepseek-engineer) ![](https://img.shields.io/github/stars/Doriandarko/deepseek-engineer?style=flat&color=yellow) - Мощный кодинг-ассистент на базе DeepSeek API.
- [claude-code.nvim](https://github.com/greggh/claude-code.nvim) ![](https://img.shields.io/github/stars/greggh/claude-code.nvim?style=flat&color=yellow) - Бесшовная интеграция Claude Code с Neovim.
- [codemcp](https://github.com/ezyang/codemcp) ![](https://img.shields.io/github/stars/ezyang/codemcp?style=flat&color=yellow) - Кодинг-ассистент MCP для Claude Desktop.
- [codefuse-chatbot](https://github.com/codefuse-ai/codefuse-chatbot) ![](https://img.shields.io/github/stars/codefuse-ai/codefuse-chatbot?style=flat&color=yellow) - Умный ассистент жизненного цикла разработки на MaaS.
- [vim-ai](https://github.com/madox2/vim-ai) ![](https://img.shields.io/github/stars/madox2/vim-ai?style=flat&color=yellow) - AI-ассистент кода для Vim.

## Ревью, тестирование и качество кода

- [Claude Code Action](https://github.com/anthropics/claude-code-action) ![](https://img.shields.io/github/stars/anthropics/claude-code-action?style=flat&color=yellow) - GitHub Action: Claude ревьюит PR и фикcит issues прямо в CI.
- [XcodeBuildMCP](https://github.com/getsentry/XcodeBuildMCP) ![](https://img.shields.io/github/stars/getsentry/XcodeBuildMCP?style=flat&color=yellow) - MCP-сервер и CLI для работы с Xcode-проектами агентами.
- [APIAuto](https://github.com/TommyLemon/APIAuto) ![](https://img.shields.io/github/stars/TommyLemon/APIAuto?style=flat&color=yellow) - 敏捷开发最强大易用的接口工具，机器学习零代码测试与 AI 问答、生成代码与静态检查、生成文档与光标悬浮注释，腾讯、华为、SHEIN、传音、工行等使用 The most advanced tool for HTTP API. Machine learning no-code testing and AI assistant, generating codes and static analysis, generating comments and floating hints. Used by Tencent, Huawei, SHEIN, TRANSSION, ICBC, etc.
- [rockpack](https://github.com/AlexSergey/rockpack) ![](https://img.shields.io/github/stars/AlexSergey/rockpack?style=flat&color=yellow) - Zero-config React со встроенным SSR и AI-ready структурой проекта.
- [claude-debugs-for-you](https://github.com/jasonjmcghee/claude-debugs-for-you) ![](https://img.shields.io/github/stars/jasonjmcghee/claude-debugs-for-you?style=flat&color=yellow) - Включает любой LLM в отладчик.

## DevOps и облачная автоматизация

- [kestra](https://github.com/kestra-io/kestra) ![](https://img.shields.io/github/stars/kestra-io/kestra?style=flat&color=yellow) - Event-driven платформа оркестрации и планирования для критичных приложений.
- [trigger.dev](https://github.com/triggerdotdev/trigger.dev) ![](https://img.shields.io/github/stars/triggerdotdev/trigger.dev?style=flat&color=yellow) - Trigger.dev — сборка и деплой managed AI-агентов и воркфлоу.
- [infracost](https://github.com/infracost/infracost) ![](https://img.shields.io/github/stars/infracost/infracost?style=flat&color=yellow) - Аналитика облачных затрат для инженеров, AI-агентов и CI/CD.
- [nginx-ui](https://github.com/0xJacky/nginx-ui) ![](https://img.shields.io/github/stars/0xJacky/nginx-ui?style=flat&color=yellow) - Ещё один WebUI для Nginx.
- [mcp](https://github.com/awslabs/mcp) ![](https://img.shields.io/github/stars/awslabs/mcp?style=flat&color=yellow) - Open-source MCP-серверы для AWS.
- [Chaterm](https://github.com/chaterm/Chaterm) ![](https://img.shields.io/github/stars/chaterm/Chaterm?style=flat&color=yellow) - Open-source AI-терминал управления облаком и инфраструктурой.
- [kubernetes-mcp-server](https://github.com/containers/kubernetes-mcp-server) ![](https://img.shields.io/github/stars/containers/kubernetes-mcp-server?style=flat&color=yellow) - MCP-сервер для Kubernetes и OpenShift.

## Security и pentest-агенты

- [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) ![](https://img.shields.io/github/stars/CloakHQ/CloakBrowser?style=flat&color=yellow) - Стелс-Chromium, проходящий любые проверки на ботов.
- [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) ![](https://img.shields.io/github/stars/mukul975/Anthropic-Cybersecurity-Skills?style=flat&color=yellow) - Навыки кибербезопасности Anthropic.
- [PentestGPT](https://github.com/GreyDGL/PentestGPT) ![](https://img.shields.io/github/stars/GreyDGL/PentestGPT?style=flat&color=yellow) - Агентный фреймворк автоматического пентеста на базе LLM.
- [ida-pro-mcp](https://github.com/mrexodia/ida-pro-mcp) ![](https://img.shields.io/github/stars/mrexodia/ida-pro-mcp?style=flat&color=yellow) - AI-ассистент реверс-инжиниринга: мост IDA Pro и языковых моделей.
- [hexstrike-ai](https://github.com/0x4m4/hexstrike-ai) ![](https://img.shields.io/github/stars/0x4m4/hexstrike-ai?style=flat&color=yellow) - HexStrike AI MCP — продвинутый MCP-сервер для AI-агентов (Claude, GPT, Copilot).
- [Viper](https://github.com/FunnyWolf/Viper) ![](https://img.shields.io/github/stars/FunnyWolf/Viper?style=flat&color=yellow) - Симуляция противника и Red Teaming платформа с AI.
- [ENScan_GO](https://github.com/wgpsec/ENScan_GO) ![](https://img.shields.io/github/stars/wgpsec/ENScan_GO?style=flat&color=yellow) - 一款基于各大企业信息API的工具，解决在遇到的各种针对国内企业信息收集难题。一键收集控股公司ICP备案、APP、小程序、微信公众号等信息聚合导出。支持MCP接入.
- [EvilClippy](https://github.com/outflanknl/EvilClippy) ![](https://img.shields.io/github/stars/outflanknl/EvilClippy?style=flat&color=yellow) - Кроссплатформенный ассистент для создания вредоносных MS Office документов.
- [pentest-ai-agents](https://github.com/0xSteph/pentest-ai-agents) ![](https://img.shields.io/github/stars/0xSteph/pentest-ai-agents?style=flat&color=yellow) - Превращает Claude Code в ассистента offensive-security-исследований.

## Браузерная и web-автоматизация

- [firecrawl](https://github.com/firecrawl/firecrawl) ![](https://img.shields.io/github/stars/firecrawl/firecrawl?style=flat&color=yellow) - API для поиска, скрейпинга и работы с вебом в масштабе.
- [browser-use](https://github.com/browser-use/browser-use) ![](https://img.shields.io/github/stars/browser-use/browser-use?style=flat&color=yellow) - Делает сайты доступными для AI-агентов.
- [Scrapling](https://github.com/D4Vinci/Scrapling) ![](https://img.shields.io/github/stars/D4Vinci/Scrapling?style=flat&color=yellow) - Адаптивный фреймворк веб-скрейпинга — от запроса до пайплайна.
- [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) ![](https://img.shields.io/github/stars/ChromeDevTools/chrome-devtools-mcp?style=flat&color=yellow) - Chrome DevTools для кодинг-агентов.
- [OpenCLI](https://github.com/jackwener/OpenCLI) ![](https://img.shields.io/github/stars/jackwener/OpenCLI?style=flat&color=yellow) - Превращает любой сайт в CLI и использует залогиненный браузер AI-агентом.
- [Stagehand](https://github.com/browserbase/stagehand) ![](https://img.shields.io/github/stars/browserbase/stagehand?style=flat&color=yellow) - SDK для надёжных браузерных агентов на простых AI-примитивах.
- [lamda](https://github.com/firerpa/lamda) ![](https://img.shields.io/github/stars/firerpa/lamda?style=flat&color=yellow) - Платформа full-stack управления Android-устройствами: WebRTC-десктоп, UI/OCR.
- [browser-tools-mcp](https://github.com/AgentDeskAI/browser-tools-mcp) ![](https://img.shields.io/github/stars/AgentDeskAI/browser-tools-mcp?style=flat&color=yellow) - Мониторинг логов браузера из Cursor и других MCP-IDE.
- [firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server) ![](https://img.shields.io/github/stars/firecrawl/firecrawl-mcp-server?style=flat&color=yellow) - Официальный Firecrawl MCP — веб-скрейпинг и поиск в Cursor, Claude.
- [BrowserMCP/mcp](https://github.com/BrowserMCP/mcp) ![](https://img.shields.io/github/stars/BrowserMCP/mcp?style=flat&color=yellow) - Browser MCP — MCP-сервер управления браузером для AI-приложений.
- [exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) ![](https://img.shields.io/github/stars/exa-labs/exa-mcp-server?style=flat&color=yellow) - Exa MCP для веб-поиска и краулинга.
- [mcp-crawl4ai-rag](https://github.com/coleam00/mcp-crawl4ai-rag) ![](https://img.shields.io/github/stars/coleam00/mcp-crawl4ai-rag?style=flat&color=yellow) - Веб-краулинг и RAG для AI-агентов и кодинг-ассистентов.
- [GreasyFork-Scripts](https://github.com/F9y4ng/GreasyFork-Scripts) ![](https://img.shields.io/github/stars/F9y4ng/GreasyFork-Scripts?style=flat&color=yellow) - Open-source userscripts (скрипты Tampermonkey) для десктоп-браузеров.

## Design-to-code и фронтенд

- [awesome-design-md](https://github.com/VoltAgent/awesome-design-md) ![](https://img.shields.io/github/stars/VoltAgent/awesome-design-md?style=flat&color=yellow) - Подборка DESIGN.md-файлов систем дизайна брендов.
- [open-design](https://github.com/nexu-io/open-design) ![](https://img.shields.io/github/stars/nexu-io/open-design?style=flat&color=yellow) - Local-first open-source альтернатива Claude Design.
- [Front-End-Checklist](https://github.com/thedaviddias/Front-End-Checklist) ![](https://img.shields.io/github/stars/thedaviddias/Front-End-Checklist?style=flat&color=yellow) - Обязательный чеклист современной веб-разработки для людей и AI.
- [UI-TARS-desktop](https://github.com/bytedance/UI-TARS-desktop) ![](https://img.shields.io/github/stars/bytedance/UI-TARS-desktop?style=flat&color=yellow) - Open-source мультимодальный AI-агент-стек: модели и агентная инфраструктура.
- [ai-website-cloner-template](https://github.com/JCodesMore/ai-website-cloner-template) ![](https://img.shields.io/github/stars/JCodesMore/ai-website-cloner-template?style=flat&color=yellow) - Клонирование любого сайта одной командой через AI-агентов.
- [onlook](https://github.com/onlook-dev/onlook) ![](https://img.shields.io/github/stars/onlook-dev/onlook?style=flat&color=yellow) - Cursor для дизайнеров — open-source AI-first дизайн-инструмент.
- [frontend-slides](https://github.com/zarazhangrui/frontend-slides) ![](https://img.shields.io/github/stars/zarazhangrui/frontend-slides?style=flat&color=yellow) - Создание красивых слайдов через фронтенд-навыки кодинг-агента.
- [Figma-Context-MCP](https://github.com/GLips/Figma-Context-MCP) ![](https://img.shields.io/github/stars/GLips/Figma-Context-MCP?style=flat&color=yellow) - MCP-сервер: отдаёт вёрстку Figma AI-агентам (Cursor и др.).
- [gsap-skills](https://github.com/greensock/gsap-skills) ![](https://img.shields.io/github/stars/greensock/gsap-skills?style=flat&color=yellow) - Официальные AI-навыки для GSAP.
- [html-anything](https://github.com/nexu-io/html-anything) ![](https://img.shields.io/github/stars/nexu-io/html-anything?style=flat&color=yellow) - Агентный HTML-редактор — локальный AI-агент пишет HTML.
- [cursor-talk-to-figma-mcp](https://github.com/grab/cursor-talk-to-figma-mcp) ![](https://img.shields.io/github/stars/grab/cursor-talk-to-figma-mcp?style=flat&color=yellow) - MCP-интеграция между AI-агентом (Cursor, Claude Code) и Figma.
- [WordPress/agent-skills](https://github.com/WordPress/agent-skills) ![](https://img.shields.io/github/stars/WordPress/agent-skills?style=flat&color=yellow) - Экспертные знания WordPress для AI-ассистентов кодинга.
- [callstackincubator/agent-skills](https://github.com/callstackincubator/agent-skills) ![](https://img.shields.io/github/stars/callstackincubator/agent-skills?style=flat&color=yellow) - React Native навыки для AI-ассистентов кодинга.

## App builders и low-code

- [n8n](https://github.com/n8n-io/n8n) ![](https://img.shields.io/github/stars/n8n-io/n8n?style=flat&color=yellow) - Платформа автоматизации воркфлоу с нативными AI-возможностями.
- [langflow](https://github.com/langflow-ai/langflow) ![](https://img.shields.io/github/stars/langflow-ai/langflow?style=flat&color=yellow) - Мощный инструмент создания и деплоя AI-агентов и воркфлоу.
- [dify](https://github.com/langgenius/dify) ![](https://img.shields.io/github/stars/langgenius/dify?style=flat&color=yellow) - Production-готовая платформа для разработки агентных воркфлоу.
- [Flowise](https://github.com/FlowiseAI/Flowise) ![](https://img.shields.io/github/stars/FlowiseAI/Flowise?style=flat&color=yellow) - Визуальное построение AI-агентов.
- [JeecgBoot](https://github.com/jeecgboot/JeecgBoot) ![](https://img.shields.io/github/stars/jeecgboot/JeecgBoot?style=flat&color=yellow) - AI low-code платформа: низкий + нулевой код, генерация систем одной фразой.
- [activepieces](https://github.com/activepieces/activepieces) ![](https://img.shields.io/github/stars/activepieces/activepieces?style=flat&color=yellow) - AI-агенты, MCP и автоматизация воркфлоу (~400 MCP-серверов).
- [n8n-mcp](https://github.com/czlonkowski/n8n-mcp) ![](https://img.shields.io/github/stars/czlonkowski/n8n-mcp?style=flat&color=yellow) - MCP для Claude Desktop/Code/Windsurf/Cursor: строит n8n-воркфлоу.
- [MaxKB](https://github.com/1Panel-dev/MaxKB) ![](https://img.shields.io/github/stars/1Panel-dev/MaxKB?style=flat&color=yellow) - Open-source платформа для enterprise-агентов.
- [bisheng](https://github.com/dataelement/bisheng) ![](https://img.shields.io/github/stars/dataelement/bisheng?style=flat&color=yellow) - Open LLM DevOps платформа для enterprise AI-приложений.
- [refly](https://github.com/refly-ai/refly) ![](https://img.shields.io/github/stars/refly-ai/refly?style=flat&color=yellow) - Первый open-source билдер навыков агентов.
- [pyspur](https://github.com/PySpur-Dev/pyspur) ![](https://img.shields.io/github/stars/PySpur-Dev/pyspur?style=flat&color=yellow) - Визуальная площадка агентных воркфлоу — итерируйте агентов в 10x быстрее.
- [oinone-pamirs](https://github.com/oinone/oinone-pamirs) ![](https://img.shields.io/github/stars/oinone/oinone-pamirs?style=flat&color=yellow) - Oinone — AI-powered low-code фреймворк, объединяющий AI и разработчиков.
- [agents](https://github.com/inkeep/agents) ![](https://img.shields.io/github/stars/inkeep/agents?style=flat&color=yellow) - Создание AI-агентов в no-code билдере или TypeScript SDK.

## Разработка игр

- [GDevelop](https://github.com/4ian/GDevelop) ![](https://img.shields.io/github/stars/4ian/GDevelop?style=flat&color=yellow) - Open-source кроссплатформенный 2D/3D/мультиплеерный игровой движок.
- [Claude-Code-Game-Studios](https://github.com/Donchitos/Claude-Code-Game-Studios) ![](https://img.shields.io/github/stars/Donchitos/Claude-Code-Game-Studios?style=flat&color=yellow) - Превращает Claude Code в студию геймдева — 49 AI-агентов, 72 навыка.

## Контекст, память и индексирование кода

- [graphify](https://github.com/safishamsi/graphify) ![](https://img.shields.io/github/stars/safishamsi/graphify?style=flat&color=yellow) - Навык AI-ассистента кодинга (Claude Code, Codex, Cursor, Gemini).
- [claude-mem](https://github.com/thedotmack/claude-mem) ![](https://img.shields.io/github/stars/thedotmack/claude-mem?style=flat&color=yellow) - Постоянный контекст между сессиями для любого AI-агента.
- [ragflow](https://github.com/infiniflow/ragflow) ![](https://img.shields.io/github/stars/infiniflow/ragflow?style=flat&color=yellow) - Open-source RAG-движок, объединяющий глубокое понимание документов.
- [mem0](https://github.com/mem0ai/mem0) ![](https://img.shields.io/github/stars/mem0ai/mem0?style=flat&color=yellow) - Универсальный слой памяти для AI-агентов.
- [headroom](https://github.com/headroomlabs-ai/headroom) ![](https://img.shields.io/github/stars/headroomlabs-ai/headroom?style=flat&color=yellow) - Сжатие выводов инструментов, логов и RAG-чанков до LLM.
- [mempalace](https://github.com/MemPalace/mempalace) ![](https://img.shields.io/github/stars/MemPalace/mempalace?style=flat&color=yellow) - Лучший по бенчмаркам open-source AI-слой памяти.
- [llama_index](https://github.com/run-llama/llama_index) ![](https://img.shields.io/github/stars/run-llama/llama_index?style=flat&color=yellow) - Ведущая платформа document-агентов и OCR.
- [LightRAG](https://github.com/HKUDS/LightRAG) ![](https://img.shields.io/github/stars/HKUDS/LightRAG?style=flat&color=yellow) - Простое и быстрое дополненное получение.
- [Vane](https://github.com/ItzCrazyKns/Vane) ![](https://img.shields.io/github/stars/ItzCrazyKns/Vane?style=flat&color=yellow) - AI-powered поисковый движок ответов.
- [codebase-memory-mcp](https://github.com/DeusData/codebase-memory-mcp) ![](https://img.shields.io/github/stars/DeusData/codebase-memory-mcp?style=flat&color=yellow) - Высокопроизводительный MCP-сервер интеллекта кодовой базы.
- [PageIndex](https://github.com/VectifyAI/PageIndex) ![](https://img.shields.io/github/stars/VectifyAI/PageIndex?style=flat&color=yellow) - Индекс документов для reasoning-based RAG без векторов.
- [cognee](https://github.com/topoteretes/cognee) ![](https://img.shields.io/github/stars/topoteretes/cognee?style=flat&color=yellow) - Open-source AI-платформа памяти для агентов.
- [chroma](https://github.com/chroma-core/chroma) ![](https://img.shields.io/github/stars/chroma-core/chroma?style=flat&color=yellow) - Поисковая инфраструктура для AI.
- [Repomix](https://github.com/yamadashy/repomix) ![](https://img.shields.io/github/stars/yamadashy/repomix?style=flat&color=yellow) - Упаковывает весь репозиторий в один файл для подсчёта контекста AI.
- [serena](https://github.com/oraios/serena) ![](https://img.shields.io/github/stars/oraios/serena?style=flat&color=yellow) - Мощный MCP-тулкит для кодинга: семантический поиск и редактирование.
- [agentmemory](https://github.com/rohitg00/agentmemory) ![](https://img.shields.io/github/stars/rohitg00/agentmemory?style=flat&color=yellow) - 1 Persistent memory for AI coding agents based on real-world benchmarks.
- [OpenMetadata](https://github.com/open-metadata/OpenMetadata) ![](https://img.shields.io/github/stars/open-metadata/OpenMetadata?style=flat&color=yellow) - Open Context Layer для данных и AI: построение траста данных.
- [claude-context](https://github.com/zilliztech/claude-context) ![](https://img.shields.io/github/stars/zilliztech/claude-context?style=flat&color=yellow) - MCP поиска кода для Claude Code.
- [code2prompt](https://github.com/mufeedvh/code2prompt) ![](https://img.shields.io/github/stars/mufeedvh/code2prompt?style=flat&color=yellow) - CLI: превращает кодовую базу в один Markdown-промпт для LLM.
- [semble](https://github.com/MinishLab/semble) ![](https://img.shields.io/github/stars/MinishLab/semble?style=flat&color=yellow) - Быстрый и точный поиск кода для агентов.
- [byterover-cli](https://github.com/campfirein/byterover-cli) ![](https://img.shields.io/github/stars/campfirein/byterover-cli?style=flat&color=yellow) - ByteRover CLI (brv) — переносимый слой памяти для автономных кодинг-агентов.
- [Zep](https://github.com/getzep/zep) ![](https://img.shields.io/github/stars/getzep/zep?style=flat&color=yellow) - Сервис долговременной памяти для диалогового и агентного AI.
- [CodeGraphContext](https://github.com/CodeGraphContext/CodeGraphContext) ![](https://img.shields.io/github/stars/CodeGraphContext/CodeGraphContext?style=flat&color=yellow) - MCP-сервер + CLI: индексирует код в графовую БД для контекста.
- [RooFlow](https://github.com/GreatScottyMac/RooFlow) ![](https://img.shields.io/github/stars/GreatScottyMac/RooFlow?style=flat&color=yellow) - Улучшенная система Memory Bank для агентов.

## MCP-серверы и клиенты

- [awesome-mcp-servers](https://github.com/punkpeye/awesome-mcp-servers) ![](https://img.shields.io/github/stars/punkpeye/awesome-mcp-servers?style=flat&color=yellow) - Кураторская подборка серверов Model Context Protocol.
- [MCP Servers](https://github.com/modelcontextprotocol/servers) ![](https://img.shields.io/github/stars/modelcontextprotocol/servers?style=flat&color=yellow) - Эталонные реализации серверов Model Context Protocol.
- [GitHub MCP Server](https://github.com/github/github-mcp-server) ![](https://img.shields.io/github/stars/github/github-mcp-server?style=flat&color=yellow) - Официальный MCP-сервер GitHub для работы с репозиториями, issues и PR.
- [FastMCP](https://github.com/PrefectHQ/fastmcp) ![](https://img.shields.io/github/stars/PrefectHQ/fastmcp?style=flat&color=yellow) - Быстрый питонический фреймворк для создания MCP-серверов и клиентов.
- [fastapi_mcp](https://github.com/tadata-org/fastapi_mcp) ![](https://img.shields.io/github/stars/tadata-org/fastapi_mcp?style=flat&color=yellow) - Экспонирует эндпоинты FastAPI как MCP-инструменты с Auth.
- [mcp-use](https://github.com/mcp-use/mcp-use) ![](https://img.shields.io/github/stars/mcp-use/mcp-use?style=flat&color=yellow) - Fullstack MCP-фреймворк для разработки MCP-приложений.
- [DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP) ![](https://img.shields.io/github/stars/wonderwhy-er/DesktopCommanderMCP?style=flat&color=yellow) - MCP-сервер для Claude: контроль терминала, поиск файловой системы, diff.
- [Awesome-MCP-ZH](https://github.com/yzfly/Awesome-MCP-ZH) ![](https://img.shields.io/github/stars/yzfly/Awesome-MCP-ZH?style=flat&color=yellow) - MCP ресурсы на китайском: гайд, Claude MCP, серверы, клиенты.
- [klavis](https://github.com/Klavis-AI/klavis) ![](https://img.shields.io/github/stars/Klavis-AI/klavis?style=flat&color=yellow) - Klavis AI — платформа MCP-интеграции для надёжных инструментов агентов.
- [metamcp](https://github.com/metatool-ai/metamcp) ![](https://img.shields.io/github/stars/metatool-ai/metamcp?style=flat&color=yellow) - MCP-агрегатор, оркестратор, middleware и шлюз в одном docker.

## Skills, промпты и правила агентов

- [prompts.chat](https://github.com/f/prompts.chat) ![](https://img.shields.io/github/stars/f/prompts.chat?style=flat&color=yellow) - F.k.a. Awesome ChatGPT Prompts. Share, discover, and collect prompts from the community. Free and open source — self-host for your organization with complete privacy.
- [system-prompts-and-models-of-ai-tools](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools) ![](https://img.shields.io/github/stars/x1xhlol/system-prompts-and-models-of-ai-tools?style=flat&color=yellow) - Системные промпты и модели AI-инструментов (Augment, Claude Code, Cursor и др.).
- [caveman](https://github.com/JuliusBrussee/caveman) ![](https://img.shields.io/github/stars/JuliusBrussee/caveman?style=flat&color=yellow) - Why use many token when few token do trick — Claude Code skill that cuts 65% of tokens by talking like caveman.
- [ponytail](https://github.com/DietrichGebert/ponytail) ![](https://img.shields.io/github/stars/DietrichGebert/ponytail?style=flat&color=yellow) - Заставляет AI-агента думать как самый ленивый senior-разработчик.
- [agent-skills](https://github.com/addyosmani/agent-skills) ![](https://img.shields.io/github/stars/addyosmani/agent-skills?style=flat&color=yellow) - Продакшн-навыки инженерии для AI-агентов кодинга.
- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills) ![](https://img.shields.io/github/stars/ComposioHQ/awesome-claude-skills?style=flat&color=yellow) - Кураторский список Claude Skills, ресурсов и инструментов.
- [taste-skill](https://github.com/Leonxlnx/taste-skill) ![](https://img.shields.io/github/stars/Leonxlnx/taste-skill?style=flat&color=yellow) - Taste-Skill — даёт AI хороший вкус.
- [oh-my-openagent](https://github.com/code-yeongyu/oh-my-openagent) ![](https://img.shields.io/github/stars/code-yeongyu/oh-my-openagent?style=flat&color=yellow) - Omo/lazycodex: The coding agent for tokenmaxxers;the one and only agent harness for complex codebases. For your Codex, for your OpenCode.
- [claude-code-best-practice](https://github.com/shanraisshan/claude-code-best-practice) ![](https://img.shields.io/github/stars/shanraisshan/claude-code-best-practice?style=flat&color=yellow) - From vibe coding to agentic engineering - practice makes claude perfect.
- [system_prompts_leaks](https://github.com/asgeirtj/system_prompts_leaks) ![](https://img.shields.io/github/stars/asgeirtj/system_prompts_leaks?style=flat&color=yellow) - Извлечённые системные промпты Anthropic: Claude Fable 5, Opus 4.8 и др.
- [awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) ![](https://img.shields.io/github/stars/hesreallyhim/awesome-claude-code?style=flat&color=yellow) - Кураторский список навыков, хуков, команд и оркестраторов Claude Code.
- [cherry-studio](https://github.com/CherryHQ/cherry-studio) ![](https://img.shields.io/github/stars/CherryHQ/cherry-studio?style=flat&color=yellow) - AI-студия продуктивности: умный чат, агенты, 300+ ассистентов.
- [CL4R1T4S](https://github.com/elder-plinius/CL4R1T4S) ![](https://img.shields.io/github/stars/elder-plinius/CL4R1T4S?style=flat&color=yellow) - Утечки системных промптов ChatGPT, Claude, Gemini, Grok, Cursor и др.
- [antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills) ![](https://img.shields.io/github/stars/sickn33/antigravity-awesome-skills?style=flat&color=yellow) - Библиотека 1800+ агентных навыков для Claude Code, Cursor, Codex.
- [marketingskills](https://github.com/coreyhaines31/marketingskills) ![](https://img.shields.io/github/stars/coreyhaines31/marketingskills?style=flat&color=yellow) - Маркетинговые навыки для Claude Code и AI-агентов.
- [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) ![](https://img.shields.io/github/stars/Imbad0202/academic-research-skills?style=flat&color=yellow) - Навыки академических исследований для Claude Code.
- [awesome-copilot](https://github.com/github/awesome-copilot) ![](https://img.shields.io/github/stars/github/awesome-copilot?style=flat&color=yellow) - Инструкции, агенты, навыки и конфиги сообщества для GitHub Copilot.
- [prompt-optimizer](https://github.com/linshenkx/prompt-optimizer) ![](https://img.shields.io/github/stars/linshenkx/prompt-optimizer?style=flat&color=yellow) - AI-оптимизатор промптов для лучших результатов.
- [scientific-agent-skills](https://github.com/K-Dense-AI/scientific-agent-skills) ![](https://img.shields.io/github/stars/K-Dense-AI/scientific-agent-skills?style=flat&color=yellow) - Превращает любой AI-агент в AI-учёного.
- [awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) ![](https://img.shields.io/github/stars/VoltAgent/awesome-agent-skills?style=flat&color=yellow) - Подборка 1000+ агентных навыков от команд и сообщества.
- [planning-with-files](https://github.com/OthmanAdi/planning-with-files) ![](https://img.shields.io/github/stars/OthmanAdi/planning-with-files?style=flat&color=yellow) - Постоянное файловое планирование для AI-агентов кодинга.
- [claude-skills](https://github.com/alirezarezvani/claude-skills) ![](https://img.shields.io/github/stars/alirezarezvani/claude-skills?style=flat&color=yellow) - 337 Claude Code skills & agent skills & plugins (30+ Agents, 70+ custom commands, 330+ skills, customizable references, scripts)for Claude Code, Codex, Gemini CLI, Cursor, and 8 more coding agents — engineering, marketing, product, compliance, C-level advisory, research, business operations, commercial & finance, and your daily productivity skills.
- [context-mode](https://github.com/mksglu/context-mode) ![](https://img.shields.io/github/stars/mksglu/context-mode?style=flat&color=yellow) - Оптимизация контекстного окна для AI-агентов кодинга.
- [agency-agents-zh](https://github.com/jnMetaCode/agency-agents-zh) ![](https://img.shields.io/github/stars/jnMetaCode/agency-agents-zh?style=flat&color=yellow) - Агенты agency (китайская версия).
- [notebooklm-py](https://github.com/teng-lin/notebooklm-py) ![](https://img.shields.io/github/stars/teng-lin/notebooklm-py?style=flat&color=yellow) - Неофициальный Python API и навык для Google NotebookLM.
- [Skill_Seekers](https://github.com/yusufkaraaslan/Skill_Seekers) ![](https://img.shields.io/github/stars/yusufkaraaslan/Skill_Seekers?style=flat&color=yellow) - Конвертация сайтов-документаций, GitHub-репо и PDF в Claude AI-навыки.
- [Auto-claude-code-research-in-sleep](https://github.com/wanshuiyin/Auto-claude-code-research-in-sleep) ![](https://img.shields.io/github/stars/wanshuiyin/Auto-claude-code-research-in-sleep?style=flat&color=yellow) - ARIS — лёгкие Markdown-навыки автономных ML-исследований.
- [awesome-nano-banana-pro-prompts](https://github.com/YouMind-OpenLab/awesome-nano-banana-pro-prompts) ![](https://img.shields.io/github/stars/YouMind-OpenLab/awesome-nano-banana-pro-prompts?style=flat&color=yellow) - Крупнейшая библиотека промптов Nano Banana Pro — 10000+ с превью.
- [LangGPT](https://github.com/langgptai/LangGPT) ![](https://img.shields.io/github/stars/langgptai/LangGPT?style=flat&color=yellow) - LangGPT — структурированные промпты для каждого.
- [AI-Research-SKILLs](https://github.com/Orchestra-Research/AI-Research-SKILLs) ![](https://img.shields.io/github/stars/Orchestra-Research/AI-Research-SKILLs?style=flat&color=yellow) - Библиотека AI-research и инженерных навыков для любой модели.
- [chatgpt_system_prompt](https://github.com/LouisShark/chatgpt_system_prompt) ![](https://img.shields.io/github/stars/LouisShark/chatgpt_system_prompt?style=flat&color=yellow) - Коллекция системных промптов GPT и знаний о prompt injection.
- [prompt-master](https://github.com/nidhinjs/prompt-master) ![](https://img.shields.io/github/stars/nidhinjs/prompt-master?style=flat&color=yellow) - Навык Claude, пишущий точные промпты для любого AI-инструмента.
- [openskills](https://github.com/numman-ali/openskills) ![](https://img.shields.io/github/stars/numman-ali/openskills?style=flat&color=yellow) - Универсальный загрузчик навыков для AI-агентов кодинга.
- [awesome-nanobanana-pro](https://github.com/ZeroLu/awesome-nanobanana-pro) ![](https://img.shields.io/github/stars/ZeroLu/awesome-nanobanana-pro?style=flat&color=yellow) - Кураторский список промптов и примеров Nano Banana pro.
- [YouMind-OpenLab/awesome-gpt-image-2](https://github.com/YouMind-OpenLab/awesome-gpt-image-2) ![](https://img.shields.io/github/stars/YouMind-OpenLab/awesome-gpt-image-2?style=flat&color=yellow) - Крупнейшая библиотека промптов GPT Image 2 — 2000+, ежедневное обновление.
- [ChatGPT-Shortcut](https://github.com/rockbenben/ChatGPT-Shortcut) ![](https://img.shields.io/github/stars/rockbenben/ChatGPT-Shortcut?style=flat&color=yellow) - Максимизируйте эффективность и продуктивность.
- [awesome-gpt-image-2](https://github.com/freestylefly/awesome-gpt-image-2) ![](https://img.shields.io/github/stars/freestylefly/awesome-gpt-image-2?style=flat&color=yellow) - Промпт как код: промышленный движок промптов GPT-Image2, 470+ кейсов.
- [awesome-prompts](https://github.com/ai-boost/awesome-prompts) ![](https://img.shields.io/github/stars/ai-boost/awesome-prompts?style=flat&color=yellow) - Кураторский список промптов ChatGPT из топовых GPTs Store.
- [ccpm](https://github.com/automazeio/ccpm) ![](https://img.shields.io/github/stars/automazeio/ccpm?style=flat&color=yellow) - Система навыков управления проектами для агентов на GitHub Issues и worktrees.
- [awesome-gpt4o-images](https://github.com/jamez-bondos/awesome-gpt4o-images) ![](https://img.shields.io/github/stars/jamez-bondos/awesome-gpt4o-images?style=flat&color=yellow) - Подборка изображений и промптов, сгенерированных GPT-4o и gpt-image-1.
- [Prompt_Engineering](https://github.com/NirDiamant/Prompt_Engineering) ![](https://img.shields.io/github/stars/NirDiamant/Prompt_Engineering?style=flat&color=yellow) - 22 prompt engineering techniques with hands-on Jupyter Notebook tutorials, from fundamental concepts to advanced strategies for leveraging LLMs.
- [superpowers-zh](https://github.com/jnMetaCode/superpowers-zh) ![](https://img.shields.io/github/stars/jnMetaCode/superpowers-zh?style=flat&color=yellow) - AI-суперсилы кодинга — китайская расширенная версия superpowers.
- [SuperPrompt](https://github.com/NeoVertex1/SuperPrompt) ![](https://img.shields.io/github/stars/NeoVertex1/SuperPrompt?style=flat&color=yellow) - SuperPrompt — промпты, помогающие понять AI-агентов.
- [ai-notes](https://github.com/swyxio/ai-notes) ![](https://img.shields.io/github/stars/swyxio/ai-notes?style=flat&color=yellow) - Notes for software engineers getting up to speed on new AI developments. Serves as datastore for https://latent.space writing, and product brainstorming, but has cleaned up canonical references under the /Resources folder.
- [wonderful-prompts](https://github.com/langgptai/wonderful-prompts) ![](https://img.shields.io/github/stars/langgptai/wonderful-prompts?style=flat&color=yellow) - 中文 prompt 精选，ChatGPT 使用指南，提升 ChatGPT 可玩性和可用性！.
- [Awesome-Prompt-Engineering](https://github.com/promptslab/Awesome-Prompt-Engineering) ![](https://img.shields.io/github/stars/promptslab/Awesome-Prompt-Engineering?style=flat&color=yellow) - Ручная подборка ресурсов по prompt engineering.
- [awesome-ai-system-prompts](https://github.com/dontriskit/awesome-ai-system-prompts) ![](https://img.shields.io/github/stars/dontriskit/awesome-ai-system-prompts?style=flat&color=yellow) - Кураторская подборка системных промптов топовых AI-инструментов.
- [ell](https://github.com/MadcowD/ell) ![](https://img.shields.io/github/stars/MadcowD/ell?style=flat&color=yellow) - Библиотека программирования языковых моделей.
- [claude-code-ultimate-guide](https://github.com/FlorianBruniaux/claude-code-ultimate-guide) ![](https://img.shields.io/github/stars/FlorianBruniaux/claude-code-ultimate-guide?style=flat&color=yellow) - Самый полный гайд по Claude Code: воркфлоу, хуки, навыки, MCP.
- [agents-cli](https://github.com/google/agents-cli) ![](https://img.shields.io/github/stars/google/agents-cli?style=flat&color=yellow) - CLI и навыки, превращающие AI-ассистента в эксперта по агентам.
- [Learning-Prompt](https://github.com/thinkingjimmy/Learning-Prompt) ![](https://img.shields.io/github/stars/thinkingjimmy/Learning-Prompt?style=flat&color=yellow) - Бесплатный онлайн-курс prompt engineering.
- [ruler](https://github.com/intellectronica/ruler) ![](https://img.shields.io/github/stars/intellectronica/ruler?style=flat&color=yellow) - Ruler — применяйте одни правила ко всем кодинг-агентам.
- [cc-skills-golang](https://github.com/samber/cc-skills-golang) ![](https://img.shields.io/github/stars/samber/cc-skills-golang?style=flat&color=yellow) - Навыки Claude Code для Go.
- [vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template) ![](https://img.shields.io/github/stars/KhazP/vibe-coding-prompt-template?style=flat&color=yellow) - Шаблоны и воркфлоу для PRD, тех-дизайнов и MVP через LLM.
- [Vibe-Skills](https://github.com/foryourhealth111-pixel/Vibe-Skills) ![](https://img.shields.io/github/stars/foryourhealth111-pixel/Vibe-Skills?style=flat&color=yellow) - Vibe-Skills — all-in-one пакет AI-навыков.
- [best-skills](https://github.com/xstongxue/best-skills) ![](https://img.shields.io/github/stars/xstongxue/best-skills?style=flat&color=yellow) - 通用高质量 Skills 合集.
- [Sunbeam](https://github.com/pomdtr/sunbeam) ![](https://img.shields.io/github/stars/pomdtr/sunbeam?style=flat&color=yellow) - Просмотр и поиск библиотек промптов с конвертацией в любой формат.

## AI-ассистенты

- [ECC](https://github.com/affaan-m/ECC) ![](https://img.shields.io/github/stars/affaan-m/ECC?style=flat&color=yellow) - Система оптимизации производительности agent-харнеса.
- [hermes-agent](https://github.com/NousResearch/hermes-agent) ![](https://img.shields.io/github/stars/NousResearch/hermes-agent?style=flat&color=yellow) - Агент, который растёт вместе с вами.
- [AutoGPT](https://github.com/Significant-Gravitas/AutoGPT) ![](https://img.shields.io/github/stars/Significant-Gravitas/AutoGPT?style=flat&color=yellow) - AutoGPT — доступный AI для всех: использование и развитие.
- [langchain](https://github.com/langchain-ai/langchain) ![](https://img.shields.io/github/stars/langchain-ai/langchain?style=flat&color=yellow) - Платформа agent-инжиниринга.
- [deer-flow](https://github.com/bytedance/deer-flow) ![](https://img.shields.io/github/stars/bytedance/deer-flow?style=flat&color=yellow) - Open-source харнес SuperAgent: исследования, код, креатив.
- [MetaGPT](https://github.com/FoundationAgents/MetaGPT) ![](https://img.shields.io/github/stars/FoundationAgents/MetaGPT?style=flat&color=yellow) - Мультиагентный фреймворк: первая AI software-компания.
- [Claude Flow](https://github.com/ruvnet/claude-flow) ![](https://img.shields.io/github/stars/ruvnet/claude-flow?style=flat&color=yellow) - Оркестрация роя агентов Claude Code для сложных задач.
- [ruflo](https://github.com/ruvnet/ruflo) ![](https://img.shields.io/github/stars/ruvnet/ruflo?style=flat&color=yellow) - Ведущий мета-харнес для агентов.
- [crewAI](https://github.com/crewAIInc/crewAI) ![](https://img.shields.io/github/stars/crewAIInc/crewAI?style=flat&color=yellow) - Фреймворк оркестрации ролевых автономных AI-агентов.
- [agno](https://github.com/agno-agi/agno) ![](https://img.shields.io/github/stars/agno-agi/agno?style=flat&color=yellow) - Создание, запуск и управление agent-платформами.
- [wshobson/agents](https://github.com/wshobson/agents) ![](https://img.shields.io/github/stars/wshobson/agents?style=flat&color=yellow) - Библиотека специализированных сабагентов Claude Code для агентных воркфлоу.
- [oh-my-claudecode](https://github.com/Yeachan-Heo/oh-my-claudecode) ![](https://img.shields.io/github/stars/Yeachan-Heo/oh-my-claudecode?style=flat&color=yellow) - Teams-first мультиагентная оркестрация для Claude Code.
- [langgraph](https://github.com/langchain-ai/langgraph) ![](https://img.shields.io/github/stars/langchain-ai/langgraph?style=flat&color=yellow) - Построение устойчивых агентов.
- [nanoclaw](https://github.com/nanocoai/nanoclaw) ![](https://img.shields.io/github/stars/nanocoai/nanoclaw?style=flat&color=yellow) - Легковесная альтернатива OpenClaw в контейнерах для безопасности.
- [composio](https://github.com/ComposioHQ/composio) ![](https://img.shields.io/github/stars/ComposioHQ/composio?style=flat&color=yellow) - 1000+ тулкитов, поиск инструментов, контекст и аутентификация для агентов.
- [agentscope](https://github.com/agentscope-ai/agentscope) ![](https://img.shields.io/github/stars/agentscope-ai/agentscope?style=flat&color=yellow) - Создание и запуск агентов, которым видно, понимаешь и доверяешь.
- [haystack](https://github.com/deepset-ai/haystack) ![](https://img.shields.io/github/stars/deepset-ai/haystack?style=flat&color=yellow) - Open-source AI-фреймворк оркестрации для production LLM-приложений.
- [12-Factor Agents](https://github.com/humanlayer/12-factor-agents) ![](https://img.shields.io/github/stars/humanlayer/12-factor-agents?style=flat&color=yellow) - Принципы создания production-готового ПО на LLM-агентах.
- [adk-python](https://github.com/google/adk-python) ![](https://img.shields.io/github/stars/google/adk-python?style=flat&color=yellow) - Open-source Python-тулкит для создания, оценки и деплоя agent-приложений.
- [eliza](https://github.com/elizaOS/eliza) ![](https://img.shields.io/github/stars/elizaOS/eliza?style=flat&color=yellow) - Open-source агентная операционная система.
- [camel](https://github.com/camel-ai/camel) ![](https://img.shields.io/github/stars/camel-ai/camel?style=flat&color=yellow) - CAMEL — первый и лучший мультиагентный фреймворк.
- [PocketFlow-Tutorial-Codebase-Knowledge](https://github.com/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge) ![](https://img.shields.io/github/stars/The-Pocket/PocketFlow-Tutorial-Codebase-Knowledge?style=flat&color=yellow) - Pocket Flow — от кодовой базы к туториалу.
- [PocketFlow](https://github.com/The-Pocket/PocketFlow) ![](https://img.shields.io/github/stars/The-Pocket/PocketFlow?style=flat&color=yellow) - Pocket Flow — LLM-фреймворк на 100 строк.
- [evolver](https://github.com/EvoMap/evolver) ![](https://img.shields.io/github/stars/EvoMap/evolver?style=flat&color=yellow) - GEP-powered самоэволюционирующий движок для AI-агентов.
- [adk-go](https://github.com/google/adk-go) ![](https://img.shields.io/github/stars/google/adk-go?style=flat&color=yellow) - Open-source Go-тулкит для создания, оценки и деплоя agent-приложений.
- [PraisonAI](https://github.com/MervinPraison/PraisonAI) ![](https://img.shields.io/github/stars/MervinPraison/PraisonAI?style=flat&color=yellow) - Нанимайте AI-рабочую силу 24/7.
- [swarms](https://github.com/kyegomez/swarms) ![](https://img.shields.io/github/stars/kyegomez/swarms?style=flat&color=yellow) - Enterprise-grade мультиагентный фреймворк оркестрации для продакшна.
- [openagent](https://github.com/the-open-agent/openagent) ![](https://img.shields.io/github/stars/the-open-agent/openagent?style=flat&color=yellow) - Next-generation personal AI assistant powered by LLM, RAG and agent loops, supporting computer-use, browser-use and coding agent, demo: https://demo.openagentai.org.
- [AdalFlow](https://github.com/SylphAI-Inc/AdalFlow) ![](https://img.shields.io/github/stars/SylphAI-Inc/AdalFlow?style=flat&color=yellow) - AdalFlow — библиотека построения и автооптимизации LLM-приложений.
- [eve](https://github.com/vercel/eve) ![](https://img.shields.io/github/stars/vercel/eve?style=flat&color=yellow) - Фреймворк построения агентов.
- [core](https://github.com/cheshire-cat-ai/core) ![](https://img.shields.io/github/stars/cheshire-cat-ai/core?style=flat&color=yellow) - AI-агент микросервис.
- [helixent](https://github.com/MagicCube/helixent) ![](https://img.shields.io/github/stars/MagicCube/helixent?style=flat&color=yellow) - Маленькая библиотека для ReAct-style циклов AI-агентов на Bun.

## Наблюдаемость и eval

- [posthog](https://github.com/PostHog/posthog) ![](https://img.shields.io/github/stars/PostHog/posthog?style=flat&color=yellow) - All-in-one платформа для разработчиков: аналитика, фича-флаги, сессии.
- [Langfuse](https://github.com/langfuse/langfuse) ![](https://img.shields.io/github/stars/langfuse/langfuse?style=flat&color=yellow) - Open-source наблюдаемость для LLM: трейсинг, оценка и управление промптами.
- [mlflow](https://github.com/mlflow/mlflow) ![](https://img.shields.io/github/stars/mlflow/mlflow?style=flat&color=yellow) - Open-source AI-инжиниринг платформа для агентов, LLM и ML-моделей.
- [Promptfoo](https://github.com/promptfoo/promptfoo) ![](https://img.shields.io/github/stars/promptfoo/promptfoo?style=flat&color=yellow) - Тестирование и редтим промптов, агентов и RAG для разных провайдеров.
- [opik](https://github.com/comet-ml/opik) ![](https://img.shields.io/github/stars/comet-ml/opik?style=flat&color=yellow) - Дебаг, оценка и мониторинг LLM-приложений, RAG и агентных воркфлоу.
- [openobserve](https://github.com/openobserve/openobserve) ![](https://img.shields.io/github/stars/openobserve/openobserve?style=flat&color=yellow) - Open-source платформа наблюдаемости: логи, метрики, трейсы, мониторинг.
- [RagaAI-Catalyst](https://github.com/raga-ai-hub/RagaAI-Catalyst) ![](https://img.shields.io/github/stars/raga-ai-hub/RagaAI-Catalyst?style=flat&color=yellow) - Python SDK для наблюдаемости, мониторинга и оценки Agent AI.
- [phoenix](https://github.com/Arize-ai/phoenix) ![](https://img.shields.io/github/stars/Arize-ai/phoenix?style=flat&color=yellow) - Наблюдаемость и оценка AI.
- [codeburn](https://github.com/getagentseal/codeburn) ![](https://img.shields.io/github/stars/getagentseal/codeburn?style=flat&color=yellow) - Локальный трекер использования токенов и затрат AI-кодинга (31 инструмент).
- [evidently](https://github.com/evidentlyai/evidently) ![](https://img.shields.io/github/stars/evidentlyai/evidently?style=flat&color=yellow) - Open-source фреймворк наблюдаемости ML и LLM.
- [openllmetry](https://github.com/traceloop/openllmetry) ![](https://img.shields.io/github/stars/traceloop/openllmetry?style=flat&color=yellow) - Open-source наблюдаемость для GenAI/LLM на базе OpenTelemetry.
- [aim](https://github.com/aimhubio/aim) ![](https://img.shields.io/github/stars/aimhubio/aim?style=flat&color=yellow) - Aim — простой open-source трекер экспериментов.
- [Helicone](https://github.com/Helicone/helicone) ![](https://img.shields.io/github/stars/Helicone/helicone?style=flat&color=yellow) - Open-source наблюдаемость LLM: мониторинг, оценка и эксперименты.
- [logfire](https://github.com/pydantic/logfire) ![](https://img.shields.io/github/stars/pydantic/logfire?style=flat&color=yellow) - Платформа наблюдаемости для production LLM и агентных систем.
- [agenta](https://github.com/Agenta-AI/agenta) ![](https://img.shields.io/github/stars/Agenta-AI/agenta?style=flat&color=yellow) - Open-source LLMOps: prompt playground, оценка LLM, управление.
- [OpenLit](https://github.com/openlit/openlit) ![](https://img.shields.io/github/stars/openlit/openlit?style=flat&color=yellow) - LLM-наблюдаемость на базе OpenTelemetry: GPU-мониторинг и гардраилы.
- [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) ![](https://img.shields.io/github/stars/UKGovernmentBEIS/inspect_ai?style=flat&color=yellow) - Фреймворк для оценки LLM от Института безопасности ИИ.
- [trench](https://github.com/FrigadeHQ/trench) ![](https://img.shields.io/github/stars/FrigadeHQ/trench?style=flat&color=yellow) - Open-source инфраструктура аналитики.
- [ClaudeBar](https://github.com/tddworks/ClaudeBar) ![](https://img.shields.io/github/stars/tddworks/ClaudeBar?style=flat&color=yellow) - MacOS-меню приложение: мониторинг квот AI-ассистентов кодинга.
- [sniffly](https://github.com/chiphuyen/sniffly) ![](https://img.shields.io/github/stars/chiphuyen/sniffly?style=flat&color=yellow) - Дашборд Claude Code: статистика использования, анализ ошибок.
- [prompty](https://github.com/microsoft/prompty) ![](https://img.shields.io/github/stars/microsoft/prompty?style=flat&color=yellow) - Создание, управление и оценка LLM-промптов для AI-приложений.
- [langtrace](https://github.com/Scale3-Labs/langtrace) ![](https://img.shields.io/github/stars/Scale3-Labs/langtrace?style=flat&color=yellow) - Open-source end-to-end наблюдаемость LLM на OpenTelemetry.
- [langkit](https://github.com/whylabs/langkit) ![](https://img.shields.io/github/stars/whylabs/langkit?style=flat&color=yellow) - Open-source тулкит мониторинга больших языковых моделей.

## Документация, research и knowledge work

- [Understand-Anything](https://github.com/Egonex-AI/Understand-Anything) ![](https://img.shields.io/github/stars/Egonex-AI/Understand-Anything?style=flat&color=yellow) - Графы, которые обучают, а не просто впечатляют.
- [learn-claude-code](https://github.com/shareAI-lab/learn-claude-code) ![](https://img.shields.io/github/stars/shareAI-lab/learn-claude-code?style=flat&color=yellow) - Bash — всё что нужно: нано agent-харнес в стиле Claude Code с нуля.
- [gpt_academic](https://github.com/binary-husky/gpt_academic) ![](https://img.shields.io/github/stars/binary-husky/gpt_academic?style=flat&color=yellow) - 为GPT/GLM等LLM大语言模型提供实用化交互接口，特别优化论文阅读/润色/写作体验，模块化设计，支持自定义快捷按钮&函数插件，支持Python和C++等项目剖析&自译解功能，PDF/LaTex论文翻译&总结功能，支持并行问询多种LLM模型，支持chatglm3等本地模型。接入通义千问, deepseekcoder, 讯飞星火, 文心一言, llama2, rwkv, claude2, moss等。.
- [OpenSpec](https://github.com/Fission-AI/OpenSpec) ![](https://img.shields.io/github/stars/Fission-AI/OpenSpec?style=flat&color=yellow) - Spec-driven разработка (SDD) для AI-ассистентов кодинга.
- [TrendRadar](https://github.com/sansan0/TrendRadar) ![](https://img.shields.io/github/stars/sansan0/TrendRadar?style=flat&color=yellow) - AI-driven public opinion & trend monitor with multi-platform aggregation, RSS, and smart alerts. 告别信息过载，你的 AI 舆情监控助手与热点筛选工具！聚合多平台热点 + RSS 订阅，支持关键词精准筛选。AI 智能筛选新闻 + AI 翻译 + AI 分析简报直推手机，也支持接入 MCP 架构，赋能 AI 自然语言对话分析、情感洞察与趋势预测等。支持 Docker ，数据本地/云端自持。集成微信/飞书/钉钉/Telegram/邮件/ntfy/bark/slack 等渠道智能推送。.
- [context7](https://github.com/upstash/context7) ![](https://img.shields.io/github/stars/upstash/context7?style=flat&color=yellow) - Context7 — актуальная документация кода для LLM и AI-редакторов.
- [storm](https://github.com/stanford-oval/storm) ![](https://img.shields.io/github/stars/stanford-oval/storm?style=flat&color=yellow) - LLM-система курирования знаний: исследование темы и генерация статьи.
- [DeepTutor](https://github.com/HKUDS/DeepTutor) ![](https://img.shields.io/github/stars/HKUDS/DeepTutor?style=flat&color=yellow) - Agent-native персонализированный тьютор.
- [gpt-researcher](https://github.com/assafelovic/gpt-researcher) ![](https://img.shields.io/github/stars/assafelovic/gpt-researcher?style=flat&color=yellow) - Автономный агент глубоких исследований на любых LLM.
- [GLM-5](https://github.com/zai-org/GLM-5) ![](https://img.shields.io/github/stars/zai-org/GLM-5?style=flat&color=yellow) - GLM-5: от Vibe Coding к агентному инжинирингу.
- [codebase-to-course](https://github.com/zarazhangrui/codebase-to-course) ![](https://img.shields.io/github/stars/zarazhangrui/codebase-to-course?style=flat&color=yellow) - Навык Claude Code: превращает кодовую базу в интерактивный HTML-курс.
- [claude-scholar](https://github.com/Galaxy-Dawn/claude-scholar) ![](https://img.shields.io/github/stars/Galaxy-Dawn/claude-scholar?style=flat&color=yellow) - Полуавтоматический исследовательский ассистент для науки и разработки.
- [deep-research](https://github.com/u14app/deep-research) ![](https://img.shields.io/github/stars/u14app/deep-research?style=flat&color=yellow) - Глубокие исследования на любых LLM.
- [agentic-ai-prompt-research](https://github.com/Leonxlnx/agentic-ai-prompt-research) ![](https://img.shields.io/github/stars/Leonxlnx/agentic-ai-prompt-research?style=flat&color=yellow) - Исследование работы агентных AI-ассистентов кодинга.
- [apple-docs-mcp](https://github.com/kimsungwhee/apple-docs-mcp) ![](https://img.shields.io/github/stars/kimsungwhee/apple-docs-mcp?style=flat&color=yellow) - MCP-сервер документации Apple: iOS/macOS/SwiftUI, видео WWDC.

## Обучение и ресурсы

- [generative-ai-for-beginners](https://github.com/microsoft/generative-ai-for-beginners) ![](https://img.shields.io/github/stars/microsoft/generative-ai-for-beginners?style=flat&color=yellow) - GenAI для начинающих.
- [LLMs-from-scratch](https://github.com/rasbt/LLMs-from-scratch) ![](https://img.shields.io/github/stars/rasbt/LLMs-from-scratch?style=flat&color=yellow) - Реализация LLM типа ChatGPT на PyTorch с нуля, шаг за шагом.
- [llm-course](https://github.com/mlabonne/llm-course) ![](https://img.shields.io/github/stars/mlabonne/llm-course?style=flat&color=yellow) - Курс по большим языковым моделям с roadmap и Colab-ноутбуками.
- [Prompt-Engineering-Guide](https://github.com/dair-ai/Prompt-Engineering-Guide) ![](https://img.shields.io/github/stars/dair-ai/Prompt-Engineering-Guide?style=flat&color=yellow) - Гайды, статьи, ноутбуки по prompt engineering.
- [ai-agents-for-beginners](https://github.com/microsoft/ai-agents-for-beginners) ![](https://img.shields.io/github/stars/microsoft/ai-agents-for-beginners?style=flat&color=yellow) - AI-агенты для начинающих.
- [hello-agents](https://github.com/datawhalechina/hello-agents) ![](https://img.shields.io/github/stars/datawhalechina/hello-agents?style=flat&color=yellow) - 《从零开始构建智能体》——从零开始的智能体原理与实践教程.
- [BMAD-METHOD](https://github.com/bmad-code-org/bmad-method) ![](https://img.shields.io/github/stars/bmad-code-org/bmad-method?style=flat&color=yellow) - Агентная методология и IDE-промпты для полного цикла AI-разработки продукта.
- [ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch) ![](https://img.shields.io/github/stars/rohitg00/ai-engineering-from-scratch?style=flat&color=yellow) - AI-инжиниринг с нуля.
- [500-AI-Agents-Projects](https://github.com/ashishpatel26/500-AI-Agents-Projects) ![](https://img.shields.io/github/stars/ashishpatel26/500-AI-Agents-Projects?style=flat&color=yellow) - Подборка 500 кейсов AI-агентов в разных индустриях.
- [awesome-ai-agents](https://github.com/e2b-dev/awesome-ai-agents) ![](https://img.shields.io/github/stars/e2b-dev/awesome-ai-agents?style=flat&color=yellow) - Кураторский список автономных AI-агентов и агентных фреймворков.
- [awesome-generative-ai-guide](https://github.com/aishwaryanr/awesome-generative-ai-guide) ![](https://img.shields.io/github/stars/aishwaryanr/awesome-generative-ai-guide?style=flat&color=yellow) - Единый репо: GenAI-исследования, интервью, ноутбуки.
- [Hands-On-Large-Language-Models](https://github.com/HandsOnLLM/Hands-On-Large-Language-Models) ![](https://img.shields.io/github/stars/HandsOnLLM/Hands-On-Large-Language-Models?style=flat&color=yellow) - Код к книге O'Reilly «Hands-On Large Language Models».
- [vibe-coding-cn](https://github.com/2025Emma/vibe-coding-cn) ![](https://img.shields.io/github/stars/2025Emma/vibe-coding-cn?style=flat&color=yellow) - Кураторский список ресурсов по vibe coding на китайском.
- [ml-engineering](https://github.com/stas00/ml-engineering) ![](https://img.shields.io/github/stars/stas00/ml-engineering?style=flat&color=yellow) - Открытая книга по ML-инжинирингу.
- [easy-vibe](https://github.com/datawhalechina/easy-vibe) ![](https://img.shields.io/github/stars/datawhalechina/easy-vibe?style=flat&color=yellow) - Vibe coding 2026 | Your First Modern Coding course beginners to master step by step.
- [Awesome-Multimodal-Large-Language-Models](https://github.com/BradyFU/Awesome-Multimodal-Large-Language-Models) ![](https://img.shields.io/github/stars/BradyFU/Awesome-Multimodal-Large-Language-Models?style=flat&color=yellow) - Подборка по мультимодальным большим языковым моделям.
- [ai-guide](https://github.com/liyupi/ai-guide) ![](https://img.shields.io/github/stars/liyupi/ai-guide?style=flat&color=yellow) - AI-гид: ресурсы по vibe coding на китайском.
- [generative-ai](https://github.com/GoogleCloudPlatform/generative-ai) ![](https://img.shields.io/github/stars/GoogleCloudPlatform/generative-ai?style=flat&color=yellow) - Примеры кода и ноутбуки для GenAI на Google Cloud с Gemini.
- [mcp-for-beginners](https://github.com/microsoft/mcp-for-beginners) ![](https://img.shields.io/github/stars/microsoft/mcp-for-beginners?style=flat&color=yellow) - Open-source курс основ Model Context Protocol (MCP).
- [context-engineering-intro](https://github.com/coleam00/context-engineering-intro) ![](https://img.shields.io/github/stars/coleam00/context-engineering-intro?style=flat&color=yellow) - Context engineering — новый vibe coding для AI-кодинг-ассистентов.
- [open-llms](https://github.com/eugeneyan/open-llms) ![](https://img.shields.io/github/stars/eugeneyan/open-llms?style=flat&color=yellow) - Список открытых LLM, доступных для коммерческого использования.
- [awesome-generative-ai](https://github.com/steven2358/awesome-generative-ai) ![](https://img.shields.io/github/stars/steven2358/awesome-generative-ai?style=flat&color=yellow) - Кураторский список современных GenAI-проектов и сервисов.
- [LLMSurvey](https://github.com/RUCAIBox/LLMSurvey) ![](https://img.shields.io/github/stars/RUCAIBox/LLMSurvey?style=flat&color=yellow) - Страница обзора «A Survey of Large Language Models».
- [awesome-chatgpt-zh](https://github.com/EmbraceAGI/awesome-chatgpt-zh) ![](https://img.shields.io/github/stars/EmbraceAGI/awesome-chatgpt-zh?style=flat&color=yellow) - ChatGPT китайский гайд: инструкции, разработка приложений, ресурсы.
- [llm-engineer-toolkit](https://github.com/KalyanKS-NLP/llm-engineer-toolkit) ![](https://img.shields.io/github/stars/KalyanKS-NLP/llm-engineer-toolkit?style=flat&color=yellow) - Кураторский список 120+ LLM-библиотек по категориям.
- [LLMsPracticalGuide](https://github.com/Mooler0410/LLMsPracticalGuide) ![](https://img.shields.io/github/stars/Mooler0410/LLMsPracticalGuide?style=flat&color=yellow) - Кураторский список практических ресурсов по LLM.
- [anomaly-detection-resources](https://github.com/yzhao062/anomaly-detection-resources) ![](https://img.shields.io/github/stars/yzhao062/anomaly-detection-resources?style=flat&color=yellow) - Книги, статьи, видео и тулбоксы по обнаружению аномалий.
- [awesome-LLM-resources](https://github.com/WangRongsheng/awesome-LLM-resources) ![](https://img.shields.io/github/stars/WangRongsheng/awesome-LLM-resources?style=flat&color=yellow) - ‍ 全世界最好的LLM资料总结（多模态生成、Agent、辅助编程、AI审稿、数据处理、模型训练、模型推理、o1 模型、MCP、小语言模型、视觉语言模型） | Summary of the world's best LLM resources.
- [learn-ai-engineering](https://github.com/ashishps1/learn-ai-engineering) ![](https://img.shields.io/github/stars/ashishps1/learn-ai-engineering?style=flat&color=yellow) - Изучите AI и LLM с нуля по бесплатным ресурсам.
- [vibe-vibe](https://github.com/datawhalechina/vibe-vibe) ![](https://img.shields.io/github/stars/datawhalechina/vibe-vibe?style=flat&color=yellow) - AI для всех: первый систематический туториал по vibe coding.
- [awesome-ai-tools](https://github.com/mahseema/awesome-ai-tools) ![](https://img.shields.io/github/stars/mahseema/awesome-ai-tools?style=flat&color=yellow) - Кураторский список топовых AI-инструментов.
- [awesome-vibe-coding](https://github.com/filipecalegario/awesome-vibe-coding) ![](https://img.shields.io/github/stars/filipecalegario/awesome-vibe-coding?style=flat&color=yellow) - Кураторский список ресурсов по vibe coding совместно с AI.
- [vibe-coding](https://github.com/EnzeD/vibe-coding) ![](https://img.shields.io/github/stars/EnzeD/vibe-coding?style=flat&color=yellow) - Подборка ресурсов и практик по vibe coding.
- [aicodeguide](https://github.com/automata/aicodeguide) ![](https://img.shields.io/github/stars/automata/aicodeguide?style=flat&color=yellow) - AI Code Guide — roadmap для старта кодинга с AI.
- [awesome-ai-coding-tools](https://github.com/ai-for-developers/awesome-ai-coding-tools) ![](https://img.shields.io/github/stars/ai-for-developers/awesome-ai-coding-tools?style=flat&color=yellow) - Кураторский список AI-инструментов кодинга.

## AI-инфра и модельные платформы

- [ollama](https://github.com/ollama/ollama) ![](https://img.shields.io/github/stars/ollama/ollama?style=flat&color=yellow) - Запуск Kimi, GLM, DeepSeek, gpt-oss, Qwen, Gemma и др. локально.
- [transformers](https://github.com/huggingface/transformers) ![](https://img.shields.io/github/stars/huggingface/transformers?style=flat&color=yellow) - Фреймворк определения моделей для state-of-the-art ML.
- [open-webui](https://github.com/open-webui/open-webui) ![](https://img.shields.io/github/stars/open-webui/open-webui?style=flat&color=yellow) - Удобный AI-интерфейс (Ollama, OpenAI API и др.).
- [vllm](https://github.com/vllm-project/vllm) ![](https://img.shields.io/github/stars/vllm-project/vllm?style=flat&color=yellow) - Высокопроизводительный движок инференса и сервинга LLM.
- [LlamaFactory](https://github.com/hiyouga/LlamaFactory) ![](https://img.shields.io/github/stars/hiyouga/LlamaFactory?style=flat&color=yellow) - Унифицированный эффективный fine-tuning 100+ LLM и VLM (ACL 2024).
- [unsloth](https://github.com/unslothai/unsloth) ![](https://img.shields.io/github/stars/unslothai/unsloth?style=flat&color=yellow) - Веб-UI для обучения и запуска open-моделей (Gemma, Qwen, DeepSeek).
- [anything-llm](https://github.com/Mintplex-Labs/anything-llm) ![](https://img.shields.io/github/stars/Mintplex-Labs/anything-llm?style=flat&color=yellow) - Перестаньте арендовать свой интеллект.
- [llm-app](https://github.com/pathwaycom/llm-app) ![](https://img.shields.io/github/stars/pathwaycom/llm-app?style=flat&color=yellow) - Готовые облачные шаблоны для RAG, AI-пайплайнов и enterprise-поиска.
- [litellm](https://github.com/BerriAI/litellm) ![](https://img.shields.io/github/stars/BerriAI/litellm?style=flat&color=yellow) - Python SDK и прокси-сервер для 100+ LLM API в формате OpenAI.
- [LocalAI](https://github.com/mudler/LocalAI) ![](https://img.shields.io/github/stars/mudler/LocalAI?style=flat&color=yellow) - Open-source AI-движок для локального запуска.
- [milvus](https://github.com/milvus-io/milvus) ![](https://img.shields.io/github/stars/milvus-io/milvus?style=flat&color=yellow) - Высокопроизводительная cloud-native векторная БД для масштабного ANN-поиска.
- [jan](https://github.com/janhq/jan) ![](https://img.shields.io/github/stars/janhq/jan?style=flat&color=yellow) - Open-source аналог ChatGPT, работающий оффлайн на вашем компьютере.
- [ray](https://github.com/ray-project/ray) ![](https://img.shields.io/github/stars/ray-project/ray?style=flat&color=yellow) - Движок AI-вычислений.
- [quivr](https://github.com/QuivrHQ/quivr) ![](https://img.shields.io/github/stars/QuivrHQ/quivr?style=flat&color=yellow) - Opinionated RAG для интеграции GenAI в приложения.
- [Langchain-Chatchat](https://github.com/chatchat-space/Langchain-Chatchat) ![](https://img.shields.io/github/stars/chatchat-space/Langchain-Chatchat?style=flat&color=yellow) - RAG и агенты на Langchain + ChatGLM/Qwen/Llama.
- [langextract](https://github.com/google/langextract) ![](https://img.shields.io/github/stars/google/langextract?style=flat&color=yellow) - Python-библиотека извлечения структуры из текста через LLM.
- [Qwen](https://github.com/QwenLM/Qwen) ![](https://img.shields.io/github/stars/QwenLM/Qwen?style=flat&color=yellow) - Официальный репо Qwen (通义千问) — чат и предобученные LLM от Alibaba.
- [Chinese-LLaMA-Alpaca](https://github.com/ymcui/Chinese-LLaMA-Alpaca) ![](https://img.shields.io/github/stars/ymcui/Chinese-LLaMA-Alpaca?style=flat&color=yellow) - Chinese-LLaMA-Alpaca: LLaMA/Alpaca для китайского.
- [Megatron-LM](https://github.com/NVIDIA/Megatron-LM) ![](https://img.shields.io/github/stars/NVIDIA/Megatron-LM?style=flat&color=yellow) - Текущие исследования обучения трансформеров в масштабе.
- [ChatGLM2-6B](https://github.com/zai-org/ChatGLM2-6B) ![](https://img.shields.io/github/stars/zai-org/ChatGLM2-6B?style=flat&color=yellow) - ChatGLM2-6B — open-source билингвальный чат-LM.
- [outlines](https://github.com/dottxt-ai/outlines) ![](https://img.shields.io/github/stars/dottxt-ai/outlines?style=flat&color=yellow) - Структурированные выводы.
- [ggml](https://github.com/ggml-org/ggml) ![](https://img.shields.io/github/stars/ggml-org/ggml?style=flat&color=yellow) - Тензорная библиотека для машинного обучения.
- [DeepLearningExamples](https://github.com/NVIDIA/DeepLearningExamples) ![](https://img.shields.io/github/stars/NVIDIA/DeepLearningExamples?style=flat&color=yellow) - State-of-the-Art скрипты глубокого обучения, организованные по моделям.
- [litgpt](https://github.com/Lightning-AI/litgpt) ![](https://img.shields.io/github/stars/Lightning-AI/litgpt?style=flat&color=yellow) - 20+ high-performance LLMs with recipes to pretrain, finetune and deploy at scale.
- [txtai](https://github.com/neuml/txtai) ![](https://img.shields.io/github/stars/neuml/txtai?style=flat&color=yellow) - All-in-one AI-фреймворк: семантический поиск, оркестрация LLM.
- [HRM](https://github.com/sapientinc/HRM) ![](https://img.shields.io/github/stars/sapientinc/HRM?style=flat&color=yellow) - Hierarchical Reasoning Model — официальный релиз.
- [MOSS](https://github.com/OpenMOSS/MOSS) ![](https://img.shields.io/github/stars/OpenMOSS/MOSS?style=flat&color=yellow) - Open-source tool-augmented разговорная языковая модель от Fudan University.
- [promptflow](https://github.com/microsoft/promptflow) ![](https://img.shields.io/github/stars/microsoft/promptflow?style=flat&color=yellow) - Создание качественных LLM-приложений: прототип, тест, продакшн.
- [petals](https://github.com/bigscience-workshop/petals) ![](https://img.shields.io/github/stars/bigscience-workshop/petals?style=flat&color=yellow) - Запуск LLM дома, в стиле BitTorrent.
- [OpenRLHF](https://github.com/OpenRLHF/OpenRLHF) ![](https://img.shields.io/github/stars/OpenRLHF/OpenRLHF?style=flat&color=yellow) - Простой, масштабируемый и быстрый агентный RL-фреймворк на Ray (PPO и DAP).
- [PowerInfer](https://github.com/Tiiny-AI/PowerInfer) ![](https://img.shields.io/github/stars/Tiiny-AI/PowerInfer?style=flat&color=yellow) - Высокоскоростной сервинг LLM для локального деплоя.
- [deeplake](https://github.com/activeloopai/deeplake) ![](https://img.shields.io/github/stars/activeloopai/deeplake?style=flat&color=yellow) - AI Data Runtime для агентов.
- [optimate](https://github.com/nebuly-ai/optimate) ![](https://img.shields.io/github/stars/nebuly-ai/optimate?style=flat&color=yellow) - Коллекция библиотек оптимизации производительности AI-моделей.
- [osaurus](https://github.com/osaurus-ai/osaurus) ![](https://img.shields.io/github/stars/osaurus-ai/osaurus?style=flat&color=yellow) - Владейте своим AI.
- [plano](https://github.com/katanemo/plano) ![](https://img.shields.io/github/stars/katanemo/plano?style=flat&color=yellow) - AI-native прокси и дата-плоскость для агентных приложений.
- [unstract](https://github.com/Zipstack/unstract) ![](https://img.shields.io/github/stars/Zipstack/unstract?style=flat&color=yellow) - LLM-извлечение неструктурированных данных для API-деплоя и ETL.
- [bifrost](https://github.com/maximhq/bifrost) ![](https://img.shields.io/github/stars/maximhq/bifrost?style=flat&color=yellow) - Самый быстрый enterprise AI-шлюз (50x быстрее LiteLLM).
- [lemonade](https://github.com/lemonade-sdk/lemonade) ![](https://img.shields.io/github/stars/lemonade-sdk/lemonade?style=flat&color=yellow) - Lemonade — обнаружение и запуск локальных AI-приложений с оптимизированными LLM.

## Доменные AI-агенты

- [TradingAgents](https://github.com/TauricResearch/TradingAgents) ![](https://img.shields.io/github/stars/TauricResearch/TradingAgents?style=flat&color=yellow) - Мультиагентный LLM-фреймворк для финансового трейдинга.
- [daily_stock_analysis](https://github.com/ZhuLinsen/daily_stock_analysis) ![](https://img.shields.io/github/stars/ZhuLinsen/daily_stock_analysis?style=flat&color=yellow) - LLM-система анализа акций: мульти-рынок, новости, дашборд, авто-пуш.
- [OpenMontage](https://github.com/calesthio/OpenMontage) ![](https://img.shields.io/github/stars/calesthio/OpenMontage?style=flat&color=yellow) - Первая open-source агентная система видеопроизводства.
- [LibreChat](https://github.com/danny-avila/LibreChat) ![](https://img.shields.io/github/stars/danny-avila/LibreChat?style=flat&color=yellow) - Расширенный клон ChatGPT: агенты, MCP, навыки, DeepSeek, Anthropic, OpenAI.
- [FinceptTerminal](https://github.com/Fincept-Corporation/FinceptTerminal) ![](https://img.shields.io/github/stars/Fincept-Corporation/FinceptTerminal?style=flat&color=yellow) - Современное финанс-приложение: аналитика рынков, инвестиции.
- [FinGPT](https://github.com/AI4Finance-Foundation/FinGPT) ![](https://img.shields.io/github/stars/AI4Finance-Foundation/FinGPT?style=flat&color=yellow) - FinGPT — open-source финансовые большие языковые модели.
- [machine-learning-for-trading](https://github.com/stefan-jansen/machine-learning-for-trading) ![](https://img.shields.io/github/stars/stefan-jansen/machine-learning-for-trading?style=flat&color=yellow) - Код к «Machine Learning for Trading», 3-е издание.
- [xiaohongshu-mcp](https://github.com/xpzouying/xiaohongshu-mcp) ![](https://img.shields.io/github/stars/xpzouying/xiaohongshu-mcp?style=flat&color=yellow) - MCP для xiaohongshu.com.
- [ai-berkshire](https://github.com/xbtlin/ai-berkshire) ![](https://img.shields.io/github/stars/xbtlin/ai-berkshire?style=flat&color=yellow) - Berkshire эпохи AI: фреймворк стоимостного инвестирования на Claude Code/Codex.
- [QuantDinger](https://github.com/brokermr810/QuantDinger) ![](https://img.shields.io/github/stars/brokermr810/QuantDinger?style=flat&color=yellow) - AI-платформа количественного трейдинга crypto/акций/форекс.
- [FinRobot](https://github.com/AI4Finance-Foundation/FinRobot) ![](https://img.shields.io/github/stars/AI4Finance-Foundation/FinRobot?style=flat&color=yellow) - FinRobot — open-source AI-агент для финансового анализа на LLM.
- [claude-ads](https://github.com/AgriciDaniel/claude-ads) ![](https://img.shields.io/github/stars/AgriciDaniel/claude-ads?style=flat&color=yellow) - Навык аудита и оптимизации платной рекламы для Claude Code.
- [FinanceToolkit](https://github.com/JerBouma/FinanceToolkit) ![](https://img.shields.io/github/stars/JerBouma/FinanceToolkit?style=flat&color=yellow) - Прозрачный и эффективный финансовый анализ.
- [arc-kit](https://github.com/tractorjuice/arc-kit) ![](https://img.shields.io/github/stars/tractorjuice/arc-kit?style=flat&color=yellow) - Харнес архитектурного управления предприятием: стратегия, архитектура, доставка.
- [aso-skills](https://github.com/Eronred/aso-skills) ![](https://img.shields.io/github/stars/Eronred/aso-skills?style=flat&color=yellow) - AI-навыки для App Store Optimization (ASO) и маркетинга приложений.
- [ai-legal-claude](https://github.com/zubair-trabzada/ai-legal-claude) ![](https://img.shields.io/github/stars/zubair-trabzada/ai-legal-claude?style=flat&color=yellow) - AI-юридический ассистент — навык для Claude Code.
- [mathcode](https://github.com/math-ai-org/mathcode) ![](https://img.shields.io/github/stars/math-ai-org/mathcode?style=flat&color=yellow) - Frontier математический кодинг-агент.

## Требует ревью

- [ChatTTS](https://github.com/2noise/ChatTTS) ![](https://img.shields.io/github/stars/2noise/ChatTTS?style=flat&color=yellow) - Генеративная модель речи для повседневных диалогов.
- [FunASR](https://github.com/modelscope/FunASR) ![](https://img.shields.io/github/stars/modelscope/FunASR?style=flat&color=yellow) - Industrial-grade распознавание речи: 170x realtime, 50+ языков.
- [gemini-voyager](https://github.com/Nagi-ovo/gemini-voyager) ![](https://img.shields.io/github/stars/Nagi-ovo/gemini-voyager?style=flat&color=yellow) - All-in-one набор улучшений для Google Gemini и AI Studio.
- [nuclear](https://github.com/nukeop/nuclear) ![](https://img.shields.io/github/stars/nukeop/nuclear?style=flat&color=yellow) - Стриминговый музыкальный плеер, находящий свободную музыку.
- [CVPR2024-Paper-Code-Interpretation](https://github.com/extreme-assistant/CVPR2024-Paper-Code-Interpretation) ![](https://img.shields.io/github/stars/extreme-assistant/CVPR2024-Paper-Code-Interpretation?style=flat&color=yellow) - Подборка статей/кода/разборов CVPR 2024.
- [XHS-Downloader](https://github.com/JoeanAmier/XHS-Downloader) ![](https://img.shields.io/github/stars/JoeanAmier/XHS-Downloader?style=flat&color=yellow) - Загрузчик контента Xiaohongshu (RedNote).
- [xiaozhi-esp32-server](https://github.com/xinnan-tech/xiaozhi-esp32-server) ![](https://img.shields.io/github/stars/xinnan-tech/xiaozhi-esp32-server?style=flat&color=yellow) - 本项目为xiaozhi-esp32提供后端服务，帮助您快速搭建ESP32设备控制服务器。Backend service for xiaozhi-esp32, helps you quickly build an ESP32 device control server.
- [VAR](https://github.com/FoundationVision/VAR) ![](https://img.shields.io/github/stars/FoundationVision/VAR?style=flat&color=yellow) - Визуальное авторегрессионное моделирование — предсказание следующего масштаба для генерации изображений.
- [ICCV2023-Paper-Code-Interpretation](https://github.com/extreme-assistant/ICCV2023-Paper-Code-Interpretation) ![](https://img.shields.io/github/stars/extreme-assistant/ICCV2023-Paper-Code-Interpretation?style=flat&color=yellow) - Подборка статей/кода/разборов ICCV 2023/2021/2019/2017.
- [natively-cluely-ai-assistant](https://github.com/Natively-AI-assistant/natively-cluely-ai-assistant) ![](https://img.shields.io/github/stars/Natively-AI-assistant/natively-cluely-ai-assistant?style=flat&color=yellow) - Free open-source AI-ассистент встреч, интервью и заметок.
- [deepseek_ocr_app](https://github.com/rdumasia303/deepseek_ocr_app) ![](https://img.shields.io/github/stars/rdumasia303/deepseek_ocr_app?style=flat&color=yellow) - Быстрое vibe-coded приложение для DeepSeek OCR.
- [global-stock-data](https://github.com/simonlin1212/global-stock-data) ![](https://img.shields.io/github/stars/simonlin1212/global-stock-data?style=flat&color=yellow) - 美股港股全栈数据工具包 (AI Skill) — 7层架构 · 17端点 · 5数据源 · 零鉴权 | US & HK Stock Full-Stack Data Toolkit for AI Coding Assistants.

## Контрибьютинг

Нашли классный инструмент или сделали свой? Добавьте через Pull Request — правила см. в CONTRIBUTING.md (одна утилита на PR, живой репозиторий, нейтральное описание). Число звёзд обновляется автоматически раз в сутки через GitHub Action. Лицензия CC0-1.0.
