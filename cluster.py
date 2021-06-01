class Cluster:
    def __init__(self, c_id, samples):
        self.c_id = c_id
        self.samples = samples

    def merge(self, other):

        if self.c_id > other.c_id:
            for sample in self.samples:
                other.samples.append(sample)
            other.samples = sorted(other.samples)
            del self
        else:
            for sample in other.samples:
                self.samples.append(sample)
            self.samples = sorted(self.samples)
            del other

    def print_details(self, silhouette):

        labels = [sample.label for sample in self.samples]
        label_set = set(labels)
        label_dict = {}
        for label in label_set:
            label_dict[label] = 0
        for label in labels:
            label_dict[label] = label_dict[label]+1
        dominant_label = max(label_dict.values())
        print(f'Cluster {self.c_id}: [{self.samples}], dominant label = {dominant_label}, silhouette = {silhouette}')
#we need to take care of the order in equal labels