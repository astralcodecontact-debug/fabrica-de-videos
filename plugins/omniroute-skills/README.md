# OmniRoute Skills

A single plugin bundling 47 agent skills so Claude can use them on demand:

- **46 OmniRoute skills** from [`diegosouzapw/OmniRoute`](https://github.com/diegosouzapw/OmniRoute), an MIT-licensed local AI gateway. These cover the OmniRoute API and CLI: provider management, routing combos and fallback chains (19 strategies), API keys and budgets, usage logs, token compression, caching, resilience, tunnels, backups, MCP and A2A access, and CLI setup. API skills target the local OmniRoute server at `https://localhost:20128` using a local bearer token.
- **claude-mem** from [`TerminalSkills/skills`](https://github.com/TerminalSkills/skills/tree/main/skills/claude-mem), a guide to adding persistent memory to Claude Code across sessions (covers `claude-mem` and Claude Subconscious).

## Notes

- These skills are documentation/reference skills authored by third parties. They were scanned before bundling: every OmniRoute command targets the local server on `localhost:20128`, with no external network calls or credential reads; claude-mem is documentation only. As with any skill, review before relying on it, since skills run with full agent permissions.
- Skill authors are third parties whose reputation was not independently verified.
- The `ponytail` skill is an unrelated coding-style skill (`DietrichGebert/ponytail`) that ships inside the OmniRoute repo and is included for completeness.

## Skills included

Routing & providers: `omni-providers`, `omni-models`, `omni-combos-routing`, `omni-inference`, `omni-resilience`, `omni-proxies`, `omni-tunnels`
Keys, budgets, usage: `omni-api-keys`, `omni-budget`, `omni-usage-logs`, `omni-settings`
Efficiency: `omni-compression`, `omni-context-rtk`, `omni-cache`
Integration: `omni-mcp`, `omni-agents-a2a`, `omni-webhooks`, `omni-sync-cloud`, `omni-db-backups`, `omni-version-manager`, `omni-cli-tools`, `omni-github-skills`, `omni-auth`
CLI: `cli-setup`, `cli-serve`, `cli-health`, `cli-providers`, `cli-keys`, `cli-models`, `cli-chat`, `cli-routing`, `cli-resilience`, `cli-compression`, `cli-contexts`, `cli-cost-usage`, `cli-mcp`, `cli-a2a`, `cli-tunnel`, `cli-backup-sync`, `cli-policy-audit`, `cli-batches`, `cli-eval`, `cli-plugins-skills`, `cli-skill-collector`, `config-codex-cli`
Memory: `claude-mem`
Other: `ponytail`
