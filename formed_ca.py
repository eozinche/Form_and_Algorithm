import rhinoscriptsyntax as rs
import random as rnd
 
def CA():
   
    # input
    gridSizeX = rs.GetInteger("grid size X", 10)
    gridSizeY = rs.GetInteger("grid size Y", 10)
    steps = rs.GetInteger("how many steps", 20)
   
    listCells = [None]*gridSizeX
    # make first generation
    for x in range(gridSizeX):
        cells = [None]*gridSizeY
        for y in range(gridSizeY):
            if rnd.random() > 0.5:
                cells[y] = 1
            else:
                cells[y] = 0
        listCells[x] = cells
       
    # iterate through generations - steps
    for i in range(steps):
        rs.EnableRedraw(False)
        # loop x
        for x in range(gridSizeX):
            # loop y
            for y in range(gridSizeY):
                # torus space
                xMinus = x-1
                if x==0:
                    xMinus = gridSizeX-1
                xPlus = x+1
                if x==gridSizeX-1:
                    xPlus = 0
                yMinus = y-1
                if y==0:
                    yMinus = gridSizeY-1
                yPlus = y+1
                if y==gridSizeY-1:
                    yPlus = 0
               
                # sum neighbors
                sum = 0
                sum = sum + listCells[xMinus][yMinus]
                sum = sum + listCells[x][yMinus]
                sum = sum + listCells[xPlus][yMinus]
                sum = sum + listCells[xMinus][y]
                sum = sum + listCells[xPlus][y]
                sum = sum + listCells[xMinus][yPlus]
                sum = sum + listCells[x][yPlus]
                sum = sum + listCells[xPlus][yPlus]
               
                # rules
                # if alive and < 2 neighbors - dies = 0
                # if alive and == 2 or == 3 neighbors - alive = 1
                # if alive and > 3 neighbors - dies = 0
                # if dead and ==3 neighbors - alive = 1
                if listCells[x][y] == 1:
                    if sum < 2:
                        listCells[x][y] = 0
                    if sum == 2 or sum == 3:
                        listCells[x][y] = 0
                    if sum > 3:
                        listCells[x][y] = 1
                else:
                    if sum == 3:
                        listCells[x][y] = 0
               
                # render
                if listCells[x][y] == 1:
                    rs.AddPoint([x,y,i])
                    #rs.AddBox([ [x,y,i], [x+1,y,i], [x+1,y+1,i], [x,y+1,i], [x,y,i+1], [x+1,y,i+1], [x+1,y+1,i+1], [x,y+1,i+1]])
        rs.EnableRedraw(True)
 
CA()
