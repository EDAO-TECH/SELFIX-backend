#!/bin/bash
echo "🌙 Starting nightly AI digestion..."

# Log timestamp
NOW=$(date '+%Y-%m-%d %H:%M:%S')
echo "🕒 Night Session Started: $NOW" >> /opt/SELFIX/logs/digestion.log

# Run both theory and practical
python3 /opt/SELFIX/ai_tower/study_manager.py theory >> /opt/SELFIX/logs/digestion.log
python3 /opt/SELFIX/ai_tower/study_manager.py practical >> /opt/SELFIX/logs/digestion.log

echo "✅ Night session complete."
