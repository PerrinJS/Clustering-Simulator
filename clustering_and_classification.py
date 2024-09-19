#!/usr/bin/python
import random
import math
import colorsys

import color_and_position_conversion as CAPConv

def _argmin(in_list):
    curr_min_pair = (None, None)
    for i, value in enumerate(in_list):
        if curr_min_pair[0] is None or curr_min_pair[0] > value:
            curr_min_pair = (value, i)

    return curr_min_pair[1]

def _calculate_centroid(cluster):
    running_x_sum, running_y_sum = (0, 0)
    assert len(cluster) > 0
    for point in cluster:
        running_x_sum += point[0]
        running_y_sum += point[1]
    adverage_pos = (running_x_sum/len(cluster), running_y_sum/len(cluster))
    centroid_idx = _argmin(list([math.dist(adverage_pos, point) for point in cluster]))
    centroid = cluster[centroid_idx]
    return centroid

class KNearestNeighbor:
    """This uses the euclidian distance as the distance metric
       Data must be a list of float values"""

    class ClusteredPointRelativeDistance:
        def __init__(self, point, cluster_id, distance):
            self.point = point
            self.cluster_id = cluster_id
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

    def __init__(self, num_neighbours = 3, clustered_data = None):
        self.num_neighbours = num_neighbours
        self.clustered_data = clustered_data
        self.num_data_points = 0
        for i in self.clustered_data:
            self.num_data_points += len(i)

    def clasify_point(self, point):
        if self.clustered_data is None:
            raise ValueError("self.clustered_data cannot be None")
        if self.num_data_points < self.num_neighbours:
            raise ValueError("You can't have more neighbours then data points")

        #Majoirity voting with random tie breaker
        #start checking against the shortest distance found so far.
        #If it's smaller than that the repleace that element in that index of the list.
        #If not check the next smallest element if it's smaller then that put
        #the current one in that position ect.
        #i in this case is the cluster id
        ordered_nearest_neighbors = []
        for i, cluster in enumerate(self.clustered_data):
            for clustered_point in cluster:
                curr_point = self.ClusteredPointRelativeDistance(clustered_point, i,\
                                                                math.dist(clustered_point, point))
                j = 0
                for neighbor in ordered_nearest_neighbors:
                    if neighbor > curr_point:
                        break
                    j += 1
                #Less then because if we went through all of ordered_nearest_neighbors
                #then j == its lenth
                if j < len(ordered_nearest_neighbors):
                    ordered_nearest_neighbors[j] = curr_point

        #now we have a short list of close points we do a majority vote
        class_vote_list = []
        for _ in range(0,len(self.clustered_data)):
            class_vote_list.append(0)
        for close_point in ordered_nearest_neighbors:
            class_vote_list[close_point.cluster_id] += 1
        heighest_vote = (-1, -1)
        for i, class_vote in enumerate(class_vote_list):
            if heighest_vote[0] < class_vote:
                heighest_vote = (class_vote, i)
            elif heighest_vote[0] == class_vote:
                if random.random() > .5:
                    heighest_vote = (class_vote, i)

        #return the class id of the heightest vote
        return heighest_vote[1]


class KMeansClusterer:
    def __init__(self, num_neighbours = 3, data = None):
        """Data should be a list of vectors in the case of this project hsv
        values with the 'value' in hsv being ignored."""
        self.num_neighbours = num_neighbours
        self.data = data
        self.clustered_data = None
        self.centroids = None

    def convert_pos_to_hsv(c_list):
        output = []
        for color in c_list:
            output.append(CAPConv.pos_to_polar(color, None))
        return output

    def convert_clusters_to_hsv(clust_list):
        output = []
        for cluster in clust_list:
            output.append(KMeansClusterer.convert_pos_to_hsv(cluster))
        return output

    def generate_labels(self):
        if len(self.data) < self.num_neighbours:
            raise ValueError("You can't have more neighbours then data points")

        random.shuffle(self.data)

        clusters = [[] for _ in range(self.num_neighbours)]
        centroids_pos = []
        euclidian_centroids = []
        euclidian_points = [CAPConv.polar_to_pos(point) for point in self.data]
        #Randomly select unique points to use as centroids
        for _ in range(self.num_neighbours):
            centroids_pos_tmp = random.randrange(0, len(self.data))
            #Make sure it's not already selected
            while centroids_pos_tmp in centroids_pos:
                centroids_pos_tmp = random.randrange(0, len(self.data))
            centroids_pos.append(centroids_pos_tmp)
            euclidian_centroids.append(euclidian_points[centroids_pos_tmp])

        converged = False
        while not converged:
            clusters = [[] for _ in range(self.num_neighbours)]

            for point in euclidian_points:
                #point is x1 centroid is x2
                #For each point find the distance to each centroid.
                #Then find which distance is smallest.
                #Next set that point as being part of that closest centroids cluster.
                distances_to_centroids = [math.dist(point, centroid)\
                                        for centroid in euclidian_centroids]
                smallest_distance_pos = _argmin(distances_to_centroids)
                clusters[smallest_distance_pos].append(point)

            #generate the new centroids based off the new classifications
            new_centroids = [_calculate_centroid(cluster) for cluster in clusters]

            new_centroids_sorted = new_centroids.copy()
            euclidian_centroids_sorted = euclidian_centroids.copy()
            converged = new_centroids_sorted.sort() == euclidian_centroids_sorted.sort()
            euclidian_centroids = new_centroids

        self.clustered_data = clusters
        self.centroids = euclidian_centroids

    def get_clusters(self):
        if self.clustered_data is None:
            self.generate_labels()
        return KMeansClusterer.convert_clusters_to_hsv(self.clustered_data)

    def get_centroids(self):
        if self.centroids is None:
            self.generate_labels()
        return KMeansClusterer.convert_pos_to_hsv(self.centroids)


class KMeansClustererRGB(KMeansClusterer):

    def convert_hsv_clusters_to_rgb(hsv_clusters):
        output_list = []
        for cluster in hsv_clusters:
            output_list.append(KMeansClustererRGB.convert_hsv_list_to_rgb(cluster))

        return output_list

    def convert_hsv_list_to_rgb(hsv_list):
        rgb_list = []
        for element in hsv_list:
            h,s = element
            v=1
            rgb_list.append(colorsys.hsv_to_rgb(h,s,v))

        return rgb_list

    def __init__(self, data):
        hsv_converted_points = [colorsys.rgb_to_hsv(r,g,b) for r,g,b in data]
        self.clustered_data_rgb = None
        self.centroids_rgb = None
        super().__init__(data=hsv_converted_points)

    def get_clusters(self):
        if self.clustered_data_rgb is None:
            hsv_clusters = super().get_clusters()
            self.clustered_data_rgb = KMeansClustererRGB.convert_hsv_clusters_to_rgb(hsv_clusters)
        return self.clustered_data_rgb

    def get_centroids(self):
        if self.centroids_rgb is None:
            hsv_centroids = super().get_centroids()
            self.centroids_rgb = KMeansClustererRGB.convert_hsv_list_to_rgb(hsv_centroids)
        return self.centroids_rgb

if __name__ == '__main__':
    from color_and_position_conversion import pos_to_polar
    #thing = NearestNeighbor(3, None)
    points = []
    for _ in range(20):
        points.append((random.randrange(1, 500), random.randrange(1,500)))
    randPointsPolar = [pos_to_polar(point, (250,250)) for point in points]

    clusterer = KMeansClusterer(data = randPointsPolar)
    clusters = clusterer.get_clusters()
    point = (random.randrange(1, 500), random.randrange(1,500))
    point = pos_to_polar(point, (250,250))
    nearestNeighborFinder = KNearestNeighbor(clustered_data = clusters)
    pointsCluster = nearestNeighborFinder.clasify_point(point)
    print(str(point) + "\n" + str(clusters[pointsCluster]) + "\n\n" + str(clusters))

    calc_centroid_list = [(1,1), (2,2), (3,3)]
    calc_centroid = _calculate_centroid(calc_centroid_list)
    print(str(calc_centroid) + ' == (2,2)')
    print(str(calc_centroid_list[1]) + ' == ' +\
          str(calc_centroid_list[calc_centroid_list.index((2,2))]))
    assert _calculate_centroid([(1,1), (2,2), (3,3)]) == (2,2)

    #Check the conversion of the values
    cluterer = KMeansClusterer(data = calc_centroid_list)
    clusters = cluterer.get_clusters()
    print(clusters)
