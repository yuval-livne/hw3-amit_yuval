import abc


class Link:
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def compute(self, cluster, other, matrix):
        pass


class SingleLink:
    def __init__(self):
        pass

    def compute(self, cluster, other, matrix):
        """
        computes distance between two clusters according to simple link and returns it
        :param cluster: first cluster to compute distance from(cluster)
        :param other: second cluster to compute distance to(cluster)
        :param matrix: distance matrix between samples in the data(dictionary)
        :return: returns the distance(float)
        """
        min = matrix[(cluster.samples[0].s_id, other.samples[0].s_id)]
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                if sample_cluster.s_id > sample_other.s_id:
                    current_dist = matrix[(sample_cluster.s_id, sample_other.s_id)]
                else:
                    current_dist = matrix[(sample_other.s_id, sample_cluster.s_id)]
                if current_dist < min:
                    min = current_dist
        return min

    @staticmethod
    def print_link():
        print("single link")


class CompleteLink:
    def __init__(self):
        pass

    def compute(self, cluster, other, matrix):
        """
        computes distance between two clusters according to complete link and returns it
        :param cluster: first cluster to compute distance from(cluster)
        :param other: second cluster to compute distance to(cluster)
        :param matrix: distance matrix between samples in the data(dictionary)
        :return: returns the distance(float)
        """
        max = matrix[(cluster.samples[0].s_id, other.samples[0].s_id)]
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                if sample_cluster.s_id > sample_other.s_id:
                    current_dist = matrix[(sample_cluster.s_id, sample_other.s_id)]
                else:
                    current_dist = matrix[(sample_other.s_id, sample_cluster.s_id)]
                if current_dist > max:
                    max = current_dist
        return max

    @staticmethod
    def print_link():
        print("complete link")
