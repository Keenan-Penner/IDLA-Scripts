from idla_tree import *

import numpy

import matplotlib.pyplot as plt

import random

# Small scale --> more particles

BIRTH_SCALE = 0.5 # birth parameter 

TIME_SCALE= 0.1 # movement increment

MAX_TIME=10

WIDTH=2



class Particle:
    def __init__(self, num , bC, cS, bT, mT, alive):
        self.number = num
        self.birthCoord = bC
        self.currentSite = cS
        self.birthTime = bT
        self.mvtTime = mT
        self.alive = alive 


class Point:
    def __init__(self, x , y , bT ):
        self.xCoord = x
        self.yCoord = y
        self.birthTime = bT


class ParticleGrid:
    def __init__(self, d, w = WIDTH):
        self.width = w
        self.dictionary = d
    def createDictionary(self, dictionary):
        dico = {}
        for i in range(2*self.width + 1):
            for j in range(2*self.width + 1):
                dictKey = f"{i}--{j}"
                dico[dictKey] = dictionary



class Grid:
    def __init__(self, w = WIDTH):
        self.width = w
        self.grid = self.createDictionary()

    def createDictionary(self): 
        dictionary = {}
        for i in range(2*self.width + 1):
            for j in range(2*self.width +1):
                dictKey = f"{i-self.width}--{j-self.width}"
                birthTime=poissonProcess(BIRTH_SCALE)
                dictionary[dictKey] = Point(i-self.width, j-self.width, birthTime) 
        return dictionary 



## POISSON FUNCTIONS

def poissonProcess(param , time=MAX_TIME):
    t=0
    L=[]
    while t<=time:
        var=numpy.random.exponential(param)
        if t+var<= time:
            t+=var
            L.append(t)
        else:
            return L
    return L


def timeMatrix(param): #returns matrix of exponential times (with parameter param) for each site (structure: matrix of array)
    L=[]
    times=[]
    for i in range(2*WIDTH+1):
        line=[]
        for j in range(2*WIDTH+1):
            P=poissonProcess(param)
            for value in P:
                times.append(value)
            line.append(P)
        L.append(line)
        times.sort()
    return times, L 


## TOOLS

def fromWhich(value, L , M ): # returns TRUE if from first list, else FALSE
    for valueL in L:
        if value==valueL:
            return True
    return False

def findValue( value , d ): # finds Particle.number for a Particle.mvtTime entry
    for keys in d:
        if value in d[keys].mvtTime:
            return d[keys].number



## RANDOM WALK FUNCTIONS

def sum_list(L1,L2):
    S=[]
    for i in range(len(L1)):
        S.append(L1[i]+L2[i])
    return S


def movement(L,p): #for 2D idla
    if p<0.25:##right##
        
        newposition=sum_list(L[0],[1,0])
        L.append([1,0])
    
    
    elif 0.25<=p<0.5:##left##
        
        newposition=sum_list(L[0],[-1,0])
        L.append([-1,0])
    
    elif 0.5<=p<0.75:##up##
        
        newposition=sum_list(L[0],[0,1])
        L.append([0,1])
    
    else:##down##
        
        newposition=sum_list(L[0],[0,-1])
        L.append([0,-1])
    return L, newposition

## IDLA FUNCTIONS

def edenDLA(center = False):
    # INITIALIZATION OF GRID AND PARTICLES
    
    G = Grid() #creates square grid of size width with birthtimes for each point
    d = {}
    btimes = [] #birth times
    mtimes = [] #movement times
    times = [] # list with all times 
    info = []
    for element in G.grid: # loop on each site of the grid
        point = G.grid[element]
        btimes += point.birthTime # array of all birthtimes 
        for t in point.birthTime:
            info.append([t, point.xCoord, point.yCoord])
        info.sort(key = lambda x: x[0]) # sorted list with birthtime and corresponding birth site 
    #print(info)
    numParticles = len(info) # total number of particles born on grid
    print(numParticles)
    for k in range(numParticles):
        movementTimes = poissonProcess(TIME_SCALE)
        mtimes += movementTimes
        d[f"Particle{k}"] = Particle(k, info[k][1:3], info[k][1:3], info[k][0], movementTimes, False) 
    times=mtimes + btimes
    times.sort()
    # INITIALIZATION OF LOOP 
    agg = []
    count = 0 
    activeSites = []
    # MAIN LOOP
    count = 0
    #print(numParticles)
    #print(btimes)
    #print(mtimes)
    print(len(times))
    for index, t in enumerate(times):
        #print(t)
        fromBirth = fromWhich(t, btimes, mtimes) # returns True if birthtime, else False
        #print(fromBirth)
        #print(agg)
        if center:
            if fromBirth:
                p = d[f"Particle{count}"]
                #print(p.birthCoord)
                if [0,0] not in agg:
                    if p.birthCoord == [0,0]:
                        agg.append(p.birthCoord)
                else:
                    if p.birthCoord not in activeSites and p.birthCoord in agg:
                        activeSites.append(p.birthCoord) # site is now listed as active
                        p.alive = True
                #print(agg)
                count += 1
            else:
                particleNum = findValue(t, d) # locates which particle has to move
                #print(particleNum)
                p = d[f"Particle{particleNum}"]
                if p.alive : # checks if particle is alive or not
                    unif = random.random()
                    move = movement([p.currentSite], unif)[1] # generates random direction to go in 
                    if move not in agg:
                        agg.append(move)
                        p.alive = False 
                    elif move not in activeSites:
                        activeSites.append(move)
                        activeSites.remove(p.currentSite)
                        p.currentSite = move
            #print(index)
        else:
            if fromBirth:
                p = d[f"Particle{count}"]
                #print(p.birthCoord)
                if p.birthCoord not in agg:
                    agg.append(p.birthCoord)
                if p.birthCoord not in activeSites:
                    activeSites.append(p.birthCoord) # site is now listed as active
                    p.alive = True
                #print(agg)
                count += 1
            else:
                particleNum = findValue(t, d) # locates which particle has to move
                #print(particleNum)
                p = d[f"Particle{particleNum}"]
                if p.alive : # checks if particle is alive or not
                    unif = random.random()
                    move = movement([p.currentSite], unif)[1] # generates random direction to go in 
                    if move not in agg:
                        agg.append(move)
                        p.alive = False 
                    elif move not in activeSites:
                        activeSites.append(move)
                        activeSites.remove(p.currentSite)
                        p.currentSite = move
            #print(index)
    #print(agg)
    return agg 



def idla():

    # INITIALISATION 
    time = timeMatrix(BIRTH_SCALE)
    orderedBirth=time[0] # list of ordered birth times
    birthMatrix=time[1] # matrix of birth times of particles

    totalParticles=len(orderedBirth)

    trajectories=[ ]
    for i in range(2*WIDTH +1):
        line=[]
        for j in range(2*WIDTH +1):
            line.append([])
        trajectories.append(line)

    time = timeMatrix(TIME_SCALE)
    orderedMove=time[0] # list of ordered move times
    moveMatrix=time[1] # Matrix of move times of particles
    
    allTimes=[]
    for time in orderedBirth:
        allTimes.append(time)
    for time in orderedMove:
        allTimes.append(time)
    allTimes.sort()
    agg=[]
    activeSites=[] 
    for t in allTimes:
        fromBirth=fromWhich( t , orderedBirth, orderedMove ) 
        if(fromBirth):
            index= findValue(t, birthMatrix)
            position=[index[0],index[1]]
            activeSites.append(position)
        if(not fromBirth):
            index=findValue(t, moveMatrix)
            position=[index[0],index[1]]
            p=random.random()
            move=movement([position],p)[1]
            if move not in agg:
                agg.append(move)
            else:
                if move not in activeSites:
                    activeSites.append(move)
                    activeSites.remove(position)
                    trajectories[position[0]][position[1]] 





def process():
    if True:
        return 'yay'
    return 0


def changeCoord(i,j):
    return i+WIDTH,j+WIDTH


if __name__ == "__main__":

    print(edenDLA(False))
    
    '''
    dico = {"Particle1" : Particle(1, [0,0], [0,0], 2.3, [0,0.5], True),
            "Particle2" : Particle(2, [0,0], [0,0], 2.5, [0,0.7], True)}
    #print(findValue(2.3, dico))
    for keys in dico:
        print(keys)
        print(dico[keys].mvtTime)
        if 0.7 in dico[keys].mvtTime:
            print(dico[keys].number)
    print(process())
    '''