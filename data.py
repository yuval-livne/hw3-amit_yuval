import pandas
from sample import Sample

class Data:
    def __init__(self, path):
        self.path = path
        self.data = self.load_data()
        self.data_dict

    def load_data(self):
        df = pandas.read_csv(self.path)
        self.data_dict = df.to_dict(orient="list")
        return self.data_dict

    def create_samples(self):
        sample_list = []
        genes = []
        for record in range(len(self.data_dict["samples"])):
            sample_id = self.data_dict["samples"][record]
            genes_cols = list(self.data_dict.keys())[2:]
            for gene in genes_cols:
                genes.append(self.data_dict[gene][record])
            label = self.data_dict["type"][record]
            sample_list.append(Sample(sample_id, genes, label))
        return sample_list
