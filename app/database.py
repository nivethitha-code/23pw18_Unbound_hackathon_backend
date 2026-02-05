import os
import httpx
import logging
from dotenv import load_dotenv

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

if not url or not key:
    raise ValueError("SUPABASE_URL and SUPABASE_KEY must be set in .env")

logger = logging.getLogger(__name__)

class SupabaseResponse:
    def __init__(self, data):
        self.data = data

class SupabaseQueryBuilder:
    def __init__(self, base_url, headers, table):
        self.url = f"{base_url}/rest/v1/{table}"
        self.headers = headers
        self.params = {}
        self.method = "GET"
        self.json_data = None

    def select(self, columns="*"):
        self.method = "GET"
        self.params["select"] = columns
        return self

    def eq(self, column, value):
        # PostgREST uses column=eq.value
        self.params[column] = f"eq.{value}"
        return self

    def insert(self, data):
        self.method = "POST"
        self.headers["Prefer"] = "return=representation"
        self.json_data = data
        return self

    def update(self, data):
        self.method = "PATCH"
        self.headers["Prefer"] = "return=representation"
        self.json_data = data
        return self
    
    def order(self, column, desc=False):
        order = "desc" if desc else "asc"
        self.params["order"] = f"{column}.{order}"
        return self
    
    def limit(self, count):
        self.headers["Range-Unit"] = "items"
        self.headers["Range"] = f"0-{count-1}"
        return self

    def execute(self):
        try:
             with httpx.Client(timeout=10.0) as client:
                if self.method == "GET":
                     r = client.get(self.url, headers=self.headers, params=self.params)
                elif self.method == "POST":
                     r = client.post(self.url, headers=self.headers, json=self.json_data, params=self.params)
                elif self.method == "PATCH":
                     r = client.patch(self.url, headers=self.headers, json=self.json_data, params=self.params)
                
                if r.status_code >= 400:
                    logger.error(f"Supabase Error: {r.text}")
                    r.raise_for_status()
                
                return SupabaseResponse(r.json())
        except Exception as e:
            logger.error(f"Database operation failed: {e}")
            raise e

class SupabaseClient:
    def __init__(self, url, key):
        self.url = url
        self.headers = {
            "apikey": key,
            "Authorization": f"Bearer {key}",
            "Content-Type": "application/json"
        }

    def table(self, name):
         return SupabaseQueryBuilder(self.url, self.headers.copy(), name)

# Initialize the client
supabase = SupabaseClient(url, key)
