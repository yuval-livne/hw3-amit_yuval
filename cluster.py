class Cluster:
    def __init__(self, c_id, samples):
        self.c_id = c_id
        self.samples = samples


    def merge(self, other):
        """
        merges the other cluster provided with the current cluster and deletes the other
        :param other: cluster to merge and delete(cluster)
        """
        for sample in other.samples:
            self.samples.append(sample)
        self.samples = sorted(self.samples, key=lambda sample: sample.s_id)
        del other

    def print_details(self, silhouette):
        """
        prints the cluster's and its samples' details
        :param silhouette: the cluster's silhouette value(int)
        """
        labels = [sample.label for sample in self.samples]
        id_list = [sample.s_id for sample in self.samples]

        label_set = set(labels)  # holds the unique label values
        # create labels histogram
        label_dict = {}
        for label in label_set:
            label_dict[label] = 0  # initialize the histogram
        # fill the histogram
        for label in labels:
            label_dict[label] = label_dict[label] + 1

        # check which label appears most
        dom_count = 0
        for label in label_dict.keys():
            if label_dict[label] >= dom_count:
                #  if two labels appear the same amount of times we'll take the lexicographic first label
                if label_dict[label] == dom_count:
                    if label < dominant_label:
                        dominant_label = label
                        dom_count = label_dict[label]
                else:
                    dominant_label = label
                    dom_count = label_dict[label]

        print(f'Cluster {self.c_id}: {id_list}, dominant label = {dominant_label}, silhouette = {silhouette}')
