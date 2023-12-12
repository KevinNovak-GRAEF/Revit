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

doc = DocumentManager.Instance.CurrentDBDocument
uidoc=DocumentManager.Instance.CurrentUIApplication.ActiveUIDocument

ROUNDTO = 7

#Preparing input from dynamo to revit
element = UnwrapElement(IN[0])

filterBrace = ElementStructuralTypeFilter(Structure.StructuralType.Brace)

structuralFraming = FilteredElementCollector(doc).OfCategory(BuiltInCategory.OST_StructuralFraming)

bracing = FilteredElementCollector(doc).WherePasses(filterBrace).WhereElementIsNotElementType().ToElementIds()

idsBracing = List[ElementId]()
for brace in bracing:
    idsBracing.Add(brace)

beams = structuralFraming.Excluding(idsBracing).WhereElementIsNotElementType().ToElements()

placementCheck = []

for beam in beams:
    data = {}
    origin = {}
    startPoint = {}
    endPoint = {}
    id = beam.Id
    locationCurve = beam.Location.Curve
    locationOrigin = locationCurve.Origin
    
    # Origin
    originX = round(locationOrigin.X, ROUNDTO)
    absOriginX = abs(originX)
    origin["X"] = originX
    originY = round(locationOrigin.Y, ROUNDTO)
    absOriginY = abs(originY)
    origin["Y"] = originY
    originZ = round(locationOrigin.Z, ROUNDTO)
    origin["Z"] = originZ
    absOriginZ = abs(originZ)
    
    # Startpoint
    locationStartPoint = locationCurve.GetEndPoint(0)
    startX = round(locationStartPoint.X, ROUNDTO)
    absStartX = abs(startX)
    startPoint["X"] = startX
    startY = round(locationStartPoint.Y, ROUNDTO)
    absStartY = abs(startY)
    startPoint["Y"] = startY
    startZ = round(locationStartPoint.Z, ROUNDTO)
    absStartZ = abs(startZ)
    startPoint["Z"] = startZ
    
    # Endpoint
    locationEndPoint = locationCurve.GetEndPoint(1)
    endX = round(locationEndPoint.X, ROUNDTO)
    absEndX = abs(endX)
    endPoint["X"] = endX
    endY = round(locationEndPoint.Y, ROUNDTO)
    absEndY = abs(endY)
    endPoint["Y"] = endY
    endZ = round(locationEndPoint.Z, ROUNDTO)
    absEndZ = abs(endZ)
    endPoint["Z"] = endZ
    originSet = set(origin)
    startPointSet = set(startPoint)
    if absStartX > absEndX or absStartY> absEndY:
        data["ID"] = id
        data["Origin"] = origin
        data["Start Point"] = startPoint
        data["End Point"] = endPoint
    else:
        continue
        
    placementCheck.append(data)
    
    
#Do some action in a Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

TransactionManager.Instance.TransactionTaskDone()

OUT = placementCheck
