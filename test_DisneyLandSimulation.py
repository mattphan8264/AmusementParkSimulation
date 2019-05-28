import DisneyLandSimulation as D
import numpy as np


def checkFloat(float1, float2, t=1e-10):
    """Compare two floats"""
    return abs(float1 - float2) < t


class TestGroup:
    """Test suite for the Group class"""

    def setup_method(self):
        """Setups simple grid and rides for testing each method"""
        D.GridWidth = 30
        D.GridHeight = 20
        D.grid = (
            np.zeros((D.GridWidth, D.GridHeight)) - 1
        )  # grid that holds position of rides
        D.walkGrid = np.zeros(
            (D.GridWidth, D.GridHeight)
        )  # grid that holds amount of people per acre
        D.ridelocation = [[2, 0], [1, 1], [0, 2]]
        D.rideDuration = [1, 2, 3]
        D.rideID = [0, 1, 2]
        D.rideDuration = [1, 2, 3]
        D.rideMax = [5, 7, 9]
        D.fastPassRides = [0]
        self.group = D.Group(1, [1, 0, 2], 5)
        self.group.Location = [0, 0]
        D.walkGrid[0, 0] = 5

    def test_init(self):
        """Test constructor for group"""
        assert self.group.ID == 1
        assert self.group.Count == 5
        assert self.group.Destinations == [1, 0, 2]
        assert self.group.CurrentDestination == 0
        assert self.group.Status == -1
        assert self.group.WalkTime == 0
        assert D.walkGrid[0, 0] == 5
        assert self.group.NextDestination == D.ridelocation[1]

    def test_rideFinished_less(self):
        """Tests rideFinshed when there are still rides left"""
        # current less than length
        self.group.rideFinished()
        assert self.group.CurrentDestination == 1
        assert self.group.Status == D.WALKING
        assert self.group.NextDestination == D.ridelocation[1]

    def test_rideFinished_equal(self):
        """Tests rideFinshed when there just left last ride"""
        # current equal to length
        self.group.CurrentDestination = 2
        self.group.rideFinished()
        assert self.group.CurrentDestination == 3
        assert self.group.Status == D.LEAVING

    def test_rideFinished_greater(self):
        """Tests rideFinshed when currentDestination greater than total"""
        # current greater than length
        self.group.CurrentDestination = 3
        self.group.Status == D.WALKING
        self.group.rideFinished()
        assert self.group.CurrentDestination == 4
        assert self.group.Status == D.LEAVING

    def test_walk_walking(self):
        """Tests walk when walking toward a ride"""
        # walk towards ride
        self.group.Status = D.WALKING
        self.group.walk()
        assert D.walkGrid[0, 0] == 0
        assert D.walkGrid[1, 0] == 5
        assert self.group.Location == [1, 0]
        assert self.group.Status == D.WALKING
        assert checkFloat(
            self.group.WalkTime, 5 / D.WalkDelayAmount + D.DefaultWalkTime
        )

    def test_walk_walkTime(self):
        """Tests walk when waiting for walk time"""
        # walk time
        self.group.Status = D.WALKING
        self.group.WalkTime = 1.05
        oldWalkTime = self.group.WalkTime
        self.group.walk()
        assert checkFloat(oldWalkTime - 1, self.group.WalkTime)
        assert self.group.CurrentDestination == 0
        assert self.group.Location == [0, 0]
        assert self.group.Status == D.WALKING
        assert D.walkGrid[0, 0] == 5

    def test_walk_wait(self):
        """Tests walk when waiting for ride"""
        self.group.Status = D.WALKING
        self.group.Location = [1, 1]
        D.walkGrid[1, 1] = 5
        self.group.walk()
        assert self.group.Status == D.WAITING
        assert self.group.Location == [1, 1]
        assert D.walkGrid[1, 1] == 5

    def test_walk_leave(self):
        """Tests walk when leaving and at exit"""
        self.group.Status = D.LEAVING
        self.group.Location = D.Entrance
        self.group.walk()
        assert self.group.Location == D.Entrance
        assert self.group.Status == D.LEAVING
