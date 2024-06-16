import os
from dotenv import load_dotenv


UTILS_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.dirname(UTILS_DIR)

dotenv_path = os.path.join(ROOT_DIR, ".env")

if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)


# QDRANT

QDRANT_URL = os.environ.get("QDRANT_URL", None )
QDRANT_API_KEY = os.environ.get("QDRANT_PASSWORD", None)
QDRANT_COLLECTION = os.environ.get("QDRANT_COLLECTION", None)


# DATABASE

DB_CONNECTION_STRING = os.getenv("DB_CONNECTION_STRING")

# OPENAI
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

