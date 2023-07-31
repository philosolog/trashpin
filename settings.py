import pathlib
import os
from dotenv import load_dotenv

load_dotenv()

if pathlib.Path("alternate.env"):
	load_dotenv(pathlib.Path("alternate.env"))

token = os.getenv("token_alternate") or os.getenv("token")
uid = os.getenv("uid_alternate") or os.getenv("uid")
base_directory = pathlib.Path(__file__).parent
cogs_directory = base_directory / "cogs"