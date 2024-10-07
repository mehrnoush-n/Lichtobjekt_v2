import vs
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
        r2 = (r - 2*th)/2
        vs.Rect(-r1,-r1,r1,r1)
        a = vs.LNewObj()
        vs.Rect(-r2,-r2,r2,r2)
        b = vs.LNewObj()
        c = vs.AddHole(a, b)[1]
        
        cube = []
        if form == 'Rechteck':
            if type == 'non-cap':
                if side == 'left':
                    pass
                    '''
                    #cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(l,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1 ))

                    #cube.append(NewNurbsCurve(r1,r,r1-h,    r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,r1,r1-h,    l,r1,r1-h))
                    cube.append(NewNurbsCurve(l,r,r1-h,    l-r1,w-r,r1-h))
                    cube.append(NewNurbsCurve(0,w-r1,r1-h,    l,w-r1,r1-h ))

                    #cube.append(NewNurbsCurve(r1,r1,-h,    r1,r1,0))
                    cube.append(NewNurbsCurve(l-r1,w-r1,-h,    l-r1,w-r1,0))
                    cube.append(NewNurbsCurve(l-r1,r1,-h,    l-r1,r1,0))
                    #cube.append(NewNurbsCurve(r1,w-r1,-h,    r1,w-r1,0 ))
                    '''
                else:
                    pass
                    '''
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
                    '''
            else:
                pass
                '''
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
                '''
                
                

        elif form == 'gleichschenkliges Dreieck':
            if type == 'non-cap':
                if side == 'left':
                    pass
                    '''
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    
                    cube.append(NewNurbsCurve(0,(w)/2,r1-h, l,(w)/2,r1-h))
                    
                    cube.append(NewNurbsCurve(l-r1,r,-r,    l-r1,(w-r)/2,r1-h))
                    cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,(w-r)/2,r1-h))
                    '''
                else:
                    pass
                    '''
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    
                    cube.append(NewNurbsCurve(0,(w)/2,r1-h, l,(w)/2,r1-h))
                    
                    cube.append(NewNurbsCurve(r1,r,-r,    r1,(w-r)/2,r1-h))
                    cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,(w-r)/2,r1-h))
                    '''
            else:
                pass
                '''
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                
                cube.append(NewNurbsCurve(0,(w)/2,r1-h, l,(w)/2,r1-h))
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                
                cube.append(NewNurbsCurve(r1,r,-r,    r1,(w-r)/2,r1-h))
                cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,(w-r)/2,r1-h))
                
                cube.append(NewNurbsCurve(l-r1,r,-r,    l-r1,(w-r)/2,r1-h))
                cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,(w-r)/2,r1-h))
                '''
        else:
            if type == 'non-cap':
                if side == 'left':
                    pass
                    '''
                    cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))

                    cube.append(NewNurbsCurve(l-r1,r1,-r,    l-r1,w-r1,-h+r1))
                    cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,w-r1,-h+r1))

                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))      
                    '''
                else:
                    pass
                    '''
                    cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                    cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                    cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                    
                    #diagonal
                    cube.append(NewNurbsCurve(r1,r1,-r,    r1,w-r1,-h+r1))
                    cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r))
                    
                    #lower
                    cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))  
                    '''
            else:
                pass
                '''
                cube.append(NewNurbsCurve(r1,r,-r1,    r1,w-r,-r1))
                cube.append(NewNurbsCurve(l-r1,r,-r1,    l-r1,w-r,-r1))
                
                cube.append(NewNurbsCurve(0,r1,-r1,    l,r1,-r1))
                cube.append(NewNurbsCurve(0,w-r1,-r1,    l,w-r1,-r1))
                
                #diagonal
                cube.append(NewNurbsCurve(r1,r1,-r,    r1,w-r1,-h+r1))
                cube.append(NewNurbsCurve(r1,w-r1,-r,    r1,w-r1,-h+r))
                
                cube.append(NewNurbsCurve(l-r1,r1,-r,    l-r1,w-r1,-h+r1))
                cube.append(NewNurbsCurve(l-r1,w-r1,-r,    l-r1,w-r1,-h+r))
                
                #lower
                cube.append(NewNurbsCurve(0,w-r1,-h+r1, l,w-r1,-h+r1))     
                '''


        for n in cube : 
            vs.ExtrudeAlongPath(n, c)
            vs.DelObject(n)
            
        vs.DelObject(c)
        vs.DelObject(b)
        vs.DelObject(a)
    
            
            
			
