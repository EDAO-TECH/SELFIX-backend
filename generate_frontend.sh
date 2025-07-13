#!/bin/bash
cd /opt/SELFIX
source venv/bin/activate  # activate Python env if needed
python3 local_ai.py >> logs/frontend_gen.log 2>&1
