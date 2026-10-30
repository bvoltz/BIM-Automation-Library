# -*- coding: utf-8 -*-
import Autodesk.Revit.DB as DB

# The basic anatomy of a Collector requires:
# 1. Passing the 'doc' (current document)
# 2. Applying filters (Class, Category, View, or Type limits)
# 3. Finalizing with .ToElements() to turn it into a clean Python list


# --- 1. COLLECT BY CATEGORY (Instances only) ---
# Perfect for Doors, Furniture, Windows, Columns, etc.
door_instances = DB.FilteredElementCollector(doc) \
                .OfCategory(DB.BuiltInCategory.OST_Doors) \
                .WhereElementIsNotElementType() \
                .ToElements()


# --- 2. COLLECT BY CLASS ---
# Perfect for structural elements like Views, Levels, Sheets, or Walls
all_views = DB.FilteredElementCollector(doc) \
            .OfClass(DB.View) \
            .ToElements()


# --- 3. COLLECT ONLY WITHIN THE ACTIVE VIEW ---
# Limits your search to what is visible right now in your current view
furniture_in_view = DB.FilteredElementCollector(doc, doc.ActiveView.Id) \
                    .OfCategory(DB.BuiltInCategory.OST_Furniture) \
                    .WhereElementIsNotElementType() \
                    .ToElements()


# --- 4. COLLECT FAMILY TYPES (Symbols) ---
# Use this when you want to look at or change a Type Parameter instead of an Instance
door_types = DB.FilteredElementCollector(doc) \
            .OfCategory(DB.BuiltInCategory.OST_Doors) \
            .WhereElementIsElementType() \
            .ToElements()
