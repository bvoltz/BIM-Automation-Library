import os

from dotenv import load_dotenv
from supabase import create_client

load_dotenv()

# --- Settings from .env ---
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
email_a = os.environ.get("SUPABASE_EMAIL")
password_a = os.environ.get("SUPABASE_PASSWORD")
email_b = os.environ.get("SUPABASE_EMAIL_B")
password_b = os.environ.get("SUPABASE_PASSWORD_B")


# --- Test 1: User A can see their own rows ---
client_a = create_client(url, key)
client_a.auth.sign_in_with_password({"email": email_a, "password": password_a})
rows_a = client_a.table("revit_models").select("*").execute()
print("Test 1 - User A sees", len(rows_a.data), "rows (expected: more than 0)")


# --- Test 2: User B can't see User A's rows ---
client_b = create_client(url, key)
client_b.auth.sign_in_with_password({"email":email_b, "password": password_b})
rows_b = client_b.table("revit_models").select("*").execute()
print("Test 2 - User B sees", len(rows_b.data), "rows (expected: 0)")


# --- Test 3: Not signed in = can't insert ---
client_anon = create_client(url, key)
# Note: no sign-in on purpose
try:
    client_anon.table("revit_models").insert({
        "project_name": "Should Fail",
        "status": "pending",
    }).execute()
    print("Test 3 - FAILED: anonymous insert was allowed!")
except Exception as e:
    print("Test 3 - Blocked as expected:", e)