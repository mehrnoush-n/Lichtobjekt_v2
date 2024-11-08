import vs
import math


def get_objects_on_layer(layer_name):
    objects = []   
    def collect_object(handle):
        objects.append(handle)    
    criteria = f"(L='{layer_name}')"    
    vs.ForEachObject(collect_object, criteria) 
   	
    return objects

def NewNurbsCurve(x1,y1,z1,x2,y2,z2):
	nC = vs.CreateNurbsCurve(x1, y1, z1, True, 1)
	#vs.AddVertex3D(nC, 1, 1, 0)
	vs.AddVertex3D(nC, x2, y2, z2)
	return nC


def run():
    # Enable the pydev debugger
    # import pydevd
    # pydevd.settrace(suspend=False)

    # name of the class the PIO would be assigned to
    class_name = 'BIM-430_ELEKTRISCHE_ANLAGEN-4451_Allgemeinbeleuchtung'
    #Datenbank for the Bahnsteig and Lichtobjekt PIOs
    format_data_I = 'U-Bahn Station_I'
    format_data_O = 'Lichtobjekt_O'
    
    objectName, objectHand, recordHand, wallHand = 0, 0, 0, 0
    ok, objectName, objectHand, recordHand, wallHand = vs.GetCustomObjectInfo( objectName, objectHand, recordHand, wallHand )
    if ok:
        # Retrieve the value of a parameter that is entered by the user
        station = vs.Pstation
        h = vs.Pheight
        w = vs.Pwidth
        l = vs.Plength
        th = vs.Pthickness
        r = vs.Psize
        r_sec = vs.Psize_1
        type = vs.Ptype
        side = vs.Pside
        form = vs.Pform
        mat = vs.GetObject(vs.Pmaterial)
        # Define r1 as half of the r parameter (thickness of the members in the structure).
        # Define r2 as half of the length of the interior rectangle, where the profile section consists of two rectangles (interior and exterior)
        r1 = r/2
        r1_sec = r_sec/2
        r2 = abs(r - 2*th)/2
        r2_sec = abs(r_sec - 2*th)/2
        if r2 == 0:
            vs.AlrtDialog(' profile cannot  be created ')
        # creating the exterior rectangle of the profile
        
        vs.Rect(-r1,-r1,r1,r1)
        rec_1 = vs.LNewObj()

        # creating the interior rectangle of the profile
        vs.Rect(-r2,-r2,r2,r2)
        rec_2 = vs.LNewObj()
        
        vs.Rect(-r1,-r1_sec,r1,r1_sec)
        rec_1_sec_z = vs.LNewObj()

        # creating the interior rectangle of the profile
        vs.Rect(-r2,-r2_sec,r2,r2_sec)
        rec_2_sec_z = vs.LNewObj()
        
        vs.Rect(-r1_sec,-r1,r1_sec,r1)
        rec_1_sec_y = vs.LNewObj()

        # creating the interior rectangle of the profile
        vs.Rect(-r2_sec,-r2,r2_sec,r2)
        rec_2_sec_y = vs.LNewObj()



        # creating the profile
        profile = vs.AddHole(rec_1, rec_2)[1]
        profile_sec_z = vs.AddHole(rec_1_sec_z, rec_2_sec_z)[1]
        profile_sec_y = vs.AddHole(rec_1_sec_y, rec_2_sec_y)[1]
        
        # Define cube as the list of lines to be extruded along the profile section at the end
        cube = []
        # # Define cube_sec as the list of lines to be extruded along the profile section at the end (for smaller sections)
        # delta z
        cube_sec_z = []
        # delta y
        cube_sec_y = []
        if form == 'Rechteck':
            if type == 'non-cap':
                if side == 'left':
                    
                    
                    # delta x - up
                    cube.append(NewNurbsCurve(0,r1,-r1,    l-r,r1,-r1))
                    # delta y - up
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l-r,w-r1,-r1 ))

                    
                    # delta x - down
                    cube.append(NewNurbsCurve(0,r1,r1-h,    l-r,r1,r1-h))
                    # delta y - down
                    cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    # delat x - down
                    cube.append(NewNurbsCurve(0,w-r1,r1-h,    l-r,w-r1,r1-h ))

                    
                    # delta z - right
                    cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    # delta z - right
                    cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    
                
                # form : Rechteck , type : non-cap , side : right    
                else:
                    # delta y - up
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(r,r1,-r1,    l,r1,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(r,w-r1,-r1,    l,w-r1,-r1 ))
                    
                    # delta y - down
                    cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    # delta x - down
                    cube.append(NewNurbsCurve(r,r1,r1-h,    l,r1,r1-h))
                    # delta x  - down
                    cube.append(NewNurbsCurve(r,w-r1,r1-h,    l,w-r1,r1-h ))

                    # delta z - left
                    cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    # delta z - left
                    cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
            # form : Rechteck , type : cap        
            else:
                
                if side == 'left': 
                    # delta y - up
                    cube_sec_y.append(NewNurbsCurve(r1_sec,r,-r1,    r1_sec,w-r,-r1))
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    
                    # delta y - down
                    cube_sec_y.append(NewNurbsCurve(r1_sec,r,r1-h,    r1_sec,w-r,r1-h))
                    cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))

                    # delta x - up
                    cube.append(NewNurbsCurve(r_sec,r1,-r1,    l-r,r1,-r1))                      
                    cube.append(NewNurbsCurve(r_sec,w-r1,-r1,    l-r,w-r1,-r1 ))
                    
                    # delta x - down
                    cube.append(NewNurbsCurve(r_sec,r1,r1-h,    l-r,r1,r1-h))
                    cube.append(NewNurbsCurve(r_sec,w-r1,r1-h,    l-r,w-r1,r1-h ))

                    # delta z - left
                    cube_sec_z.append(NewNurbsCurve(r1_sec,r1,-h,    r1_sec,r1,0))
                    cube_sec_z.append(NewNurbsCurve(r1_sec,w-r1,-h,    r1_sec,w-r1,0 ))
                    
                    # delta z - right
                    cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    
                
                else:
                    # delta y - up
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube_sec_y.append(NewNurbsCurve(l-r1_sec,r,-r1,    l-r1_sec,w-r,-r1))
                    
                    
                    # delta y - down
                    cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube_sec_y.append(NewNurbsCurve(l-r1_sec,r,r1-h,    l-r1_sec,w-r,r1-h))
                    
                    # delta x - up
                    cube.append(NewNurbsCurve(r,r1,-r1,    l-r_sec,r1,-r1))
                    cube.append(NewNurbsCurve(r,w-r1,-r1,    l-r_sec,w-r1,-r1 ))

                    # delta x - down
                    cube.append(NewNurbsCurve(r,r1,r1-h,    l-r_sec,r1,r1-h))
                    cube.append(NewNurbsCurve(r,w-r1,r1-h,    l-r_sec,w-r1,r1-h ))

                    # delta z - left
                    cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    
                    # delta z - right
                    cube_sec_z.append(NewNurbsCurve(l-r1_sec,r1,-h,    l-r1_sec,r1,0))
                    cube_sec_z.append(NewNurbsCurve(l-r1_sec,w-r1,-h,    l-r1_sec,w-r1,0))

                
                

        elif form == 'gleichschenkliges Dreieck':

            angle = math.pi/2 - math.atan2(-r+h, w/2-r1)
            
            zz = r1 * math.sin(angle)
            yy = r1 * math.cos(angle)
            if type == 'non-cap':
                if side == 'left':
                    # delta y - up
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    # delta x - down
                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    
                    #dia_2
                    cube.append(NewNurbsCurve(-r1+l ,0+yy ,-r+zz, -r1+l, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(-r1+l ,w-yy ,-r+zz, -r1+l, w/2+r1-yy ,-h+zz))
                # form : gleichschenkliges Dreieck , type : non-cap , side : right    
                else:
                    
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))

                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))

                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    #dia_1
                    cube.append(NewNurbsCurve(r1 ,0+yy ,-r+zz, r1, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(r1 ,w-yy ,-r+zz, r1, w/2+r1-yy ,-h+zz))
                    

            
            # form : gleichschenkliges Dreieck , type : cap   
            else:
                if side == 'left':
                    # delta y - up
                    cube_sec_y.append(NewNurbsCurve(r1_sec,r,-r1,    r1_sec,w-r,-r1))
                    # delta y - up
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))

                    # delta x - up
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    
                    # delta x - down
                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    
                    #dia_1 left
                    cube_sec_z.append(NewNurbsCurve(r1_sec ,0+yy ,-r+zz, r1_sec, w/2-r1+yy ,-h+zz))
                    cube_sec_z.append(NewNurbsCurve(r1_sec ,w-yy ,-r+zz, r1_sec, w/2+r1-yy ,-h+zz))
                    
                    #dia_2 right
                    cube.append(NewNurbsCurve(-r1+l ,0+yy ,-r+zz, -r1+l, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(-r1+l ,w-yy ,-r+zz, -r1+l, w/2+r1-yy ,-h+zz))
                
                else : 
                    # delta y - up
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    # delta y - up
                    cube_sec_y.append(NewNurbsCurve(l-r1_sec,r,-r1,    l-r1_sec,w-r,-r1))

                    # delta x up
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    # delta x - up
                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    #dia_1 left
                    cube.append(NewNurbsCurve(r1 ,0+yy ,-r+zz, r1, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(r1 ,w-yy ,-r+zz, r1, w/2+r1-yy ,-h+zz))
                    
                    #dia_2 right
                    cube_sec_z.append(NewNurbsCurve(-r1_sec+l ,0+yy ,-r+zz, -r1_sec+l, w/2-r1+yy ,-h+zz))
                    cube_sec_z.append(NewNurbsCurve(-r1_sec+l ,w-yy ,-r+zz, -r1_sec+l, w/2+r1-yy ,-h+zz))

                

        elif form == 'flach':
            if type == 'non-cap':
                if side == 'left':
                    # up
                    # delta x
                    #cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta y
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta x
                    #cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))
                    
                    # down
                    cube.append(NewNurbsCurve(0,r1,r1-h,    l,r1,r1-h))
                    cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,w-r1,r1-h,    l,w-r1,r1-h ))



                    
                # form : gleichschenkliges Dreieck , side : right , type : non-cap 
                else:
                    # up
                    # delta y
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    # delta x
                    #cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta x
                    #cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))
                    
                    # down
                    cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,r1,r1-h,    l,r1,r1-h))
                    cube.append(NewNurbsCurve(0,w-r1,r1-h,    l,w-r1,r1-h ))

                    
            # form : flach , type : cap       
            else:
                # delta x
                cube.append(NewNurbsCurve(0,r1,r1-h,    l,r1,r1-h))
                cube.append(NewNurbsCurve(0,w-r1,r1-h,    l,w-r1,r1-h ))
                if side == 'left':
                    # up
                    # delta y
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta x
                    #cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    #cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))
                    
                    # down
                    # delta y
                    cube_sec_y.append(NewNurbsCurve(r1_sec,r,r1-h,    r1_sec,w-r,r1-h))
                    cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    
                
                else : 
                    # up
                    # delta y
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta x
                    #cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    #cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))
                    
                    # down
                    # delta y
                    cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube_sec_y.append(NewNurbsCurve(l-r1_sec,r,r1-h,    l-r1_sec,w-r,r1-h))
                    

                

        # form : Dreieck , type : non-cap , side : left
        else:
            angle = math.pi/2 - math.atan2(-h-r1, r1+w)
            zz = r1 * math.sin(angle)
            yy = r1 * math.cos(angle)

            if type == 'non-cap':
                if side == 'left':
                    
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,w-r1,-h+r1))
                    
                    cube.append(NewNurbsCurve(l-r1,0-yy,-r+zz,    l-r1,w-r-yy,-h+zz))
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))    
                
                # form : Dreieck , type : non-cap , side : right   
                else:
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r1))
                    
                    cube.append(NewNurbsCurve(r1,0-yy,-r+zz,    r1,w-r-yy,-h+zz))
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))  
                    
            # form : Dreieck , type : cap      
            else:
                if side == 'left' : 
                    # delta y - right
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    # delta y - left
                    cube_sec_y.append(NewNurbsCurve(r1_sec,r,-r1,    r1_sec,w-r,-r1))
                    # delta x
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta z - right
                    cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,w-r1,-h+r1))
                    # delta z - left
                    cube_sec_z.append(NewNurbsCurve(r1_sec,w-r1,-r,    r1_sec,w-r1,-h+r1))
                    
                    # delta x - down
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))

                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1)) 

                    # dia left
                    cube_sec_z.append(NewNurbsCurve(r1_sec,0-yy,-r+zz,    r1_sec,w-r-yy,-h+zz))
                    # dia right
                    cube.append(NewNurbsCurve(l-r1,0-yy,-r+zz,    l-r1,w-r-yy,-h+zz))
                
                else:
                    # delta y - right
                    cube_sec_y.append(NewNurbsCurve(l-r1_sec,r,-r1,    l-r1_sec,w-r,-r1))
                    # delta y - left
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    
                    
                    # delta x
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    # delta z - right
                    cube_sec_z.append(NewNurbsCurve(l-r1_sec,w-r1,-r,    l-r1_sec,w-r1,-h+r1))
                    # delta z - left
                    cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r1))
                    
                    # delta x - down
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))

                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1)) 

                    # dia left
                    cube.append(NewNurbsCurve(r1,0-yy,-r+zz,    r1,w-r-yy,-h+zz))
                    # dia right
                    cube_sec_z.append(NewNurbsCurve(l-r1_sec,0-yy,-r+zz,    l-r1_sec,w-r-yy,-h+zz))
                    
        
        
        
        for line in cube : 
            # class 
            vs.NameClass(class_name)
            # extrusion
            structure = vs.ExtrudeAlongPath(line, profile)
            vs.SetClass(structure,class_name)
            vs.DelObject(line)
            # material
            vs.SetObjMaterialHandle(structure, mat)
        
        if len(cube_sec_z):
            for line in cube_sec_z:
                # class 
                vs.NameClass(class_name)
                # extrusion
                structure_sec = vs.ExtrudeAlongPath(line, profile_sec_z)
                vs.SetClass(structure_sec,class_name)
                vs.DelObject(line)
                # material
                vs.SetObjMaterialHandle(structure_sec, mat)
            for line in cube_sec_y:
                # class 
                vs.NameClass(class_name)
                # extrusion
                structure_sec = vs.ExtrudeAlongPath(line, profile_sec_y)
                vs.SetClass(structure_sec,class_name)
                vs.DelObject(line)
                # material
                vs.SetObjMaterialHandle(structure_sec, mat)




        # class
        vs.SetClass(objectHand, class_name)  
        vs.DelObject(rec_1)
        vs.DelObject(rec_2)
        vs.DelObject(rec_1_sec_y)
        vs.DelObject(rec_2_sec_z)
        vs.DelObject(rec_1_sec_z)
        vs.DelObject(rec_2_sec_y)
        
        vs.DelObject(profile)
        vs.DelObject(profile_sec_y)
        vs.DelObject(profile_sec_z)
        # material 
        vs.SetObjMaterialHandle(structure, mat)
        # 2D representation
        vs.Generate2DFrom3DComp(objectHand, 1,6, 1)
        
        # Datenbank
        vs.SetRecord(objectHand,format_data_O )
        
        vs.SetRField(objectHand, format_data_O, 'Station', station)        
        vs.SetRField(objectHand, format_data_O, 'Form', form)
        if type == 'non-cap':
            typ = type
        else:
            if r == r_sec:
                typ = 'cap-symmetrisch'
            else : 
                typ = 'cap-unsymmetrisch'
        
        vs.SetRField(objectHand, format_data_O, 'Type', typ)        
        vs.SetRField(objectHand, format_data_O, 'Side', side)        
        vs.SetRField(objectHand, format_data_O, 'Höhe', h)        
        vs.SetRField(objectHand, format_data_O, 'Länge', l)        
        vs.SetRField(objectHand, format_data_O, 'Breite', w)        
        vs.SetRField(objectHand, format_data_O, 'Breite', w)        
        vs.SetRField(objectHand, format_data_O, 'Profilstärke', th)        
        vs.SetRField(objectHand, format_data_O, 'Profilgröße', r)        
        vs.SetRField(objectHand, format_data_O, 'Profilgröße cap', r_sec)        
        #vs.SetRField(objectHand, format_data_O, 'Material', mat)        
    
            
            
			
