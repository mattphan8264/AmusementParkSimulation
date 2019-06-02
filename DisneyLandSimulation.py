import numpy as np
import matplotlib.pyplot as plt
import time

#Globals ==============================

#How big the grid will be
GridWidth = 30
GridHeight = 20
grid = np.zeros((GridWidth, GridHeight)) + 7    #grid that holds position of rides
walkGrid = np.zeros((GridWidth, GridHeight))    #grid that holds amount of people per acre

#Ride information. Each index corresponds to a single ride (i.e. index 0 in ridelocation, ID, duration, and max
#are for the same ride)
ridelocation = [[27, 18], [8, 18], [23, 7], [7, 16], [9, 17], [13, 17], [21, 15], [5, 16], [4, 16], [13, 17], 
                [13, 3], [22, 4], [17, 9], [18, 8], [1, 10], [20, 7], [20, 6], [19, 10], [18, 7], [23, 9], 
                [16, 7], [8, 10], [16, 2], [16, 8], [19, 8], [15, 7], [9, 10], [16, 5], [22, 2], [7, 10] ]
rideID = [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29]
ridePercentages = [.1263, .0944, .0788, .0707, .0654, .0593, .0590, .0562, .0537, .0352, .0348, .0268, .0236, .0228, .0213, .0197, .0161, .0146, .0137, .0131, .0131, .0119, .0107,
                    .0101, .0100, .0089, .0089, .0072, .0070, .0067]
rideMax = [163, 352, 115, 773, 128, 213, 169, 369, 261, 246, 583, 237, 184, 28, 143, 40, 27, 16, 16, 45, 60, 360, 10, 20, 16, 30, 210, 24, 19, 100]
rideDuration = [5, 10, 4, 15, 4, 5, 7, 9, 11, 8, 14, 10, 13, 3, 4, 4, 2, 2, 2, 5, 3, 18, 1, 2, 2, 3, 14, 4, 4, 10]
rideNames = ['Space Mountain', 'Indiana Jones Adventure', 'Matterhorn Bobsleds', 'Pirates of the Caribbean', 'Big Thunder Mountain Railworld', 'Autopia', 'Star Tours The Adventures Continue',
            'Haunted Mansion', 'Splash Mountain', 'Jungle Cruise', 'Its a Small World', 'Storybook Land Canal Boats', 'Finding Nemo Submarine Voyage', 'Peter Pans Flight',
            'The Many Adventures of Winnie the Pooh', 'Alice in Wonderland', 'Mad Tea Party', 'Astro Orbiter', 'Dumbo the Flying Elephant', 'Buzz Lightyear Astro Blasters', 
            'King Arthur Carrousel', 'Mark Twain Riverboat', 'Gadgets Go Coaster', 'Snow Whites Scary Adventures', 'Mr. Toads Wild Ride', 'Pinocchios Daring Journey', 'Sailing Ship Columbia'
            'Casey Jr. Circus Train', 'Roger Rabbits Car Toon Spin', 'Davy Crocketts Explorer Canoes']
nodes = [0, 1, 2, 3, 4, 5, 6]
nodeConnections = [[1], [0, 2, 4, 5], [1, 3], [2], [1], [1, 6], [5]]
rideNodeLocations = [3, 6, 2, 6, 6, 2, 2, 5, 5, 6, 4, 4, 2, 4, 5, 2, 2, 2, 4, 2, 4, 5, 4, 4, 4, 4, 5, 4, 4, 5]
nodeLocations = [[17, 19], [17, 10], [23, 10], [27, 18], [17, 3], [3, 12], [10, 16]]

rideAvailableTime = [[], [], [], [], [], [], [], [], [], [], 
                     [], [], [], [], [], [], [], [], [], [], 
                     [], [], [], [], [], [], [], [], [], []]
fastPassRides = [0, 1, 2, 4, 6, 7, 8, 10, 19, 28]

AttendeesPerHour = [300, 100, 0, 0, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
currentAttendeesPerHour = 0
maxAttendees = 500
repeatedRides = False

#Our focus group
GroupDestinations = [22, 27, 25]
GroupAmount = 3
OptimizedDestination = GroupDestinations
Entrance = [17, 19]
nodeMovement = True
TotalWalk = 0
MinWalk = 0
AverageRidesPerDay = 9
Std = 1

ShuffleAmount = 1
Repetitions = 1
PlotOn = True

#statistics
TotalWalkStepArray = []
TotalWaitStepArray = []
TotalLeaveStepArray = []
walkStepArray = []
waitStepArray = []
leaveStepArray = []

#How big the park is
DisneyLandAcres = 85
DefaultWalkTime = 0
WalkDelayAmount = 100   #How many people it takes to add delay to the group in a particular cell
AmusementParkOpenTime = 320     #how long the park stays open
MaxEnterAmount = 5  #how many people can enter the park at start
time = 0

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
    def __init__(self, ID, destinations, rideIDs, count):
        self.ID = ID
        self.Count = count
        self.Destinations = destinations
        self.RideIDList = rideIDs
        self.node = 0
        self.nextNode = 1
        self.nextNodeDestination = nodeLocations[self.nextNode]
        self.walkingTowardsNode = True
        self.FastPass = np.zeros(len(destinations))
        self.TotalSteps = 0
        
        self.totalWalkSteps = 0
        self.totalWaitSteps = 0
        self.totalLeaveSteps = 0
        
        #generating which rides have fast passes. Place holder until actual data is here
        for i in range(np.random.randint(len(destinations))):
            randomVal = np.random.randint(len(destinations))
            if (destinations[randomVal] in fastPassRides):
                self.FastPass[randomVal] = 1
        
        self.CurrentDestination = 0
        self.Status = -1
        self.Location = [17, 19]
        
        self.WalkTime = 0
        
        self.NextDestination = ridelocation[destinations[0]]
    
    
    def calculateNextNode(self):
        targetNodeInt = 0
        if self.Status == WALKING:
            targetNodeInt = self.RideIDList[self.CurrentDestination]
                
        if self.Status == WALKING or self.Status == LEAVING:
            if targetNodeInt in nodeConnections[self.node]:
                self.nextNode = targetNodeInt
            elif len(nodeConnections[self.node]) == 1:
                self.nextNode = nodeConnections[self.node][0]
            else:
                
                for i in range(len(nodeConnections[self.node])):
                    tempInt = nodeConnections[self.node][i]
                    if targetNodeInt in nodeConnections[tempInt]:
                        self.nextNode = tempInt
                    else:
                        for a in range(len(nodeConnections[tempInt])):
                            nextTempInt = nodeConnections[tempInt][a]
                            if (targetNodeInt in nodeConnections[nextTempInt]):
                                self.nextNode = nextTempInt
                            
    
    def calculateOpenRide(self):
        if (len(self.Destinations) >= self.CurrentDestination):
            return False
        tempVal = self.Destinations[self.CurrentDestination]
        if (len(rideAvailableTime[tempVal]) > 0):
            tempArr = rideAvailableTime[tempVal]
            for i in range(len(tempArr)):
                if time > tempArr[i] and time < tempArr[i + 1]:
                    difference = len(self.Destinations) - self.CurrentDestination
                    randomVal = np.random.randint(0, difference)
                    
                    if (self.CurrentDestination + randomVal < len(self.Destinations)):
                        swapVal = self.Destinations[self.CurrentDestination]
                        self.Destinations[self.CurrentDestination] = self.Desinations[self.CurrentDestination + randomVal]
                        self.Destinations[self.CurrentDestination + randomVal] = swapVal
                        
                        swapVal = self.RideIDList[self.CurrentDestination]
                        self.RideIDList[self.CurrentDestination] = self.RideIDList[self.CurrentDestination + randomVal]
                        self.RideIDList[self.CurrentDestination + randomVal] = swapVal
                        
                        self.NextDestination = ridelocation[self.Destinations[self.CurrentDestination]]

                    return False
                i += 1
        return True
        
    #Run when ride is done. If out of destinations, head towards exit    
    def rideFinished(self):
        self.CurrentDestination += 1
        if (self.CurrentDestination >= len(self.Destinations)):
            self.Status = LEAVING
            self.walkingTowardsNode = True
        else:
            #start walking, set destination to next ride location
            self.Status = WALKING
            self.NextDestination = ridelocation[self.Destinations[self.CurrentDestination]]
            if self.RideIDList[self.CurrentDestination] != self.node:
                self.calculateNextNode()
                self.walkingTowardsNode = True
            
    def freeWalk(self):
            #If leaving, head towards 0 0
        if (self.Status == LEAVING):
            if (self.Location[0] > Entrance[0]):
                self.Location[0] -= 1
            elif (self.Location[0] < Entrance[0]):
                self.Location[0] += 1
            elif (self.Location[1] > Entrance[1]):
                self.Location[1] -= 1
            elif (self.Location[1] < Entrance[1]):
                self.Location[1] += 1
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
                if (self.FastPass[self.CurrentDestination] == 1):
                    AmusementRideList[self.Destinations[self.CurrentDestination]].groupLinedUpFastPass(self.ID, self.Count)
                else:
                    AmusementRideList[self.Destinations[self.CurrentDestination]].groupLinedUp(self.ID, self.Count)
                
    def nodeAssistWalk(self):
        if (self.Location[0] > nodeLocations[self.nextNode][0]):
            self.Location[0] -= 1
        elif (self.Location[0] < nodeLocations[self.nextNode][0]):
            self.Location[0] += 1
        elif (self.Location[1] > nodeLocations[self.nextNode][1]):
            self.Location[1] -= 1
        elif (self.Location[1] < nodeLocations[self.nextNode][1]):
            self.Location[1] += 1
                    
    def nodeWalk(self):
        if (self.Status == WAITING):
            pass
        if self.Location == nodeLocations[self.nextNode]:
            self.node = self.nextNode
            if self.Status != LEAVING:
                if self.RideIDList[self.CurrentDestination] == self.node:
                    self.walkingTowardsNode = False
                    self.freeWalk()
                else:
                    self.calculateNextNode()
            else:
                self.calculateNextNode()
        else:
            self.nodeAssistWalk()
       
    #Method for walking     
    def walk(self):
        
        #If leaving and at exit, dont move anymore
        if (self.Status == LEAVING):
            if (self.Location == [17,19]):
                return False
        elif (self.Status == WALKING or self.Status == WAITING):
            if (self.ID == 0):
                self.TotalSteps += 1
                
        if (self.Status == WALKING):
            self.totalWalkSteps += 1
        elif (self.Status == WAITING):
            self.totalWaitSteps += 1
        elif (self.Status == LEAVING):
            self.totalLeaveSteps += 1
        self.WalkTime -= 1
        
        #If can walk, walk
        if (self.WalkTime <= 0):
            self.calculateOpenRide()
            walkGrid[self.Location[0]][self.Location[1]] -= self.Count
            
            if self.walkingTowardsNode == True and nodeMovement == True:
                self.nodeWalk()
            else:
                self.freeWalk()
                    
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
                
                for i in range(len(self.GroupRidingFastPass)):
                    GroupList[self.GroupRidingFastPass[i][0]].Status = RIDING
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
                
                for i in range(len(self.GroupRiding)):
                     GroupList[self.GroupRiding[i][0]].Status = RIDING
        else:
            self.CurrentTime -= 1
                
            if (self.CurrentTime <= 0):
                for i in range(len(self.GroupRiding)):
                    GroupList[self.GroupRiding[i][0]].rideFinished()

#Initialize the grid and add amusement park rides to grid
def setUpGrid():    
    for i in range(len(ridelocation)):
          #grid[ridelocation[i][0]][ridelocation[i][1]] = rideID[i]
          grid[ridelocation[i][0]][ridelocation[i][1]] = rideNodeLocations[i]
          AmusementRideList.append(AmusementRide(rideDuration[i], rideMax[i]))
    for i in range(len(nodeLocations)):
        grid[nodeLocations[i][0]][nodeLocations[i][1]] = i
          
#Initialize the group, initialize our focus group at index 0   
def initGroups():  
    nodeDestinations = []
    for a in range(len(GroupDestinations)):
        nodeDestinations.append(rideNodeLocations[GroupDestinations[a]])
    GroupList.append(Group(0, GroupDestinations, nodeDestinations, GroupAmount)) 
            
    for i in range(1, maxAttendees):
        destinations = []
        nodeDestinations = []
        
        rideCount = 0
        randomRideAmount = int(np.random.normal(AverageRidesPerDay, Std, 1))
        if (randomRideAmount < 1):
            randomRideAmount = 1
            
        if repeatedRides == True:
            rideChosen = np.random.randint(0, 30)
            for z in range(randomRideAmount):
                destinations.append(rideChosen)
                nodeDestinations.append(rideNodeLocations[rideChosen])
        else:
            while (rideCount < randomRideAmount):
                rideChosen = np.random.choice(rideID, p = ridePercentages)
                if rideChosen in destinations:
                    if np.random.randint(10) < 1:
                        destinations.append(rideChosen)
                        nodeDestinations.append(rideNodeLocations[rideChosen])
                        rideCount += 1
                else:
                    destinations.append(rideChosen)
                    nodeDestinations.append(rideNodeLocations[rideChosen])
                    rideCount += 1
        GroupList.append(Group(i, destinations, nodeDestinations, np.random.randint(1, 6)))
    

for shuffle in range(ShuffleAmount):
    
    for rep in range(Repetitions):  
        #Run for as long as park is open.
        #Every person walks, then check all rides
        setUpGrid()
        initGroups()
        
        CurrentEntered = 0
        for i in range(AmusementParkOpenTime):
            time = i
            CurrentEntered += MaxEnterAmount
            Divisor = int(i / 20)
            
            currentAttendeesPerHour += AttendeesPerHour[Divisor]
            AttendeesPerHour[Divisor] = 0
            if (CurrentEntered > currentAttendeesPerHour):
                CurrentEntered = currentAttendeesPerHour
                
            if (CurrentEntered > len(GroupList)):
                CurrentEntered = len(GroupList)
                
            for i in range(CurrentEntered):
                if (GroupList[i].Status == -1):
                    GroupList[i].Status = 0
                    walkGrid[GroupList[i].Location[0]][GroupList[i].Location[1]] += GroupList[i].Count
                GroupList[i].walk()
            
            for i in range(len(AmusementRideList)):
                AmusementRideList[i].Ride()
                AmusementRideList[i].FastPassRide()
            
            #Plot the graphs
            #1st graph is for ride locations
            #2nd graph is movement of groups    
            if (PlotOn):
                plt.clf()
                
                plt.figure(1)
                plt.imshow(grid)
                plt.axis('off')
                
                plt.figure(2)
                plt.imshow(walkGrid)
                plt.axis('off')
                
                plt.show()
                plt.pause(.1)
                
        time = 0
        walkGrid = np.zeros((GridWidth, GridHeight))
        TotalWalk += GroupList[0].TotalSteps
        
        walkStepArray.append(GroupList[0].totalWalkSteps)
        waitStepArray.append(GroupList[0].totalWaitSteps)
        leaveStepArray.append(GroupList[0].totalLeaveSteps)
        GroupList = []
        
    TotalWaitStepArray.append(waitStepArray)
    TotalLeaveStepArray.append(leaveStepArray)
    TotalWalkStepArray.append(walkStepArray)    
          
    TotalWalk = int(TotalWalk / Repetitions)
    if MinWalk == 0 or TotalWalk < MinWalk:
        MinWalkSteps = TotalWalk
        OptimizedDestinations = GroupDestinations
    TotalWalk = 0
    
    np.random.shuffle(GroupDestinations)
    
MinWalkSteps *= 2
Modulus = MinWalkSteps % 60
MinWalkSteps = int(MinWalkSteps / 60)
print('Minimum time for ride schedule = ' + str(MinWalkSteps) + 'h' + str(Modulus) + 'm')
RideString = ''
for i in range(len(OptimizedDestination)):
    RideString = RideString + str(rideNames[OptimizedDestination[i]])
    if i < len(OptimizedDestination) - 1:
        RideString += ' to '
print(RideString)
    
    
