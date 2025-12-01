import os
from pathlib import Path

BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "input"
LOG_FILE = BASE_DIR / "log.log"

MODEL_NAME = "llama3.2:1b" 
TIMEOUT = 23
MAX_RETRIES = 5
BACKOFF = 2
 