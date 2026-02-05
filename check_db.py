from app.database import supabase
import sys

def check():
    print(f"Checking connection to: {supabase.url}")
    try:
        # Try to select from workflows (limit 1 just to check existence/permission)
        response = supabase.table("workflows").select("*").limit(1).execute()
        print("✅ SUCCESS: Connected to Supabase and found 'workflows' table.")
        print(f"Rows found: {len(response.data) if response.data else 0}")
    except Exception as e:
        print("❌ ERROR: Connection failed or table not found.")
        print("This confirms the table does not exist in your Supabase project yet.")
        print(f"Details: {e}")
        # sys.exit(1)

if __name__ == "__main__":
    check()
