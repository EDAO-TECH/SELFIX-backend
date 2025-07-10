import os
import time
import requests
import pyinotify

WATCHED_FILE = "/etc/hosts"
SCAN_API_URL = "http://localhost:8080/api/scan"

class EventHandler(pyinotify.ProcessEvent):
    def process_default(self, event):
        print(f"Change detected: {event.maskname} on {event.pathname}")
        try:
            response = requests.post(SCAN_API_URL)
            print(f"Triggered scan: {response.status_code} - {response.text}")
        except Exception as e:
            print(f"Error triggering scan: {e}")

def main():
    wm = pyinotify.WatchManager()
    handler = EventHandler()
    notifier = pyinotify.Notifier(wm, handler)

    mask = pyinotify.ALL_EVENTS
    wm.add_watch(WATCHED_FILE, mask)

    print("🔍 Monitoring started. Watching for changes to:", WATCHED_FILE)
    notifier.loop()

if __name__ == "__main__":
    main()
