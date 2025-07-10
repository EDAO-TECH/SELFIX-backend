#!/bin/bash

echo "🔪 Cleaning duplicate uvicorn processes..."

# Get all uvicorn processes except the parent
PIDS=$(pgrep -f "uvicorn" | tail -n +2)

if [ -n "$PIDS" ]; then
  echo "Killing duplicate uvicorn PIDs: $PIDS"
  kill -9 $PIDS
else
  echo "✅ No duplicate uvicorn processes found."
fi
