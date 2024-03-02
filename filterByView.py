ColumnCategory = BuiltInCategory.OST_StructuralColumns

ViewParam = BuiltInParameter.VIEW_NAME
viewProvider = ParameterValueProvider(ElementId(ViewParam))
viewEvaluator = FilterStringEquals()
viewRule = FilterStringRule(viewProvider, viewEvaluator, "RVT_IFC")
viewFilter = ElementParameterFilter(viewRule)

viewIFC = FilteredElementCollector(doc).OfClass(View3D).WherePasses(viewFilter).FirstElementId()

columns = FilteredElementCollector(doc, viewIFC).OfCategory(ColumnCategory).WhereElementIsNotElementType().ToElements()

# PickObject(s) use list for objects
reference = uidoc.Selection.PickObjects(Selection.ObjectType.Element)
elmntList = []
for ref in reference:
    elmnt = doc.GetElement(ref)
    elmntList.append(elmnt)

# PickElementsByRectangle
reference = uidoc.Selection.PickElementsByRectangle()
