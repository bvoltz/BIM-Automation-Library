import os
from supabase import create_client
from dotenv import load_dotenv

load_dotenv()

# Load your credentials
supabase = create_client(
    os.environ.get("SUPABASE_URL"),
    os.environ.get("SUPABASE_KEY")
)

# Test with sample insert
data = {
    'project_name': 'Test Project',
    'storage_path': 'models/test.rvt',
    'last_updated': '2026-10-31-T00:00:00Z'
}
response = supabase.table('revit_models').insert(data).execute()
print(response)