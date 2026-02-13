@echo off
set ANTHROPIC_BASE_URL=http://localhost:8080
set ANTHROPIC_API_KEY=YOUR_ANTHROPIC_API_KEY_HERE
echo Starting Claude Code via Proxy...
"C:\Program Files\nodejs\npx.cmd" -y @anthropic-ai/claude-code %*
