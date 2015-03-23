import rhinoscriptsyntax as rs
 

# funtion to gather input and call the recursive function 
def aggregation ():
    intGens = rs.GetInteger("how many generations", 5,1,8)
    listObjs = []
    listObjs.append (rs.GetObject ("select mesh",16))
   
    listObjs.append (rs.GetObject ("select reference point 1",1))
    listObjs.append (rs.GetObject ("select reference point 2",1))
    listObjs.append (rs.GetObject ("select reference point 3",1))
   
    listObjs.append (rs.GetObject ("select target 1 point 1",1))
    listObjs.append (rs.GetObject ("select target 1 point 2",1))
    listObjs.append (rs.GetObject ("select target 1 point 3",1))
   
    listObjs.append (rs.GetObject ("select target 2 point 1",1))
    listObjs.append (rs.GetObject ("select target 2 point 2",1))
    listObjs.append (rs.GetObject ("select target 2 point 3",1))
   
    substitute (listObjs,intGens)
   
 
# orient the input object based on reference and target points
def substitute (listObjs, intGens):
   
    # conditional statement
    if intGens > 1:
       
        # get a list of ref points
        refPts = []
        for i in range (1,4):
            refPts.append (rs.PointCoordinates (listObjs[i]) )
       
        # get a list of target 1 points
        targetPts1 = []
        for i in range (4,7):
            targetPts1.append (rs.PointCoordinates (listObjs[i]) )
           
        # get a list of target 1 points
        targetPts2 = []
        for i in range (7,10):
            targetPts2.append (rs.PointCoordinates (listObjs[i]) )
       
        # orient the list of objects (mesh + points)
       
        listNewObjs1 = []
        listNewObjs2 = []
        for i in range (len(listObjs)):
            listNewObjs1.append (rs.OrientObject (listObjs[i], refPts, targetPts1, 1))
            listNewObjs2.append (rs.OrientObject (listObjs[i], refPts, targetPts2, 1))
           
        substitute (listNewObjs1, intGens-1)
        substitute (listNewObjs2, intGens-1)
 
aggregation ()
