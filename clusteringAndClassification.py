#!/usr/bin/python
import random
import math

import ColorAndPositionConversion as CAPConv

def _argmin(inList):
    currMinPair = (None, None)
    for i, value in enumerate(inList):
        if currMinPair[0] is None or currMinPair[0] > value:
            currMinPair = (value, i)

    return currMinPair[1]

def _calculateCentroid(cluster):
    runningXSum, runningYSum = (0, 0)
    assert(len(cluster) > 0)
    for point in cluster:
        runningXSum += point[0]
        runningYSum += point[1]
    adveragePos = (runningXSum/len(cluster), runningYSum/len(cluster))
    centroid = _argmin(list([math.dist(adveragePos, point) for point in cluster]))
    return centroid

class KNearestNeighbor:
    """This uses the euclidian distance as the distance metric
       Data must be a list of float values"""

    class ClusteredPointRelativeDistance:
        def __init__(self, point, clusterID, distance):
            self.point = point
            self.clusterID = clusterID
            self.distance = distance

        #TODO: add all sorts of type checking etc to thease comparitors

        def __gt__(self, o):
            if self.distance > o.distance:
                return True
            return False

        def __lt__(self, o):
            if self.distance < o.distance:
                return True
            return False

        def __eq__(self, o):
            if self.distance == o.distance:
                return True
            return False

    def __init__(self, numNeighbours = 3, clusteredData = None):
        self.numNeighbours = numNeighbours
        self.clusteredData = clusteredData
        self.numDataPoints = 0
        for i in self.clusteredData:
            self.numDataPoints += len(i)

    def clasifyPoint(self, point):
        if self.clusteredData is None:
            raise ValueError("self.clusteredData cannot be None")
        if self.numDataPoints < self.numNeighbours:
            raise ValueError("You can't have more neighbours then data points")

        #Majoirity voting with random tie breaker
        #start checking against the shortest distance found so far.
        #If it's smaller than that the repleace that element in that index of the list.
        #If not check the next smallest element if it's smaller then that put
        #the current one in that position ect.
        #i in this case is the cluster id
        orderedNearestNeighbors = []
        for i, cluster in enumerate(self.clusteredData):
            for clusteredPoint in cluster:
                currPoint = self.ClusteredPointRelativeDistance(clusteredPoint, i, math.dist(clusteredPoint, point))
                j = 0
                for neighbor in orderedNearestNeighbors:
                    if neighbor > currPoint:
                        break
                    j += 1
                #Less then because if we went through all of orderedNearestNeighbors then j == its lenth
                if j < len(orderedNearestNeighbors):
                    orderedNearestNeighbors[j] = currPoint

        #now we have a short list of close points we do a majority vote
        classVoteList = []
        for _ in range(0,len(self.clusteredData)):
            classVoteList.append(0)
        for closePoint in orderedNearestNeighbors:
            classVoteList[closePoint.clusterID] += 1
        heighestVote = (-1, -1)
        for i, classVote in enumerate(classVoteList):
            if heighestVote[0] < classVote:
                heighestVote = (classVote, i)
            elif heighestVote[0] == classVote:
                if random.random() > .5:
                    heighestVote = (classVote, i)

        #return the class id of the heightest vote
        return heighestVote[1]


class KMeansClusterer:
    def __init__(self, numNeighbours = 3, data = None):
        """Data should be a list of vectors in the case of this project hsv values with the 'value' in hsv being ignored."""
        self.numNeighbours = numNeighbours
        self.data = data
        self.clusteredData = None
        self.centroids = None

    def generateLabels(self):
        if len(self.data) < self.numNeighbours:
            raise ValueError("You can't have more neighbours then data points")

        random.shuffle(self.data)

        clusters = [[] for _ in range(self.numNeighbours)]
        centroidsPos = list()
        euclidianCentroids = list()
        euclidianPoints = [CAPConv.polarToPos(point) for point in self.data]
        #Randomly select unique points to use as centroids
        for _ in range(self.numNeighbours):
            centroidsPosTmp = random.randrange(0, len(self.data))
            #Make sure it's not already selected
            while centroidsPosTmp in centroidsPos:
                centroidsPosTmp = random.randrange(0, len(self.data))
            centroidsPos.append(centroidsPosTmp)
            euclidianCentroids.append(euclidianPoints[centroidsPosTmp])

        converged = False
        while not converged:
            clusters = [[] for _ in range(self.numNeighbours)]

            for point in euclidianPoints:
                #point is x1 centroid is x2
                #For each point find the distance to each centroid.
                #Then find which distance is smallest.
                #Next set that point as being part of that closest centroids cluster.
                distancesToCentroids = [math.dist(point, centroid) for centroid in euclidianCentroids]
                smallestDistancePos = _argmin(distancesToCentroids)
                clusters[smallestDistancePos].append(point)

            #generate the new centroids based off the new classifications
            newCentroids = [_calculateCentroid(cluster) for cluster in clusters]

            converged = newCentroids.sort() == euclidianCentroids.sort()
            euclidianCentroids = newCentroids

        self.clusteredData = clusters
        self.centroids = euclidianCentroids


    def getClusters(self):
        if self.clusteredData is None:
            self.generateLabels()
        return self.clusteredData

    def getCentroids(self):
        if self.centroids is None:
            self.generateLabels()
        return self.centroids



if __name__ == '__main__':
    from ColorAndPositionConversion import posToPolar
    #thing = NearestNeighbor(3, None)
    points = []
    for _ in range(20):
        points.append((random.randrange(1, 500), random.randrange(1,500)))
    randPointsPolar = [posToPolar(point, (250,250)) for point in points]

    clusterer = KMeansClusterer(data = randPointsPolar)
    clusters = clusterer.getClusters()
    point = (random.randrange(1, 500), random.randrange(1,500))
    point = posToPolar(point, (250,250))
    nearestNeighborFinder = KNearestNeighbor(clusteredData = clusters)
    pointsCluster = nearestNeighborFinder.clasifyPoint(point)
    print(str(point) + "\n" + str(clusters[pointsCluster]) + "\n\n" + str(clusters))
