ROUNDTO = 4

description_parameter = "Description One"

structural_framing_category = BuiltInCategory.OST_StructuralFraming

filter_brace = ElementStructuralTypeFilter(Structure.StructuralType.Brace)

structural_framing = cc(doc, structural_framing_category)

bracing = FilteredElementCollector(doc).WherePasses(filter_brace).WhereElementIsNotElementType().ToElementIds()

ids_bracing = List[ElementId]()
try:
    for brace in bracing:
        ids_bracing.Add(brace)
except:
    pass
    
try:    
    beams = structural_framing.Excluding(ids_bracing).WhereElementIsNotElementType().ToElements()
except:
    beams = structural_framing.WhereElementIsNotElementType().ToElements()


#Do some action in a Transaction
TransactionManager.Instance.EnsureInTransaction(doc)

def get_point_cordinates(point, rounding):
    x = round(point.X, rounding)
    y = round(point.Y, rounding)
    z = round(point.Z, rounding)
    return x, y, z
    
def coordinate_dictionary(coord_x, coord_y, coord_z):
    dict = {}
    dict["X"] = coord_x
    dict["Y"] = coord_y
    dict["Z"] = coord_z
    return dict

placement_check = []
for beam in beams:
    data = {}
    origin = {}
    start_point = {}
    end_point = {}
    id = beam.Id.ToString()
    location_curve = beam.Location.Curve
    location_origin = location_curve.Origin
    location_curve_start_point = location_curve.GetEndPoint(0)
    location_curve_end_point = location_curve.GetEndPoint(1)
    hand_orientation = beam.HandOrientation
    hand_x, hand_y, hand_z = get_point_cordinates(hand_orientation, ROUNDTO)
    if hand_x > 0:
        rotation = round(360 - (math.degrees(math.acos(hand_y))),ROUNDTO)
    else:
        rotation = round(math.degrees(math.acos(hand_y)), ROUNDTO)
    
    if rotation >= 45 and rotation < 225:
        rotation_check = "Incorrect"
    else:
        rotation_check = "Correct"
        
    data["Rotation"] = rotation
    data["Rotation Check"] = rotation_check
    
    start_x, start_y, start_z = get_point_cordinates(location_curve_start_point, ROUNDTO)
    start_point_dict = coordinate_dictionary(start_x, start_y, start_z)
    end_x, end_y, end_z = get_point_cordinates(location_curve_end_point, ROUNDTO)
    end_point_dict = coordinate_dictionary(end_x, end_y, end_z)
    placement_direction_check = beam.LookupParameter("Placement Direction Check")
    
    if start_x > end_x or start_y > end_y:
        data["ID"] = id
        data["Start Point"] = start_point_dict
        data["End Point"] = end_point_dict
        placement_direction_check.Set(0)
        #description = beam.LookupParameter(description_parameter)
        #description_message = description.AsValueString()
        #description.Set("SHORT")
        #dataDictionary["Description"] = c.LookupParameter(description_parameter).AsValueString()
        #if description_message and description_message.isalnum():
            #description_message += " PLACEMENT"
            #description.Set(description_message)
        #else:
            #description.Set("PLACEMENT")
        #data["Description"] = beam.LookupParameter(description_parameter).AsValueString()
    else:
        placement_direction_check.Set(1)
    placement_check.append(data)
"""        
with open(r"X:\ML\2023\20230291\Design\BIM\Model Health\20220291_Framing_Placement.csv", 'w', newline='') as csvfile:
    for check in placement_check:
        key = check.keys()
        fieldnames = [k for k in key]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
    for check_data in placement_check:
        writer.writerow(check_data)
"""        
TransactionManager.Instance.TransactionTaskDone()

OUT = placement_check
