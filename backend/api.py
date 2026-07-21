"""Compatibility facade for the Flask REST API."""

from pathlib import Path
import sys
import logging

logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stdout, force=True)

CURRENT_DIR = Path(__file__).resolve().parent
PARENT_DIR = CURRENT_DIR.parent
sys.path = [entry for entry in sys.path if entry not in {"", str(CURRENT_DIR)}]
if str(PARENT_DIR) not in sys.path:
    sys.path.insert(0, str(PARENT_DIR))

from backend.http.app_factory import create_app

app, socketio, orchestrator = create_app()
logging.getLogger("genia.api").info("GenIA backend entrypoint initialized")

if __name__ == "__main__":
    logging.getLogger("genia.api").info("Starting Flask server on port 5000")
    app.run(host="0.0.0.0", port=5000, use_reloader=False)
