#line_class = 'Linie'
lightobject_layer = 'Lichtobjectkte'
PIO_lightObject = 'Lichtobjekt_v2'
prefix = 'Gleis'
object_thickness = 0.1
#beam = 'Träger'
#column = 'Stütze'
#span = 'Span'
#platform_length = 'Gl'
#platform_width = 'Breite'

format_data_I = 'U-Bahn Station_I'
format_data_O = 'Lichtobjekt_O'


import vs
import itertools
import math

def get_objects_on_layer(layer_name):
	objects = []   
	def collect_object(handle):
		objects.append(handle)    
	criteria = f"(L='{layer_name}')"    
	vs.ForEachObject(collect_object, criteria) 
	return objects

def get_layers_starting_with(prefix):

    matching_layers = []

    layer_handle = vs.FLayer()

    while layer_handle:
        # Get the name of the current layer
        layer_name = vs.GetLName(layer_handle)

        if layer_name.startswith(prefix):
            matching_layers.append(layer_name)
        layer_handle = vs.NextLayer(layer_handle)
    
    return matching_layers



def convert_comma_to_float(number_str):
    # Replace the comma with a point
    number_str = number_str.replace(',', '.')
    try:
        # Convert the string to a float
        return float(number_str)
    except ValueError:
        # Handle the error if the conversion fails
        return f"Invalid input: {number_str} is not a valid number"

def SelectObjectsByClass(class_name):
	object_handles = []
	# Create a criteria string to filter objects by class
	def ProcessObject(obj_handle):
		vs.SetSelect(obj_handle)  # Select the object
		object_handles.append(obj_handle)  # Add the object handle to the list

	# Create a criteria string to filter objects by class
	criteria = f"C='{class_name}'"

	# Use ForEachObject to loop through objects that match the class criteria
	vs.ForEachObject(ProcessObject, criteria)

	# Return the list of object handles
	return object_handles

def line_pr(line):
	x1, y1 = vs.GetSegPt1(line)
	x2, y2 = vs.GetSegPt2(line)
	pt_start = (x1,y1)
	pt_end = (x2,y2)
	length = vs.Distance(x1,y1,x2,y2)
	return [pt_start,pt_end,length]

def replace_zeros_with_previous(input_list):

    if not input_list:  # Check if the list is empty
        return input_list
    
    # Initialize a variable to hold the last non-zero value
    last_value = None
    
    for i in range(len(input_list)):
        if input_list[i] == 0:
            if last_value is not None:
                input_list[i] = last_value  # Replace 0 with last non-zero value
        else:
            last_value = input_list[i]  # Update last_value to the current non-zero member
    
    return input_list


def assign_types(number_list):
    type_dict = {}
    result = []
    type_counter = 1
    
    # Iterate through the number list
    for number in number_list:
        # If the number is not already in the type_dict, assign a new type
        if number not in type_dict:
            type_dict[number] = f"type{type_counter}"
            type_counter += 1
        # Append the corresponding type to the result list
        result.append(type_dict[number])
    
    return result


def get_2_vertex_polyline_length(poly_handle):
    num_vertices = vs.GetVertNum(poly_handle)
    
    # Check if the polyline has exactly two vertices
    if num_vertices != 2:
        vs.AlrtDialog("This function only works on a polyline with exactly 2 vertices.")
        return 0.0
    
    # Get the coordinates of the two vertices
    x1, y1, z1 = vs.GetPolyPt3D(poly_handle, 0)
    x2, y2, z2 = vs.GetPolyPt3D(poly_handle, 1)
    
    # Calculate the 3D distance between the two points
    length = math.sqrt((x2 - x1)**2 + (y2 - y1)**2 + (z2 - z1)**2)
    
    return length




def PIO_aggregate(line , format_data_I , PIO_lightObject):
	sp = vs.GetRField( line, format_data_I, 'Spannweite')
	span = convert_comma_to_float(sp)

	b_h = vs.GetRField( line, format_data_I, 'Trägerhöhe')
	beam_h = convert_comma_to_float(b_h)
	
	p_w = vs.GetRField( line, format_data_I, 'Plattformbreite')
	platform_w = convert_comma_to_float(p_w)
	
	d_1 = vs.GetRField( line, format_data_I, 'd1')
	d1 = convert_comma_to_float(d_1)
	
	d_2 = vs.GetRField( line, format_data_I, 'd2')
	d2 = convert_comma_to_float(d_2)
	
	c_w = vs.GetRField( line, format_data_I, 'Stützenbreite')
	column_w = convert_comma_to_float(c_w)
	
	station = vs.GetRField(line, format_data_I, 'Station')
	layer_name_lightobject = lightobject_layer + '_'  + station
	
	pio_type =  vs.GetRField(line, format_data_I, 'Type')
	pio_side =  vs.GetRField(line, format_data_I, 'Side')
	pio_form =  vs.GetRField(line, format_data_I, 'Form')
	
	
	
	layer_handle = vs.GetLayerByName(layer_name_lightobject)
	if not layer_handle:
		vs.CreateLayer(layer_name_lightobject,1)
		layer_handle = vs.ActLayer()
		
	anchor_pts_s = vs.GetPolyPt3D(line, 0)
	anchor_pts_e = vs.GetPolyPt3D(line, 1)
	angle = 180
	anl = anchor_pts_e[0] - anchor_pts_s[0]
	if anl > 0:
		angle = 0
	
	first_PIO = vs.CreateCustomObject(PIO_lightObject,anchor_pts_s[0],anchor_pts_s[1],angle)
	
	p_height = float(beam_h) - float(d2)
	vs.SetRField(first_PIO, PIO_lightObject , 'height', p_height)
	vs.SetRField(first_PIO, PIO_lightObject , 'length', span)
	p_width = platform_w  - d1
	vs.SetRField(first_PIO, PIO_lightObject , 'width', p_width)
	vs.SetRField(first_PIO, PIO_lightObject , 'thickness', object_thickness)
	vs.SetRField(first_PIO, PIO_lightObject , 'type', pio_type)
	vs.SetRField(first_PIO, PIO_lightObject , 'side', pio_side)
	vs.SetRField(first_PIO, PIO_lightObject , 'form', pio_form)

	vs.SetParent(first_PIO, layer_handle)
	

	distance = convert_comma_to_float(vs.GetRField(first_PIO, PIO_lightObject, 'length')) 
			
	len_pl = get_2_vertex_polyline_length(line)
	num = round(len_pl / span)
	
	#platform_layer_handle= vs.GetLayer(line)
	#platform_z = float(vs.GetLayerElevation(platform_layer_handle)[0]) / 1000
	platform_z = float (vs.GetPolyPt3D(line, 1)[2])

	PIO_all = []
	for j in range(num):
		x = distance * j
		z = -(d2) + platform_z
		if angle != 0:
			x = -x
		obj_1 = vs.HDuplicate(first_PIO, 0,0)
		vs.Move3DObj(obj_1, x, 0 ,z) 
		vs.SetRecord(obj_1, format_data_O)
		vs.SetRField(obj_1, format_data_O, 'Station', station)
		PIO_all.append(obj_1)
	vs.DelObject(first_PIO) 
	return PIO_all
	

layers_Gleis = get_layers_starting_with(prefix)


#lines =[]
#for layer in layers_Gleis:
#	lines.append(get_objects_on_layer(layer))

lines = get_objects_on_layer(prefix)


PIO_alls=[]
for l in lines:
	PIO_alls.append(PIO_aggregate(l, format_data_I , PIO_lightObject))

flatten_PIO_alls = list(itertools.chain(*PIO_alls))

dimensions = []
for pio in PIO_alls[0]:
	l = vs.GetRField(pio, PIO_lightObject, 'length')
	w = vs.GetRField(pio, PIO_lightObject, 'width')
	h = vs.GetRField(pio, PIO_lightObject, 'height')
	th = vs.GetRField(pio, PIO_lightObject, 'thickness')
	ty = vs.GetRField(pio, PIO_lightObject, 'type')
	dimensions.append((convert_comma_to_float(l),convert_comma_to_float(w),convert_comma_to_float(h),convert_comma_to_float(th),ty))

'''
#assign type
types = assign_types(dimensions)


for i in range(len(flatten_PIO_alls)):
	pio = flatten_PIO_alls[i]
	vs.SetRecord(pio, format_data_O, 'Type')
	vs.SetRField(pio, format_data_O, 'Type', types[i])
'''