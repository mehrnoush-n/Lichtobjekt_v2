import vs
import math
#Hyper parameter
layer_plots_new = "Parzellen_neu"
#here is the 3rd version
#i added another useless comment
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
    
    objectName, objectHand, recordHand, wallHand = 0, 0, 0, 0
    ok, objectName, objectHand, recordHand, wallHand = vs.GetCustomObjectInfo( objectName, objectHand, recordHand, wallHand )
    if ok:
        h = vs.Pheight
        w = vs.Pwidth
        l = vs.Plength
        th = vs.Pthickness
        r = vs.Psize
        type = vs.Ptype
        side = vs.Pside
        form = vs.Pform

        r1 = r/2
        r2 = abs(r - 2*th)/2
        if r2 == 0:
            vs.AlrtDialog(' profile cannot  be created ')

        vs.Rect(-r1,-r1,r1,r1)
        rec_1 = vs.LNewObj()
        vs.Rect(-r2,-r2,r2,r2)
        rec_2 = vs.LNewObj()
        profile = vs.AddHole(rec_1, rec_2)[1]
        

        cube = []
        if form == 'Rechteck':
            if type == 'non-cap':
                if side == 'left':
                    
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l-r,r1,-r1))
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l-r,w-r1,-r1 ))

                    #cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,r1,r1-h,    l-r,r1,r1-h))
                    cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,w-r1,r1-h,    l-r,w-r1,r1-h ))

                    #cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    #cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    
                else:
                    
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(r,r1,-r1,    l,r1,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(r,w-r1,-r1,    l,w-r1,-r1 ))

                    cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(r,r1,r1-h,    l,r1,r1-h))
                    #cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(r,w-r1,r1-h,    l,w-r1,r1-h ))

                    cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    #cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    #cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    
            else:
                
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(r,r1,-r1,    l-r,r1,-r1))
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                cube.append(NewNurbsCurve(r,w-r1,-r1,    l-r,w-r1,-r1 ))

                cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                cube.append(NewNurbsCurve(r,r1,r1-h,    l-r,r1,r1-h))
                cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                cube.append(NewNurbsCurve(r,w-r1,r1-h,    l-r,w-r1,r1-h ))

                cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                
                
                

        elif form == 'gleichschenkliges Dreieck':
            angle = math.pi/2 - math.atan2(-r+h, w/2+r1)
        
            zz = r1 * math.sin(angle)
            yy = r1 * math.cos(angle)
            if type == 'non-cap':
                if side == 'left':
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))

                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))

                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    #dia_1
                    #cube.append(NewNurbsCurve(r1 ,0+d ,-r+d, r1, w/2-r1+d ,-h+d))
                    #cube.append(NewNurbsCurve(r1 ,w-d ,-r+d, r1, w/2+r1-d ,-h+d))
                    #dia_2
                    cube.append(NewNurbsCurve(-r1+l ,0+yy ,-r+zz, -r1+l, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(-r1+l ,w-yy ,-r+zz, -r1+l, w/2+r1-yy ,-h+zz))
                    
                else:
                    
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))

                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))

                    cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                    #dia_1
                    cube.append(NewNurbsCurve(r1 ,0+yy ,-r+zz, r1, w/2-r1+yy ,-h+zz))
                    cube.append(NewNurbsCurve(r1 ,w-yy ,-r+zz, r1, w/2+r1-yy ,-h+zz))
                    #dia_2
                    #cube.append(NewNurbsCurve(-r1+l ,0+d ,-r+d, -r1+l, w/2-r1+d ,-h+d))
                    #cube.append(NewNurbsCurve(-r1+l ,w-d ,-r+d, -r1+l, w/2+r1-d ,-h+d))

            
                   
            else:
                
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))

                cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))

                cube.append(NewNurbsCurve(0,(w)/2 , r1-h, l,(w)/2 ,r1-h))
                #dia_1
                cube.append(NewNurbsCurve(r1 ,0+yy ,-r+zz, r1, w/2-r1+yy ,-h+zz))
                cube.append(NewNurbsCurve(r1 ,w-yy ,-r+zz, r1, w/2+r1-yy ,-h+zz))
                #dia_2
                cube.append(NewNurbsCurve(-r1+l ,0+yy ,-r+zz, -r1+l, w/2-r1+yy ,-h+zz))
                cube.append(NewNurbsCurve(-r1+l ,w-yy ,-r+zz, -r1+l, w/2+r1-yy ,-h+zz))

        elif form == 'Flach':
            if type == 'non-cap':
                if side == 'left':
                    
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))

                    #cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    #cube.append(NewNurbsCurve(0,r1,r1-h,    l-r,r1,r1-h))
                    #cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    #cube.append(NewNurbsCurve(0,w-r1,r1-h,    l-r,w-r1,r1-h ))

                    #cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    #cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    #cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    #cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    
                else:
                    
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    #cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))

                    #cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    #cube.append(NewNurbsCurve(r,r1,r1-h,    l,r1,r1-h))
                    #cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                    #cube.append(NewNurbsCurve(r,w-r1,r1-h,    l,w-r1,r1-h ))

                    #cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    #cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    #cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    #cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    
            else:
                
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))

                #cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                #cube.append(NewNurbsCurve(r,r1,r1-h,    l-r,r1,r1-h))
                #cube.append(NewNurbsCurve(l-r1,r,r1-h,    l-r1,w-r,r1-h))
                #cube.append(NewNurbsCurve(r,w-r1,r1-h,    l-r,w-r1,r1-h ))

                #cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                #cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                #cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                #cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))


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
                    
                else:
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r1))
                    
                    cube.append(NewNurbsCurve(r1,0-yy,-r+zz,    r1,w-r-yy,-h+zz))
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))  
                    
                    
            else:
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,w-r1,-h+r1))
                
                cube.append(NewNurbsCurve(l-r1,0-yy,-r+zz,    l-r1,w-r-yy,-h+zz))
                cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))
                cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1)) 
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r1))
                cube.append(NewNurbsCurve(r1,0-yy,-r+zz,    r1,w-r-yy,-h+zz))
        for line in cube : 
            vs.NameClass('BIM-430_ELEKTRISCHE_ANLAGEN-4451_Allgemeinbeleuchtung')
            structure = vs.ExtrudeAlongPath(line, profile)
            vs.SetClass(structure,'BIM-430_ELEKTRISCHE_ANLAGEN-4451_Allgemeinbeleuchtung')
            vs.DelObject(line)

        vs.SetClass(objectHand, 'BIM-430_ELEKTRISCHE_ANLAGEN-4451_Allgemeinbeleuchtung')  
        
    
            
            
			
