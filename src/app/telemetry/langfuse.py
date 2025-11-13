from dotenv import load_dotenv
from langfuse import get_client

load_dotenv()
langfuse_client = get_client()
try:
    print("Langfuse auth OK:", langfuse_client.auth_check())
except Exception as e:
    print("Langfuse auth FAILED:", e)
