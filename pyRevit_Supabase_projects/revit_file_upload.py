import os
from datetime import datetime, timezone  # <-- Standard library goes here

from dotenv import load_dotenv
from supabase import create_client, Client  # <-- Third-party libraries below


load_dotenv()


#--- Settings from .env ---
url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
email = os.environ.get("SUPABASE_EMAIL")      # looks up the name in .env
password = os.environ.get("SUPABASE_PASSWORD")


#---Connect and sign in---
supabase: Client = create_client(url, key)
response = supabase.auth.sign_in_with_password(
    {
        "email": email,
        "password": password,
    }
)
user_id = response.user.id

# --- CONFIG ---

LOCAL_FILE_PATH = "C:\\Users\\b902w\\Downloads\\racadvancedsampleproject.0001.rvt"
BUCKET_NAME = "revit-files"
DESTINATION_FILE_NAME = "racadvancedsampleproject.0001.rvt"
PROJECT_NAME = "Commercial Project"
upload_path = f"{user_id}/{DESTINATION_FILE_NAME}"  # Path in Supabase Storage


# --- STEP 1: Upload the Revit file to Supabase Storage ---
# STEP 1: Upload the Revit file to Supabase Storage
with open(LOCAL_FILE_PATH, "rb") as f:  # <--- Changed "r" to "rb"
    upload_response = supabase.storage.from_(BUCKET_NAME).upload(
        path=upload_path,
        file=f,
        file_options={
            "content-type": "application/octet-stream",
            "upsert": "true"  # <--- Changed "true" to True
        }
    )

print("Upload response:", upload_response)

# --- STEP 2: Get the public URL ---
public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(upload_path)
print("Public URL:", public_url)

# --- STEP 3: Insert metadata into revit_models ---
insert_response = supabase.table("revit_models").insert({
    "project_name": PROJECT_NAME,
    "storage_path": public_url,
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "status": "pending"
}).execute()

print("DB insert response:", insert_response)