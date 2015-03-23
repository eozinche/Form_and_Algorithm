import rhinoscriptsyntax as rs
import Rhino
import time
import datetime
import math
import random as rnd
 
start = [] #starting points
goal =[] #goal points
obstacle = [] #obstacles
goalcy = [] #copy list of goal points
listgoal = [] #goal pts that correspond to starting pts after calculating the closest distance
listpt =[]
 
agentlist =[] #list of agents
traillist = [] #list to store agents' positions
 
#start = rs.GetObjects ("select the starting points" , 1)
#goal = rs.GetObjects ("select the goal points(same number to starting points)", 1)
obstacle = rs.GetObjects ("select the spaces", 32)
 
steps = 120
gene = 4
 
#initiate starting pts and goal pts
def initpts():
    del start[:]
    del goal[:]
    del goalcy[:]
    for n in range(30):
       
        """
       uniform returns a float value in range -1.0 ~ 1.0

        """
        startpt = [rnd.uniform(-1, 1)*10, rnd.uniform(-1, 1) *10, rnd.uniform(-1, 1) *1]
        start.append(startpt)
       
        #goalpt = [rnd.random()*20, rnd.random() *20, rnd.random() *10+90]
        goalpt = [rnd.uniform(-1, 1)*10, rnd.uniform(-1, 1) *10, rnd.uniform(-1, 1) *10 + 63]
        goal.append(goalpt)
       
        goalcy.append(goalpt)
        rs.AddPoint (startpt)
        rs.AddPoint (goalpt)
#    print goalcy
       
#initpts()
 
#generate new generation of agents
def generate():
    initpts()
    del listgoal[:]
    del agentlist[:]
    for j in range(len(start)):
        index = rs.PointArrayClosestPoint (goalcy, start[j])#calculate the closest pt from goal to agent[j]
        vec = rs.VectorCreate (goalcy[index],start[j])
        vec = rs.VectorScale (vec,3)
        listgoal.append(goalcy[index])#store the calculated pts into list
        goalcy.pop(index)#remove the calculating goal pt from goal list
       
        #velrnd = [(rnd.random()*2) - 1,(rnd.random()*2) - 1,(rnd.random()*2) - 1]
        """
       uniform
       """
        velrnd = [(rnd.uniform(-1, 1)*2),(rnd.uniform(-1, 1)*2),(rnd.random()*2)]
 
        vel = rs.VectorAdd (velrnd, vec)
        agentlist.append(agent(start[j], vel, 0.3, 1))
       
def run():
    for i in range(gene):
        del traillist[:]
        generate()
        for k in range(steps):
            #time.sleep (0.1)
            for j in range(len(agentlist)):
                agentlist[j].update()
                agentlist[j].render()
                #goaldis = rs.Distance (agentlist[j].pos, listgoal[j])
               
                newvel = rs.VectorCreate (listgoal[j], agentlist[j].pos)
                newvel = vectorlimit(newvel, 0.34)
                #newvel = rs.VectorScale (newvel,100/goaldis)
               
                agentlist[j].vel = rs.VectorAdd (newvel,agentlist[j].vel)
                listpt.append(agentlist[j].pos)
               
                traillist.append(agentlist[j].posP)
                Rhino.RhinoApp.Wait ()
 
 
class agent():
    def __init__(self, pos, vel, maxf, maxv):
        self.pos = pos
        self.vel = vel
        self.mf = maxf
        self.mv = maxv
 
        """
       FLAGS are used in Asignment, Cohesion, Separation
       """
        self.doAlignment = False
        self.doSeparation = False
        self.doCohesion = False
       
        self.listpts = []
       
    def update(self):
        self.posP = self.pos
        # call the behaviors
        velboids1 = self.AlignmentVector()
        velboids2 = self.SeparationVector()
        velboids3 = self.CohesionVector()
        velav = self.avoid()
        veltrail = self.trail(4)
       
        # scale the behaviors
        velboids1 = rs.VectorScale (velboids1, 0.1)
        velboids2 = rs.VectorScale (velboids2, 0.1)
        velboids3 = rs.VectorScale (velboids3, 0.2)
        velav = rs.VectorScale (velav, 0.8)
        veltrail = rs.VectorScale (veltrail, 20)
       
        # add the behaviors to the vel
        #self.vel = rs.VectorAdd (self.vel, velboids1)
        self.vel = rs.VectorAdd (self.vel, velboids2)
        self.vel = rs.VectorAdd (self.vel, velboids3)
        self.vel = rs.VectorAdd (self.vel, velav)
        self.vel = rs.VectorAdd (self.vel, veltrail)
       
        # update pos
       
        self.vel = vectorlimit(self.vel, self.mv)
       
        self.pos = rs.VectorAdd (self.pos, self.vel)
       
       
    def render(self):
        #rs.AddSphere (self.pos, rnd.random() * 1)
        #rs.AddPoint (self.pos)
        rs.AddLine (self.pos, self.posP)
        #self.listpts.append(self.posP)
 
   
    #following 3 rules are BOIDS
    def AlignmentVector(self):
       
        sum =[0,0,0]
       
        count = 0
       
        for i in range(len(agentlist)):
           
            if self.pos is not agentlist[i].pos:
                dis = rs.Distance (self.pos, agentlist[i].pos)
                self.setFlag(dis)
 
                if self.doAlignment:
                    sum = rs.VectorAdd (sum, agentlist[i].vel)
                    self.count += 1
           
        resultingVec = rs.VectorScale (sum, 1/(len(agentlist)-1))
        resultingVec = vectorlimit(resultingVec,self.mv)
       
        return resultingVec
 
 
    def SeparationVector (self):
       
        sum =[0,0,0]
       
        count = 0
       
        for i in range(len(agentlist)):
 
            if self.pos is not agentlist[i].pos:
                dis = rs.Distance (self.pos, agentlist[i].pos)
                self.setFlag(dis)
 
                if self.doSeparation:
                    sum = rs.VectorSubtract (sum, agentlist[i].pos)
                    count += 1
 
        #avepos = rs.VectorScale (sum, 1/count)
        avepos = rs.VectorScale (sum, count)
        resultingVec = rs.VectorCreate (avepos,self.pos)
        resultingVec = vectorlimit(resultingVec,self.mf)
       
        return resultingVec
 
 
    def CohesionVector (self):
       
        sum =[0,0,0]
       
        count = 0
       
        for i in range(len(agentlist)):
           
            if self.pos is not agentlist[i].pos:
                dis = rs.Distance (self.pos, agentlist[i].pos)
                self.setFlag(dis)
 
                if self.doCohesion:
                    sum = rs.VectorAdd (sum,agentlist[i].pos)
                    count += 1
               
        avepos = rs.VectorScale (sum, 1/(len(agentlist)-1))
        resultingVec = rs.VectorCreate (avepos, self.pos)
        resultingVec = vectorlimit(resultingVec, self.mf)
       
        return resultingVec
 
 
    def setFlag(self, dis):
 
        #print dis
           
        if dis < 1:
            #doAlignment = True
            self.doSeparation = True
            self.doCohesion = False
           
        #if 1 < dis and dis < 8:
            #doAlignment = False
           
        if 8 <= dis:
            #doAlignment = True
            self.doCohesion = True
            self.doSeparation = False
       
 
    # let next generation to trace the last generations' routes
    def trail(self, r):
        vectr = [0,0,0]
        sum = [0,0,0]
        count = 0
        if traillist:
            for i in range(len(traillist)):
                distan = rs.Distance (self.pos, traillist[i])
                vecref = rs.VectorCreate (traillist[i],self.pos)
                angl = rs.VectorAngle (self.vel,vecref)
                if 0 < distan < r and 0 < angl < 45:
                    sum = rs.VectorAdd (sum, traillist[i])
                    count = count + 1
            if count > 0:
                avep = rs.VectorScale (sum, 1/count)
                vectr = rs.VectorCreate (avep, self.pos)
                vectr = vectorlimit(vectr,self.mf)
            #if count == 0:
        #print(vectr)
        return vectr
 
 
    #avoid the obstacles
    def avoid(self):
        if obstacle:
            avoid = [0,0,0]
            count = 0
            sumradar = 0
            averadar = 0
            for i in range(len(obstacle)):
                judge = rs.MeshClosestPoint(obstacle[i],self.pos)
                radar = rs.Distance (self.pos,judge[0])
                vecradar = rs.VectorCreate (self.pos, judge[0])
     #            print radar
                if radar < 0.5:
                    self.pos = rs.VectorSubtract (self.posP,self.pos)
                    vecradar = rs.VectorScale (vecradar, 2)

                if radar < 3 and radar > 0.5:
                    avoid = rs.VectorAdd (avoid,judge[0])
                    sumradar += radar
                    count += 1
                    vecradar = rs.VectorScale (vecradar, 0.5)
                    obstacle[i] = rs.MoveObject (obstacle[i], vecradar)
            if count != 0:
                aveavoid = rs.VectorScale (avoid, 1/count)
                averadar = sumradar/count
            else:
                aveavoid = self.pos
                averadar = averadar + 24
            vec1 = rs.VectorCreate (self.pos,aveavoid)
            vec1 = rs.VectorScale (vec1,((averadar+24)/averadar)**2)
            if rs.VectorLength (vec1) > 1:
                vec1 = vectorlimit(vec1,1)
     #           n = rnd.randint(0,10)
     #        vec1 = rs.VectorRotate (vec1,-60,[0,0,1])
           
        else: vec1 = [0,0,0]
       
        return vec1
 
 
       
#limit vector's  scale
def vectorlimit(vec,limit):
    if rs.VectorLength(vec) > limit:
        vec = rs.VectorUnitize(vec)
        vec = rs.VectorScale(vec, limit)
    return vec
 
  
run()
