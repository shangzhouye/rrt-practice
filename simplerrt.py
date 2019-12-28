# The RRT challenge by Shangzhou on Sep. 12
# Last updated: Sep. 19

# add the collision circles and draw them
# check collision function
# search for the path function

import numpy as np 
import random
from matplotlib import pyplot as plt

class rrt:
    # initialize the data list
    def __init__(self, delta = 1, initialloc = [50,50], domainwid = 100, domainhei = 100, goalloc = [100,100]):
        self.delta = delta
        self.domainwidth = domainwid
        self.domainheight = domainhei
        self.goallocation = np.array(goalloc)
        self.rrtdata = [[np.array(initialloc),[]]]

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

    # def trytoconnect

    # add a new point to the tree
    def addnewpoint(self, oldindex, oldpoint, randompoint):
        newpoint = oldpoint + ((randompoint - oldpoint) / np.linalg.norm(randompoint - oldpoint)) * self.delta
        newindex = len(self.rrtdata)
        self.rrtdata[oldindex][1].append(newindex)
        self.rrtdata.append([newpoint,[]])
        return newindex, newpoint
    
    # plot the tree
    def plottree(self, oldpoint, newpoint):
        plt.scatter(oldpoint[0], oldpoint[1], color = '#337AB7', linewidth=2)
        plt.scatter(newpoint[0], newpoint[1], color = '#337AB7', linewidth=2)
        plt.plot([oldpoint[0], newpoint[0]], [oldpoint[1], newpoint[1]], color = '#4F4F4F', linewidth=2)

    

# establish the data list
myrrt = rrt()
random.seed(99)
myrrt.delta = 1

# starting the loop here
for k in range(500):
    mypoint = myrrt.randompoint()
    nearestid, nearestpoint = myrrt.nearestvertex(mypoint)
    addedid, addedpoint = myrrt.addnewpoint(nearestid, nearestpoint, mypoint)
    myrrt.plottree(nearestpoint, addedpoint)


# show the plot
plt.title('The RRT Tree')
plt.ylabel('Y axis')
plt.xlabel('X axis')
# plt.xlim(0, 100)
# plt.ylim(0, 100)
plt.show()