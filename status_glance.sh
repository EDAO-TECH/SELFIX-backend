#!/bin/bash

echo "🔎 SELFIX Live System Glance"
echo "=============================="

cpu=$(ps -A -o %cpu | awk '{s+=$1} END {print s}')
mem=$(vm_stat | awk '/Pages active/ {a=$3} /Pages wired/ {w=$3} /Pages free/ {f=$3} END {u=a+w; t=u+f; printf "%.1f", (u/t)*100}')

echo "🧠 CPU: $cpu% | 🧠 MEM: $mem%"

ip=$(curl -s ifconfig.me)
echo "🌍 External IP: $ip"

# FastAPI check
fastapi_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health)
echo "⚙️ FastAPI: $fastapi_status"

# GPT API check
gpt_status=$(curl -s -o /dev/null -w "%{http_code}" http://localhost:8825/api/karma-score -H "Stripe-Token: test")
echo "🤖 GPT API: $gpt_status"

# Healing Daemon check
if pgrep -f "daemon_loop.py" > /dev/null; then
    echo "🧬 Healing Daemon: ✅ Running"
else
    echo "🧬 Healing Daemon: ❌ Not Running"
fi

echo "=============================="
