# /opt/SELFIX/mini_panel.py

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse, JSONResponse
from pathlib import Path
import json

app = FastAPI()

REPORT_DIR = Path("/opt/SELFIX/reports")
JOURNAL_PATH = Path("/opt/SELFIX/data/ai_journal.json")

def load_latest_report():
    reports = sorted(REPORT_DIR.glob("precheck_report_*.json"), reverse=True)
    if not reports:
        return [], "⚠️ No reports available"
    data = json.loads(reports[0].read_text())
    status = "✅ All Systems Operational" if all(d.get("status") == "pass" for d in data) else "⚠️ Issues Detected"
    return data, status

def call_local_ai(message: str, agent_id: str):
    # Placeholder: you can wire to actual AI logic here
    journal_entry = {
        "agent_id": agent_id,
        "query": message,
        "response": f"[Local AI Response Placeholder] You said: {message}"
    }

    # Append to journal
    if JOURNAL_PATH.exists():
        try:
            journal = json.loads(JOURNAL_PATH.read_text())
            if isinstance(journal, list):
                journal.append(journal_entry)
            else:
                journal = [journal, journal_entry]
        except:
            journal = [journal_entry]
    else:
        journal = [journal_entry]
    
    JOURNAL_PATH.write_text(json.dumps(journal, indent=2))
    return journal_entry["response"]

@app.get("/panel/{agent_id}", response_class=HTMLResponse)
def customer_dashboard(agent_id: str):
    report, status_msg = load_latest_report()
    color = "#4CAF50" if "✅" in status_msg else "#f44336"

    html = f"<html><head><title>SELFIX Panel</title></head><body>"
    html += f"<h1 style='color:{color}'>SELFIX System Status for {agent_id}</h1><p>{status_msg}</p>"

    html += f"<form method='post' action='/panel/{agent_id}/chat'>"
    html += f"<input type='text' name='message' placeholder='Ask SELFIX AI...' required style='width:60%;'/>"
    html += f"<input type='submit' value='Ask AI'/></form><hr><ul>"

    for item in report:
        item_color = "#4CAF50" if item["status"] == "pass" else "#f44336"
        html += f"<li><b>{item['check']}</b>: <span style='color:{item_color}'>{item['status']}</span></li>"

    html += "</ul><p><a href='/panel/{agent_id}/report'>Download Report (JSON)</a></p></body></html>"
    return HTMLResponse(content=html)

@app.post("/panel/{agent_id}/chat", response_class=HTMLResponse)
async def chat_ai(agent_id: str, message: str = Form(...)):
    ai_reply = call_local_ai(message, agent_id)
    html = f"<h2>SELFIX AI Says:</h2><p>{ai_reply}</p><a href='/panel/{agent_id}'>⬅️ Back to panel</a>"
    return HTMLResponse(content=html)

@app.get("/panel/{agent_id}/report", response_class=JSONResponse)
def download_report(agent_id: str):
    report, _ = load_latest_report()
    return JSONResponse(content={"agent": agent_id, "report": report})
