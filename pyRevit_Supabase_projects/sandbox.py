import os
from dotenv import load_dotenv
from supabase import create_client, Client
from datetime import datetime, timezone

load_dotenv()

url = os.environ.get("SUPABASE_URL")
key = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

# --- CONFIG ---
LOCAL_FILE_PATH = "C:\\Users\\b902w\\Downloads\\racadvancedsampleproject.0001.rvt"
BUCKET_NAME = "revit-files"
DESTINATION_FILE_NAME = "racadvancedsampleproject.0001.rvt"
PROJECT_NAME = "Commercial Project"

# --- STEP 1: Upload the Revit file to Supabase Storage ---
with open(LOCAL_FILE_PATH, "rb") as f:
    upload_response = supabase.storage.from_(BUCKET_NAME).upload(
        path=DESTINATION_FILE_NAME,
        file=f,
        file_options={
            "content-type": "application/octet-stream",
            "upsert": "true"
        },
    )
print("Upload response:", upload_response)

# --- STEP 2: Get the public URL ---
public_url = supabase.storage.from_(BUCKET_NAME).get_public_url(DESTINATION_FILE_NAME)
print("Public URL:", public_url)

# --- STEP 3: Insert metadata into revit_models ---
insert_response = supabase.table("revit_models").insert({
    "project_name": PROJECT_NAME,
    "storage_path": public_url,
    "last_updated": datetime.now(timezone.utc).isoformat(),
    "status": "pending"
}).execute()

print("DB insert response:", insert_response)