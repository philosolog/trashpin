"""Configuration settings for the Trashpin Discord bot.

Loads environment variables from .env file.
"""

import logging
import os
import sys
from pathlib import Path
from dotenv import load_dotenv

logger = logging.getLogger(__name__)

load_dotenv()

# Support alternate/debug tokens
if Path("alternate.env").exists():
	load_dotenv(Path("alternate.env"))

token: str | None = os.getenv("token_debug") or os.getenv("token_alternate") or os.getenv("token")

if not token:
	logger.error("Bot token not found in environment variables.")
	logger.error("Please set 'token' in your .env file.")
	sys.exit(1)

uid: str | None = os.getenv("uid_debug") or os.getenv("uid_alternate") or os.getenv("uid")
base_directory: Path = Path(__file__).parent
cogs_directory: Path = base_directory / "cogs"
guilds_directory: str = "databases/guilds.db"