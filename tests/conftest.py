import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
# The project imports modules as top-level packages (utils, tools, agent, ...)
# and reads config/config.yaml with a relative path, so run from the repo root.
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

# Dummy keys so tool classes can be constructed without real credentials.
for key in ["GROQ_API_KEY", "OPENAI_API_KEY", "GPLACES_API_KEY", "TAVILY_API_KEY",
            "OPENWEATHERMAP_API_KEY", "EXCHANGE_RATE_API_KEY"]:
    os.environ.setdefault(key, "test-key")
