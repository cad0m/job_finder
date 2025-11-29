from pathlib import Path
from dotenv import load_dotenv
import os

# Resolve project root (one level up from package folder)
PROJECT_ROOT = Path(__file__).resolve().parents[1]
env_path = PROJECT_ROOT / ".env"

# Only load if .env exists
if env_path.exists():
    load_dotenv(env_path)