import abc
class Link():
    __metaclass__=abc.ABCMeta

    @abc.abstractmethod
    def compute(self, cluster, other):
        pass


class SingleLink(Link):

    def compute(self, cluster, other, matrix):
        min=matrix[(cluster.samples[0], other.samples[0])]
        # min = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                current_dist=matrix[(sample_cluster, sample_other)]
                # current_dist = sample_cluster.compute_euclidean_distance(sample_other)
                if (current_dist < min):
                    min = current_dist
        return min

    @staticmethod
    def print_link():
        print("single link")


class CompleteLink(Link):
    @staticmethod
    def print_link():
        print("complete link")

    def compute(self, cluster, other, matrix):
        # max = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        max = matrix[(cluster.samples[0], other.samples[0])]
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                current_dist=matrix[(sample_cluster, sample_other)]
                # current_dist = sample_cluster.compute_euclidean_distance(sample_other)
                if (current_dist > max):
                    max = current_dist
        return max


