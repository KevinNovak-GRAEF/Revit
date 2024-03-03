base_point = BasePoint.GetProjectBasePoint(doc)
base_point_position = base_point.Position
base_point_position_z = base_point_position.Z
survey_point = BasePoint.GetSurveyPoint(doc)
survey_point_position = survey_point.Position
survey_point_position_z = survey_point_position.Z

baseElevationParam = BuiltInParameter.BASEPOINT_ELEVATION_PARAM
baseNSParam = BuiltInParameter.BASEPOINT_NORTHSOUTH_PARAM
baseEWParam = BuiltInParameter.BASEPOINT_EASTWEST_PARAM

reference = uidoc.Selection.PickObject(Selection.ObjectType.Element)
elmnt = doc.GetElement(reference)

projectBase = BasePoint.GetProjectBasePoint(doc)
projectBasePosition = projectBase.Position
projectBasePositionX = projectBasePosition.X
projectBasePositionY = projectBasePosition.Y
projectBasePositionZ = projectBasePosition.Z

curve = elmnt.Location.Curve
startPoint = curve.GetEndPoint(0)
startPointX = startPoint.X
startPointY = startPoint.Y
startPointZ = startPoint.Z




startPointXPB = startPointX - projectBasePositionX
startPointYPB = startPointY - projectBasePositionY
startPointZPB = startPointZ - projectBasePositionZ

startPointPB = XYZ(startPointXPB, startPointYPB, startPointZPB)
