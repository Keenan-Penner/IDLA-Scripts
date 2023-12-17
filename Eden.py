from idla_tree import *

import numpy

import matplotlib.pyplot as plt

import random

import os 

# Small scale --> more particles

BIRTH_SCALE = 5 # birth parameter 

TIME_SCALE= 0.2 # movement increment

MAX_TIME=5

WIDTH=2



class Particle:
    def __init__(self, num , bC, cS, bT, mT, alive):
        self.number = num
        self.birthCoord = bC
        self.currentSite = cS
        self.birthTime = bT
        self.mvtTime = mT
        self.alive = alive 

class Particlebis:
    def __init__(self, m, cs):
        self.moveTime = m
        self.currentSite = cs



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

# Sub optimal algorithm: too many uselessly generated particles

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


# correct version of algorithm, takes in account the memory loss property of exponentially distributed variables

def euIDLA(n):
    #INITIALIZATION
    agg = [[0,0]]
    activeSites = []
    while len(agg) < n:
        # INITIALIZING PARTICLES AND BIRTHTIMES
        d = {} # will store all info about particles
        info = [] # will store info about order in which particles need to be sent, and from where
        btimes = [] # stores all birth times
        mtimes = [] # stores all movement times
        oldAgg = agg.copy() 
        # GENERATE BIRTHTIMES FOR EACH SITE OF THE AGGREGATE
        for site in agg:
            birthTimes = poissonProcess(BIRTH_SCALE)
            btimes += birthTimes
            for t in birthTimes:
                info.append([t, site[0], site[1]]) # store info 
        info.sort(key = lambda x: x[0]) # sorted list with birthtime and corresponding birth site 
        # birthtimes have been generated for each site in the aggregate 
        # PARTICLE GENERATION 
        numParticles = len(info) # total number of particles born
        #print(f"length of birthtimes is {len(btimes)}")
        #print(f"number of born particles is {numParticles}")
        #print(len(agg)) 
        for k in range(numParticles):
            movementTimes = poissonProcess(TIME_SCALE)
            mtimes += movementTimes
            d[f"Particle{k}"] = Particle(k, info[k][1:3], info[k][1:3], info[k][0], movementTimes, False)
        times = btimes + mtimes
        #print(f"length of movement times is {len(mtimes)}")
        times.sort()
        # Particles have been generated with all necessary information
        # MAIN LOOP
        count = 0 # keeps track of number of born particles for each 'round'
        #print(len(times))
        for t in times:
            #print(t)
            fromBirth = fromWhich(t, btimes, mtimes) # returns True if t is a birth time, else False
            #print(fromBirth)
            #print(agg)
            #print(oldAgg)
            if fromBirth:
                p = d[f"Particle{count}"]
                #print(p.birthCoord)
                if p.birthCoord not in activeSites:
                    activeSites.append(p.birthCoord) # site is now listed as active
                    p.alive = True
                count += 1
            else:
                particleNum = findValue(t, d) # locates which particle has to move
                #print(particleNum)
                p = d[f"Particle{particleNum}"]
                if p.alive : # checks if particle is alive or not
                    unif = random.random() 
                    move = movement([p.currentSite], unif)[1] # generates next site the particle must visit 
                    if move not in agg:
                        agg.append(move)
                        p.alive = False # add particle to aggregate and kill the particle
                    elif move not in activeSites:
                        activeSites.append(move)
                        activeSites.remove(p.currentSite)
                        p.currentSite = move.copy()
            if oldAgg != agg:
                break
        print(len(agg))
    return agg 

#### TEST FOR OPTIMAL VERSION

def eden(n):
    agg = [[0,0]]
    activeSites = []
    while len(agg) < n:
# INITIALIZE BIRTH TIMES
        btimes = []
        mtimes = []
        info = []
        d = {}
        numActiveParticles = 0
        num = numActiveParticles.copy()
        oldAgg = agg.copy()
        for site in agg:
            birthTimes = poissonProcess(BIRTH_SCALE)
            btimes += birthTimes
            for t in birthTimes:
                info.append([t, site[0], site[1]])
        info.sort(key = lambda x: x[0])
# BIRTHTIMES ARE INITIALIZED ALONG WITH INFO ABOUT CORRESPONDING SITE
        while num == numActiveParticles: # need to regenerate times as long as no particle is born
            # also need to regenerate times and update active sites
            for index, site in enumerate(activeSites):
                movementTimes = random.exponential(TIME_SCALE)
                mtimes += movementTimes
                d[f"Particle{movementTimes}"] = Particlebis(movementTimes, site)
            mtimes.sort()
            count = 0
            for t in info:
                firstMoveTime = mtimes[count]
                site = [t[1], t[2]]
                if t[0] < firstMoveTime and site not in activeSites: # means that at time t, a new particle has to be added 
                    activeSites += site 
                    numActiveParticles += 1 
                    # need to create a moving time for this new particle
                    newMvmtTime = t + numpy.random.exponential(TIME_SCALE)
                    d[f"Particle{newMvmtTime}"] = Particlebis(newMvmtTime, site)
                elif t[0] > firstMoveTime: # means that at time t, a particle has to move
                    cs = d[f"Particle{firstMoveTime}"].currentSite # current site the particle is on 
                    unif = random.random()
                    move = movement([cs], unif)[1] # new site it will settle on 
                    if move not in agg: 
                        agg.append(move)
                        # need to create a birthtime for this particle
                    elif move not in activeSites: 
                        activeSites.append(move)
                        activeSites.remove(cs)
                        d[f"Particle{firstMoveTime}"].currentSite = move 
                    count += 1 
                break

def test(nbStep = 10000, doPlot= True, gridSize = 20): # nbStep --> number of time increments to be considered
    agg = [[0,0]]
    times = [numpy.random.exponential(BIRTH_SCALE)]
    sites = [[0,0]] 
    births = [True] # says whether or not the site is free 
    for step in range(nbStep):
        time = times[0]
        birth = births[0]
        site = sites[0]
        if birth: 
            # site = sites[0]
            if site not in agg: # cannot spawn a particle on a site that isn't in aggregate (maybe useless mais ballec)
                pass
            else:
                newTime = time + numpy.random.exponential(TIME_SCALE) # time of particle move
                times[0] = newTime
                births[0] = False
        else:
            # site = sites[0]
            unif = random.random()
            move = movement([site], unif)[1] # new site to visit 
            if move in sites:
                index = sites.index(move)
                if births[index]: # the site we want to move to is free 
                    newTime = time + numpy.random.exponential(TIME_SCALE)
                    times[0] = newTime
                    births[0] = False # site is now occupied
                    sites[0] = move 
                    times.pop(index)
                    sites.pop(index)
                    births.pop(index)
                else: # we stay on the same site
                    newTime = time + numpy.random.exponential(TIME_SCALE)
                    times[0] = newTime
                    births[0] = False 
            else:
                agg.append(move)
                newTime = time + numpy.random.exponential(BIRTH_SCALE)
                times[0] = newTime
                births[0] = True # free site  
                newTime = time + numpy.random.exponential(BIRTH_SCALE)
                times.append(newTime)
                births.append(True)
                sites.append(move) # programmed birth for site we just added to aggregate
        times, sites, births = zip(*sorted(zip(times, sites, births)))
        times = list(times)
        sites = list(sites)
        births = list(births)
        if doPlot:
            
            xline = [agg[i][0] for i in range(len(agg))]
            yline = [agg[i][1] for i in range(len(agg))]

            plt.clf()
            plt.scatter(xline, yline, s = 2, color = 'C0')
            plt.axis('square')
            plt.xlim([-gridSize, gridSize])
            plt.ylim([-gridSize, gridSize])
            plt.savefig(f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\edendla\\{step}.png")
    plt.clf()
    xline = [agg[i][0] for i in range(len(agg))]
    yline = [agg[i][1] for i in range(len(agg))]
    plt.scatter(xline, yline, s = 2, color = 'C0')
    plt.axis('square')

    maxiX = max(xline)
    miniX = min(xline)

    maxiY = max(yline)
    miniY = min(yline)

    maxi = max(abs(miniX),abs(miniY), maxiX, maxiY)

    plt.xlim([-maxi-1, maxi+1])
    plt.ylim([-maxi-1, maxi+1])
    plt.savefig(f"C:\\Users\\keena\\OneDrive\\Bureau\\Math\\Python\\edendla\\final.png")
    print(len(agg))
    return agg

if __name__ == "__main__":
    
    test(50000, False)




    '''
    A = euIDLA(150)
    xline = [A[i][0] for i in range(len(A))]
    yline = [A[i][1] for i in range(len(A))]

    maxiX = max(xline)
    miniX = min(xline)

    maxiY = max(yline)
    miniY = min(yline)

    maxi = max(abs(miniX),abs(miniY), maxiX, maxiY)
    plt.scatter(xline, yline, s = 2)
    plt.axis('square')
    plt.xlim([-maxi-1, maxi+1])
    plt.ylim([-maxi-1, maxi+1])
    plt.show()
    '''
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