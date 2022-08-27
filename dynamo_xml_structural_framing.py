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
tree = ET.parse(r'D:\Professional\XML\Structural Framing.xml')
root = tree.getroot()

paraList = []

for ch in root:
    for c in ch:
        paraList.append(c.tag)
    
# Get the structural framing member
struFrame = FilteredElementCollector(doc)
id = struFrame.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElementIds()
elmnt = struFrame.OfCategory(BuiltInCategory.OST_StructuralFraming).WhereElementIsNotElementType().ToElements()


testDic = {
            "W8x10":{"Keynote": "TestKeynoteOne",
                    "Model": "TestModelOne",
                    "Manufacturer":"TestManufacturerOne",
                    "TypeComments":"TestCommentsOne",
                    "Description":"TestDescriptionOne"},
            "B1":{"Keynote": "TestKeynoteTwo",
                    "Model": "TestModelTwo",
                    "Manufacturer":"TestManufacturerTwo",
                    "TypeComments":"TestCommentsTwo",
                    "Description": "TestDescriptionTwo"}
            }
            
typeName = []


for e in elmnt:
    elmntType = doc.GetElement(e.GetTypeId())
    elmntName = e.Name
    
    try:
        for pl in paraList:
            newParaValue = testDic[elmntName][pl]
            paraDes = elmntType.GetParameters(pl)
            for p in paraDes:
                p.Set(newParaValue)
    except:
        TaskDialog.Show("Element not in List",elmntName)
        
    typeName.append(elmntName)

TransactionManager.Instance.TransactionTaskDone()

OUT = typeName