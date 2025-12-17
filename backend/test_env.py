"""
This file tests that our environment variables load correctly.
"""

from dotenv import load_dotenv
import os

load_dotenv()

db_url = os.getenv("DATABASE_URL")

print("Database URL:", db_url)
