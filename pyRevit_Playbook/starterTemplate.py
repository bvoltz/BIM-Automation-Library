import Autodesk.Revit.DB as DB
import Autodesk.Revit.UI as UI
from pyrevit import script, forms

# Set up environment variables
uidoc = __revit__.ActiveUIDocument
doc = uidoc.Document
output = script.get_output()

# Your code starts here...
print("Hello Revit!")
