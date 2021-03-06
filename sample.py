class Sample:
    def __init__(self, s_id, genes, label):
        self.s_id = s_id
        self.genes = genes
        self.label = label

    def compute_euclidean_distance(self, other):
        """
        computes distance between two samples and returns it
        :param other: sample to compute distance from(sample)
        :return: returns the distance(float)
        """
        return sum([(my - his) ** 2 for my, his in zip(self.genes, other.genes)]) ** 0.5
