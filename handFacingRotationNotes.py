selected = uidoc.Selection.PickObject(Selection.ObjectType.Element)
elementId = selected.ElementId
element = doc.GetElement(elementId)
hand = element.HandOrientation
facing = element.FacingOrientation
handZ = hand.Z
facingZ = facing.Z
slope = math.degrees(math.asin(handZ))
facingSlopeZ = facingZ / (math.cos(math.radians(slope)))
crossSectionRotation = math.degrees(math.asin(facingSlopeZ))

crossRotationPara = BuiltInParameter.STRUCTURAL_BEND_DIR_ANGLE

elementRotationRad = element.get_Parameter(crossRotationPara).AsDouble()
elementRotationDeg = math.degrees(elementRotationRad)

if elementRotationRad <= math.pi:
    sdsRotationRad = elementRotationRad * -1
    sdsRotationDeg = math.degrees(sdsRotationRad)
else:
    sdsRotationDeg = 360 - elementRotationDeg
