import cluster
import math


class AgglomerativeClustering:

    def __init__(self, link, samples):
        self.samples = samples
        self.link = link
        self.clusters = [cluster.Cluster(sample.s_id, [sample]) for sample in samples]

    def compute_silhouette(self, matrix):
        """
        computes silhouette value(float) of every sample in the dataset
        :param matrix: distance matrix between samples in the data(dictionary)
        :return: returns a dictionary of sample and its silhouette value(dictionary)
        """
        sil_dict = {}
        for clus in self.clusters:
            for sample in clus.samples:  # iterate over every sample in the dataset
                sum_dist = 0
                for other in clus.samples:  # iterate over every other sample in the same cluster
                    if sample.s_id > other.s_id:
                        sum_dist += matrix[(sample.s_id, other.s_id)]
                    elif sample.s_id < other.s_id:
                        sum_dist += matrix[(other.s_id, sample.s_id)]
                if len(clus.samples) > 1:
                    sil_in = float(sum_dist / (len(clus.samples) - 1))
                else:  # when a sample is the only one in the cluster, its silhouette in value is 0
                    sil_in = 0

                dist_to_clus = []
                for other_clus in self.clusters:  # iterate over other clusters
                    if other_clus == clus:
                        continue
                    sum_dist = 0
                    for other in other_clus.samples:  # iterate over every other sample in other clusters
                        if sample.s_id > other.s_id:
                            sum_dist += matrix[(sample.s_id, other.s_id)]
                        else:
                            sum_dist += matrix[(other.s_id, sample.s_id)]
                    # save the distance from the sample to every other cluster
                    dist_to_clus.append(float(sum_dist / (len(other_clus.samples))))
                sil_out = min(dist_to_clus)
                if sil_in == 0:
                    sil_dict[sample.s_id] = 0
                else:
                    sil_dict[sample.s_id] = float((sil_out - sil_in) / (max(sil_out, sil_in)))

        return sil_dict

    def compute_summery_silhouette(self, matrix):
        """
        computes silhouette value(float) of every cluster and for the whole dataset
        :param matrix: distance matrix between samples in the data(dictionary)
        :return: returns a dictionary of cluster(or the whole dataset) and its silhouette value(dictionary)
        """
        samples_dict = self.compute_silhouette(matrix)  # holds the samples silhouette dictionary
        sum_total = 0
        clus_dict = {}
        for clus in self.clusters:
            sum_clus = 0
            for sample in clus.samples:
                sum_clus += samples_dict[sample.s_id]
                sum_total += samples_dict[sample.s_id]
            # save each cluster's silhouette
            clus_dict[clus.c_id] = format(round(float(sum_clus) / len(clus.samples), 3), '.3f')
        clus_dict[0] = format(round(float(sum_total / len(self.samples)), 3), '.3f')  # save the dataset silhouette
        return clus_dict

    def compute_rand_index(self):
        """
        computes random index value(float) of the whole dataset
        :return: returns the random index value(float) of the whole dataset
        """
        tp = 0
        tn = 0
        number_of_pairs = math.factorial(len(self.samples)) / (2 * math.factorial(len(self.samples) - 2))
        for clus in self.clusters:
            for sample in clus.samples:  # iterate over every sample in the dataset
                for other in clus.samples:  # iterate over every other sample in the same cluster
                    if sample.s_id >= other.s_id:
                        continue
                    if sample.label == other.label:  # two samples were clustered correctly into the same cluster
                        tp += 1

                for other_clus in self.clusters:  # iterate over other clusters
                    if other_clus == clus:
                        continue
                    for other in other_clus.samples:  # iterate over every other sample in other clusters
                        if sample.s_id > other.s_id:  # avoid duplicate check
                            continue
                        if sample.label != other.label:  # two samples were clustered correctly into different clusters
                            tn += 1

        return format(round(float((tp + tn) / number_of_pairs), 3), '.3f')

    def matrix_dist(self):
        """
        computes distances(float) between each pair of samples in the dataset
        :return: returns a distances dictionary in format: key=(first_id, second_id), value=distance
        """
        matrix_dic = {}
        for clus in self.clusters:
            for other_clus in self.clusters:
                if clus.samples[0].s_id > other_clus.samples[0].s_id:  # avoid duplicates
                    matrix_dic[(clus.samples[0].s_id, other_clus.samples[0].s_id)] = clus.samples[0]\
                        .compute_euclidean_distance(other_clus.samples[0])
        return matrix_dic

    def run(self, max_clusters):
        """
        runs the agglomerative clustering on the dataset and prints its results
        :param max_clusters: number of clusters to stop clustering
        """
        sample_dist_matrix = self.matrix_dist()
        self.link.print_link()
        first_clus = self.clusters[0]  # initialize first cluster to merge into
        second_clus = self.clusters[0]  # initialize second cluster to merge
        max_samples_dist = max(sample_dist_matrix.values())
        # initialize minimun distance between two samples
        min_dist = max_samples_dist
        while len(self.clusters) > max_clusters:  # clustering loop
            for clus in self.clusters:  # iterate over every cluster
                for other_clus in self.clusters:  # iterate over other clusters
                    if clus.c_id > other_clus.c_id:  # avoid duplicates and make sure to pass correct key to dictionary
                        # compute distance between two clusters according to current link
                        clus_dist = self.link.compute(clus, other_clus, sample_dist_matrix)
                        if clus_dist < min_dist:  # keep the minimum distance and its clusters
                            min_dist = clus_dist
                            first_clus = other_clus
                            second_clus = clus
            self.clusters.remove(second_clus)  # remove the cluster that's getting merged from clusters list
            first_clus.merge(second_clus)  # merge the cluster with higher id into the other
            min_dist = max_samples_dist  # restore high distance in order to start the search again

        sum_sil = self.compute_summery_silhouette(sample_dist_matrix)
        # print results
        for clus in self.clusters:
            clus.print_details(sum_sil[clus.c_id])
        print(f'Whole data: silhouette = {sum_sil[0]}, RI = {self.compute_rand_index()}')
