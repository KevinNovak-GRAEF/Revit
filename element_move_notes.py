columns = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralColumns).WhereElementIsNotElementType().ToElements()
framing = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()
beam_location = framing[0].Location
column_location = columns[0].Location #.point for current location
new_beam_location_start = XYZ(10,10,0)
new_beam_location_end = XYZ(25,20,0)
new_column_location = XYZ(20,20,0)

line = Line.CreateBound(new_beam_location_start, new_beam_location_end)

TransactionManager.Instance.EnsureInTransaction(doc)

beam_location.Curve = line
# For vector move
# ElementTransformUtils.MoveElement(doc, columns[0].Id, new_column_location)
column_location.Point = new_column_location

TransactionManager.Instance.TransactionTaskDone()
