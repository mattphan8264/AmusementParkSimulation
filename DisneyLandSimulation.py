import numpy as np
import matplotlib.pyplot as plt
import time

#Globals ==============================

#How big the grid will be
GridWidth = 30
GridHeight = 20
grid = np.zeros((GridWidth, GridHeight)) - 1    #grid that holds position of rides
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

fastPassRides = [0, 1, 2, 4, 6, 7, 8, 10, 19, 28]

Hours = np.arange(16) * 20
AttendeesPerHour = [300, 100, 0, 400, 100, 100, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
maxAttendees = 1000

#Our focus group
GroupDestinations = [0, 3, 2, 6, 8, 10, 15]
GroupAmount = 3
TotalWalkSteps = 0
MinWalkSteps = 0
OptimizedDestination = GroupDestinations
Entrance = [17, 19]
AverageRidesPerDay = 9
Std = 1
EntranceTime = 20

ShuffleAmount = 5
Repetitions = 10
PlotOn = False


#How big the park is
DisneyLandAcres = 85
DefaultWalkTime = 1
WalkDelayAmount = 100   #How many people it takes to add delay to the group in a particular cell
AmusementParkOpenTime = 320     #how long the park stays open
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
        self.TotalSteps = 0
        
        #generating which rides have fast passes. Place holder until actual data is here
        for i in range(np.random.randint(len(destinations))):
            randomVal = np.random.randint(len(destinations))
            if (destinations[randomVal] in fastPassRides):
                self.FastPass[randomVal] = 1
        
        self.CurrentDestination = 0
        self.Status = -1
        self.Location = [17, 19]
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
            if (self.Location == Entrance):
                return
        elif (self.Status == WALKING or self.Status == WAITING):
            if (self.ID == 0):
                self.TotalSteps += 1
        self.WalkTime -= 1
        
        #If can walk, walk
        if (self.WalkTime <= 0):
            walkGrid[self.Location[0]][self.Location[1]] -= self.Count
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
        
        rideCount = 0
        randomRideAmount = int(np.random.normal(AverageRidesPerDay, Std, 1))
        if (randomRideAmount < 1):
            randomRideAmount = 1
        while (rideCount < randomRideAmount):
            rideChosen = np.random.choice(rideID, p = ridePercentages)
            if rideChosen in destinations:
                if np.random.randint(10) < 1:
                    destinations.append(rideChosen)
                    rideCount += 1
            else:
                destinations.append(rideChosen)
                rideCount += 1
        GroupList.append(Group(i, destinations, np.random.randint(1, 6)))
    

for shuffle in range(ShuffleAmount):
    
    for rep in range(Repetitions):  
        #Run for as long as park is open.
        #Every person walks, then check all rides
        setUpGrid()
        initGroups()
        
        CurrentEntered = 0
        for i in range(AmusementParkOpenTime):
            CurrentEntered += MaxEnterAmount
            Divisor = int(i / 20)
            
            if (CurrentEntered > AttendeesPerHour[Divisor]):
                CurrentEntered = AttendeesPerHour[Divisor]
            
            if (CurrentEntered > len(GroupList)):
                CurrentEntered = len(GroupList)
               
            if ( i >= EntranceTime):
                if (GroupList[0].Status == -1):
                    GroupList[0].Status = 0
                GroupList[0].walk()
            for j in range(1, CurrentEntered):
                if (GroupList[j].Status == -1):
                    GroupList[j].Status = 0
                GroupList[j].walk()
            
            for k in range(len(AmusementRideList)):
                AmusementRideList[k].Ride()
                AmusementRideList[k].FastPassRide()
            
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
        walkGrid = np.zeros((GridWidth, GridHeight))
        TotalWalkSteps += GroupList[0].TotalSteps
        GroupList = []
          
    TotalWalkSteps = int(TotalWalkSteps / Repetitions)
    if MinWalkSteps == 0 or TotalWalkSteps < MinWalkSteps:
        MinWalkSteps = TotalWalkSteps
        OptimizedDestinations = GroupDestinations
    TotalWalkSteps = 0
    
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
    
    
