# The RRT challenge by Shangzhou on Sep. 12
# Last updated: Sep. 21


import numpy as np 
import random
from matplotlib import pyplot as plt

# calculate minimum distance from point to line segment
def pointtolinedist(point, line):
    if line[0][0] > line[1][0]:
        line[0], line[1] = line[1], line[0]
    # calculate three distances
    pointtoline = np.linalg.norm(np.cross(point - line[0], line[1] - line[0]))/np.linalg.norm(line[1]-line[0])
    pointtoleft = ((point[0] - line[0][0]) ** 2 + (point[1] - line[0][1]) ** 2) ** 0.5
    pointtoright = ((point[0] - line[1][0]) ** 2 + (point[1] - line[1][1]) ** 2) ** 0.5
    # calculate the intersection (after a long long hand calculation)
    m = line[1][0] - line[0][0]
    n = line[1][1] - line[0][1]
    intersection_x = (m ** 2 * point[0] + m * n * point[1] + n ** 2 * line[0][0] - m * n * line[0][1]) / (n ** 2 + m ** 2) 
    if intersection_x < line[0][0]:
        return pointtoleft
    elif intersection_x > line[1][0]:
        return pointtoright
    else:
        return pointtoline

class rrt(object):
    # initialize the data list
    def __init__(self, delta = 1, initialloc = [60,80], domainwid = 100, domainhei = 100, goalloc = [90,25]):
        self.delta = delta
        self.domainwidth = domainwid
        self.domainheight = domainhei
        self.goallocation = np.array(goalloc)
        self.initiallocation = np.array(initialloc)
        self.rrtdata = [[np.array(initialloc),[]]]
        self.circleobstacles = [[np.array([30,40]),5],\
                                [np.array([10,25]),5],\
                                [np.array([10,79]),10],\
                                [np.array([70,40]),20],\
                                [np.array([40,60]),5],\
                                [np.array([80,80]),10],\
                                [np.array([50,50]),10]]
        self.finalpath = []

    # choose a random point
    def randompoint(self):
        while True:
            chosenpoint = np.array([random.uniform(0,self.domainwidth),random.uniform(0,self.domainheight)])
            if self.checksamepoints(chosenpoint) == False:
                break
        return chosenpoint
    
    def checksamepoints(self, checkpoint):
        for i in range(len(self.rrtdata)):
            if list(self.rrtdata[i][0]) == list(checkpoint):
                return True
        return False

    # find the nearest vertex
    def nearestvertex(self, checkpoint):
        nearestindex = 0
        nearestdistance = 200
        for i in range(len(self.rrtdata)):
            distance = ((self.rrtdata[i][0][0] - checkpoint[0]) ** 2 + (self.rrtdata[i][0][1] - checkpoint[1]) ** 2) ** 0.5
            if distance < nearestdistance:
                nearestdistance = distance
                nearestindex = i
        return nearestindex, self.rrtdata[nearestindex][0]

    # check for collision, if collision, return True
    def checkcollision(self, point1, point2):
        for i in self.circleobstacles:
            if pointtolinedist(i[0], [point1, point2]) < i[1]:
                return True
        return False
        

    # find the new point
    def findnewpoint(self, oldpoint, randompoint):
        newpoint = oldpoint + ((randompoint - oldpoint) / np.linalg.norm(randompoint - oldpoint)) * self.delta
        return newpoint

    # add the new point to the tree
    def addnewpoint(self, oldindex, newpoint):
        newindex = len(self.rrtdata)
        self.rrtdata[oldindex][1].append(newindex)
        self.rrtdata.append([newpoint,[]])
        return newindex, newpoint

    # find the last point with the current idx
    def findlastpoint(self, currentindex):
        for x in range(len(self.rrtdata)):
            for y in self.rrtdata[x][1]:
                if y == currentindex:
                    return x, self.rrtdata[x][0]
        return "Cannot find the point.", "Some errors here."
    
    # plot the tree
    def plottree(self, oldpoint, newpoint, defcolor = '#337AB7', linewid = 1):
        plt.plot([oldpoint[0], newpoint[0]], [oldpoint[1], newpoint[1]], color = defcolor, linewidth=linewid)

    # plot obstacles
    def plotobstacles(self):
        for i in self.circleobstacles:
            circle = plt.Circle(i[0], i[1], color='#4F4F4F')
            plt.gcf().gca().add_artist(circle)
    

# establish the data list
myrrt = rrt()
random.seed(96) #99, 98, 97

# starting the searching loop here
for k in range(5000):
    mypoint = myrrt.randompoint()
    nearestid, nearestpoint = myrrt.nearestvertex(mypoint)
    newpoint = myrrt.findnewpoint(nearestpoint, mypoint)
    if myrrt.checkcollision(nearestpoint, newpoint) == False:
        addedid, addedpoint = myrrt.addnewpoint(nearestid, newpoint)
        myrrt.plottree(nearestpoint, addedpoint)
        if myrrt.checkcollision(addedpoint, myrrt.goallocation) == False:
            break
else:
    print("No path found within K iterations")

# find the final path
currentidx = addedid
currentpoint = addedpoint
plt.scatter(myrrt.goallocation[0], myrrt.goallocation[1], color = 'red', linewidth=1)
myrrt.plottree(currentpoint, myrrt.goallocation, defcolor = 'red', linewid=1)
while True:
    lastidx, lastpoint = myrrt.findlastpoint(currentidx)
    myrrt.finalpath.append([currentpoint, lastpoint])
    myrrt.plottree(currentpoint, lastpoint, defcolor = 'red', linewid=1)
    currentidx, currentpoint = lastidx, lastpoint
    if list(lastpoint) == list(myrrt.initiallocation):
        plt.scatter(lastpoint[0], lastpoint[1], color = 'red', linewidth=1)
        break

# show the plot
myrrt.plotobstacles()
plt.title('The RRT Tree')
plt.ylabel('Y axis')
plt.xlabel('X axis')
plt.xlim(0, 100)
plt.ylim(0, 100)
plt.show()