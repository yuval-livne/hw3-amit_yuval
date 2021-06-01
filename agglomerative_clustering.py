import cluster
import math
class AgglomerativeClustering:


    def __init__(self, link, samples):
        self.samples = samples
        self.link = link
        self.clusters = [cluster.Cluster(sample.s_id, [sample]) for sample in samples]

    def compute_silhouette(self):
        sil_dict = {}
        for clus in self.clusters:
            for sample in clus.samples:
                sum_dist = 0
                for other in clus.samples:
                    sum_dist += sample.compute_euclidean_distance(other)
                sil_in = float(sum_dist/(len(clus.samples - 1)))

                dist_to_clus = []
                for other_clus in self.clusters:
                    if other_clus == clus:
                        continue
                    sum_dist = 0
                    for other in other_clus:
                        sum_dist += sample.compute_euclidean_distance(other)
                    dist_to_clus.append(float(sum_dist / (len(other_clus.samples))))
                sil_out = min(dist_to_clus)
                sil_dict[sample.s_id] = float((sil_out - sil_in) / (max(sil_out,sil_in)))

        return sil_dict



    def compute_summery_silhouette(self):
        samples_dict = self.compute_silhouette()
        sum_total=0
        clus_dict={}
        for clus in self.clusters:
            sum_clus=0
            for sample in clus:
                sum_clus += samples_dict[sample.s_id]
                sum_total += samples_dict[sample.s_id]

            clus_dict[clus.c_id] = float(sum_clus / len(clus.samples))
        clus_dict[0] = float(sum_total / len(self.samples))
        return clus_dict

    def rand_index(self):
        TP = 0
        TN = 0
        number_of_pairs = math.factorial(len(self.samples))/(2*math.factorial(len(self.samples)-2))
        for clus in self.clusters:
            for sample in clus.samples:
                for other in clus.samples:
                    if sample.s_id >= other.s_id:
                        continue
                    if sample.label == other.label:
                        TP+=1

                for other_clus in self.clusters:
                    if other_clus == clus:
                        continue
                    if sample.s_id > other.s_id:
                        continue
                    if sample.label != other.label:
                        TN+=1



        return float((TP+TN)/number_of_pairs)
