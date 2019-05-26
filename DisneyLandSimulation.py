import numpy as np
import matplotlib.pyplot as plt
import time

#Globals ==============================

#How big the grid will be
GridWidth = 10
GridHeight = 10
grid = np.zeros((GridWidth, GridHeight)) - 1    #grid that holds position of rides
walkGrid = np.zeros((GridWidth, GridHeight))    #grid that holds amount of people per acre

#Ride information. Each index corresponds to a single ride (i.e. index 0 in ridelocation, ID, duration, and max
#are for the same ride)
ridelocation = [[0, GridHeight - 1], [GridWidth - 1, 0], [GridWidth - 1, GridHeight - 1], [4, 2], [8, 7], [8, 1], [2, 5], [5, 5], [1, 3]]
rideID = [0, 1, 2, 3, 4, 5, 6, 7, 8]
rideDuration = [5, 7, 9, 4, 7, 3, 5, 4, 7]
rideMax = [5, 7, 9, 5, 7, 9, 7, 4, 3]
fastPassRides = [0, 2, 6]
maxDestinations = 3
maxAttendees = 100

#Our focus group
GroupDestinations = [0, 1, 2, 3, 4]
GroupAmount = 4

#How big the park is
DisneyLandAcres = 85
DefaultWalkTime = 1
WalkDelayAmount = 100   #How many people it takes to add delay to the group in a particular cell
AmusementParkOpenTime = 640     #how long the park stays open
MaxEnterAmount = 3  #how many people can enter the park at start

GroupList = []
AmusementRideList = []

#Status of groups. Riding is not being used, but is here in ase we need it later
WALKING = 0
WAITING = 1
RIDING = 2
LEAVING = 3
#======================================


#Represents a group
class Group:
    def __init__(self, ID, destinations, count):
        self.ID = ID
        self.Count = count
        self.Destinations = destinations
        self.FastPass = np.zeros(len(destinations))
        
        #generating which rides have fast passes. Place holder until actual data is here
        for i in range(np.random.randint(len(destinations))):
            randomVal = np.random.randint(len(rideID))
            if (destinations[randomVal] in fastPassRides):
                self.FastPass[randomVal] = 1
        
        self.CurrentDestination = 0
        self.Status = -1
        self.Location = [0, 0]
        #Adding group member count to start position
        walkGrid[self.Location[0]][self.Location[1]] += self.Count
        self.WalkTime = 0
        
        self.NextDestination = ridelocation[destinations[0]]
    
    #Run when ride is done. If out of destinations, head towards exit    
    def rideFinished(self):
        self.CurrentDestination += 1
        if (self.CurrentDestination >= len(self.Destinations)):
            self.Status = LEAVING
        else:
            #start walking, set destination to next ride location
            self.Status = WALKING
            self.NextDestination = ridelocation[self.CurrentDestination]
       
    #Method for walking     
    def walk(self):
        #If leaving and at exit, dont move anymore
        if (self.Status == LEAVING):
            if (self.Location == [0,0]):
                return
        self.WalkTime -= 1
        
        #If can walk, walk
        if (self.WalkTime <= 0):
            walkGrid[self.Location[0]][self.Location[1]] -= self.Count
            #If leaving, head towards 0 0
            if (self.Status == LEAVING):
                if (self.Location[0] > 0):
                    self.Location[0] -= 1
                elif (self.Location[1] > 0):
                    self.Location[1] -= 1
            #If walking, walk towards destination
            elif (self.Status == WALKING):
                if (self.Location[0] > self.NextDestination[0]):
                    self.Location[0] -= 1
                elif (self.Location[0] < self.NextDestination[0]):
                    self.Location[0] += 1
                elif (self.Location[1] > self.NextDestination[1]):
                    self.Location[1] -= 1
                elif (self.Location[1] < self.NextDestination[1]):
                    self.Location[1] += 1
                elif (self.Location == self.NextDestination):
                    #If arrived at destination, set to waiting and join the line of the ride
                    self.Status = WAITING
                    AmusementRideList[self.Destinations[self.CurrentDestination]].groupLinedUp(self.ID, self.Count)
                    
            walkGrid[self.Location[0]][self.Location[1]] += self.Count
            #If we moved, set walk time to new calculation
            #Calculate how long it takes to walk through current cell
            walkTime = DefaultWalkTime + (walkGrid[self.Location[0]][self.Location[1]] / WalkDelayAmount)
            self.WalkTime = walkTime            
     
#Amusement park ride   
class AmusementRide:
    #Define separate lines and rides for fastpass and non fast pass
    def __init__(self, duration, maxAttendees):
        self.Duration = duration
        self.MaxAttendees = maxAttendees
        self.GroupWaiting = []
        self.GroupWaitingFastPass = []
        
        self.GroupRiding = []
        self.GroupRidingFastPass = []
        
        self.CurrentTime = 0
        self.CurrentTimeFastPass = 0
    
    #Add group to the line    
    def groupLinedUp(self, ID, Count):
        self.GroupWaiting.append([ID, Count])
        
    def groupLinedUpFastPass(self, ID, Count):
        self.GroupWaitingFastPass.append([ID, Count])
    
    #If the ride is not going on, add people to ride and start it    
    def FastPassRide(self):
        if (self.CurrentTimeFastPass == 0):
            #If there are people waiting
            if (len(self.GroupWaitingFastPass) > 0):
                groupCount = 0
                groupAdded = 0
                #Go through groups waiting and add them
                #Once we hit a group that won't fit or we are full, start the ride
                for i in range(len(self.GroupWaitingFastPass)):
                    if (groupCount + self.GroupWaitingFastPass[i][1] <= self.MaxAttendees):
                        groupAdded += 1
                        groupCount += self.GroupWaitingFastPass[i][1]
                    else:
                        break
                self.GroupRidingFastPass = self.GroupWaitingFastPass[0:groupAdded]
                
                #Remove riders from the wait line
                if (len(self.GroupWaitingFastPass) > groupAdded):
                    self.GroupWaitingFastPass = self.GroupWaitingFastPass[groupAdded:]
                else:
                    self.GroupWaitingFastPass = []
                    
                self.CurrentTimeFastPass = self.Duration
        else:
            self.CurrentTimeFastPass -= 1
            
            #If ride is over, run ride finished for all groups that were riding    
            if (self.CurrentTimeFastPass <= 0):
                for i in range(len(self.GroupRidingFastPass)):
                    GroupList[self.GroupRidingFastPass[i][0]].rideFinished()
    #Same as fast pass ride except for this is non fast pass    
    def Ride(self):
        if (self.CurrentTime == 0):
            if (len(self.GroupWaiting) > 0):
                groupCount = 0
                groupAdded = 0
                for i in range(len(self.GroupWaiting)):
                    if (groupCount + self.GroupWaiting[i][1] <= self.MaxAttendees):
                        groupAdded += 1
                        groupCount += self.GroupWaiting[i][1]
                    else:
                        break
                self.GroupRiding = self.GroupWaiting[0:groupAdded]
                
                if (len(self.GroupWaiting) > groupAdded):
                    self.GroupWaiting = self.GroupWaiting[groupAdded:]
                else:
                    self.GroupWaiting = []
                    
                self.CurrentTime = self.Duration
        else:
            self.CurrentTime -= 1
                
            if (self.CurrentTime <= 0):
                for i in range(len(self.GroupRiding)):
                    GroupList[self.GroupRiding[i][0]].rideFinished()

#Initialize the grid and add amusement park rides to grid
def setUpGrid():
    for i in range(len(ridelocation)):
          grid[ridelocation[i][0]][ridelocation[i][1]] = rideID[i]
          AmusementRideList.append(AmusementRide(rideDuration[i], rideMax[i]))
          
#Initialize the group, initialize our focus group at index 0   
def initGroups():  
    GroupList.append(Group(0, GroupDestinations, GroupAmount)) 
            
    for i in range(1, maxAttendees):
        destinations = []
        for a in range(1, np.random.randint(2, maxDestinations)):
            destinations.append(rideID[np.random.randint(len(rideID))])
        GroupList.append(Group(i, destinations, np.random.randint(1, 6)))
    
setUpGrid()
initGroups()

CurrentEntered = 0

#Run for as long as park is open.
#Every person walks, then check all rides
for i in range(AmusementParkOpenTime):
    CurrentEntered += MaxEnterAmount
    if (CurrentEntered > len(GroupList)):
        CurrentEntered = len(GroupList)
        
    for i in range(CurrentEntered):
        if (GroupList[i].Status == -1):
            GroupList[i].Status = 0
        GroupList[i].walk()
    
    for i in range(len(AmusementRideList)):
        AmusementRideList[i].Ride()
        AmusementRideList[i].FastPassRide()
    
    #Plot the graphs
    #1st graph is for ride locations
    #2nd graph is movement of groups    
    plt.clf()
    
    plt.figure(1)
    plt.imshow(grid)
    plt.axis('off')
    
    plt.figure(2)
    plt.imshow(walkGrid)
    plt.axis('off')
    
    plt.show()
    plt.pause(.5)
    
    