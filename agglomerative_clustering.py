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
                    for other in other_clus.samples:
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
            for sample in clus.samples:
                sum_clus += samples_dict[sample.s_id]
                sum_total += samples_dict[sample.s_id]

            clus_dict[clus.c_id] = float(sum_clus / len(clus.samples))
        clus_dict[0] = float(sum_total / len(self.samples))
        return clus_dict

    def compute_rand_index(self):
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
                    for other in other_clus.samples:
                        if other_clus == clus:
                            continue
                        if sample.s_id > other.s_id:
                            continue
                        if sample.label != other.label:
                            TN+=1

        return float((TP+TN)/number_of_pairs)

    def compute_dist_clusters(self, merged_id):
        dist_dict = {}
        for clus in self.clusters:
            for other_clus in self.clusters:
                if (clus.c_id == merged_id or other_clus.c_id == merged_id) or (merged_id == -1):
                    if (clus.c_id > other_clus.c_id):
                        dist_dict[(clus.c_id, other_clus.c_id)] = self.link.compute(clus, other_clus)
        return dist_dict


    def run(self, max_clusters):
        self.link.print_link()
        merged_id = -1
        dist_matrix = self.compute_dist_clusters(merged_id)
        first_id = 0
        second_id = 0
        first_clus = self.clusters[0]
        second_clus = self.clusters[0]
        min_dist = dist_matrix[list(dist_matrix.keys())[0]]
        while (len(self.clusters) > max_clusters):
            for key in dist_matrix.keys():
                if dist_matrix[key] < min_dist:
                    first_id = key[0]
                    second_id = key[1]
                    min_dist = dist_matrix[key]
            for clus in self.clusters:
                if clus.c_id == first_id:
                    first_clus = clus
                if clus.c_id == second_id:
                    second_clus = clus

            if first_id > second_id:
                merged_id = second_id
            else:
                merged_id = first_id
            first_clus.merge(second_clus)
            dist_matrix = self.compute_dist_clusters(merged_id)

        sum_sil = self.compute_summery_silhouette()
        for clus in self.clusters:
            clus.print_details(sum_sil[clus.c_id])
        print(f'Whole data: silhouette = {sum_sil[0]}, RI = {self.compute_rand_index()}')
