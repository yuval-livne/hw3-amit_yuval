import abc
class Link():
    __metaclass__=abc.ABCMeta

    @abc.abstractmethod
    def compute(self, cluster, other):
        pass


class SingleLink(Link):

    def compute(self, cluster, other):
        min = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                current_dist = sample_cluster.compute_euclidean_distance(sample_other)
                if (current_dist < min):
                    min = current_dist
        return min


class CompleteLink(Link):

    def compute(self, cluster, other):
        max = cluster.samples[0].compute_euclidean_distance(other.samples[0])
        for sample_cluster in cluster.samples:
            for sample_other in other.samples:
                current_dist = sample_cluster.compute_euclidean_distance(sample_other)
                if (current_dist > max):
                    max = current_dist
        return max

