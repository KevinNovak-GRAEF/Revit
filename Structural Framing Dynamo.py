import clr

clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB.Structure import *

clr.AddReference('RevitAPIUI')
from Autodesk.Revit.UI import *

clr.AddReference('System')
from System.Collections.Generic import List

clr.AddReference('RevitNodes')
import Revit
clr.ImportExtensions(Revit.GeometryConversion)
clr.ImportExtensions(Revit.Elements)

clr.AddReference('RevitServices')
import RevitServices
from RevitServices.Persistence import DocumentManager
from RevitServices.Transactions import TransactionManager

import xml.etree.ElementTree as ET

doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

#Preparing input from dynamo to revit
element = UnwrapElement(IN[0])


#Do some action in a Transaction
TransactionManager.Instance.EnsureInTransaction(doc)
 
# Parameters from XML
tree = ET.parse(r'D:\Professional\XML\Structural Framing Dynamo Update.xml')
root = tree.getroot()

paraTag = []
paraValue = []
paraList = []

for ch in root:
    for c in ch:
        paraTag.append(c.tag)
        paraValue.append(c.text)
        paraList.append(c.get('parameter'))
        
typeMark = root.find('TypeName').text
    
# Get the structural framing member
struFrame = FilteredElementCollector(doc)
id = struFrame.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElementIds()
elmnt = struFrame.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()

for e in elmnt:
    elmntType = doc.GetElement(e.GetTypeId())
    elmntName = e.Name
    
    if elmntName == typeMark:
        for pl, pv in zip (paraList, paraValue):
            paraDes = elmntType.GetParameters(pl)
            for p in paraDes:
                p.Set(pv)

TransactionManager.Instance.TransactionTaskDone()

OUT = paraTag, paraValue, paraList, typeMark