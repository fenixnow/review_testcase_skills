"""Конфигурация pytest для тестов Langfuse."""

import os
from pathlib import Path
from dotenv import load_dotenv

# Загружаем .env из директории langfuse
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(env_path)

