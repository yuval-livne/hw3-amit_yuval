import cluster
import math
class AgglomerativeClustering:


    def __init__(self, link, samples):
        self.samples = samples
        self.link = link
        self.clusters = [cluster.Cluster(sample.s_id, [sample]) for sample in samples]

    def compute_silhouette(self, matrix):
        sil_dict = {}
        for clus in self.clusters:
            for sample in clus.samples:
                sum_dist = 0
                for other in clus.samples:
                    # sum_dist += sample.compute_euclidean_distance(other)
                    sum_dist += matrix[(sample, other)]
                sil_in = float(sum_dist/(len(clus.samples - 1)))

                dist_to_clus = []
                for other_clus in self.clusters:
                    if other_clus == clus:
                        continue
                    sum_dist = 0
                    for other in other_clus.samples:
                        sum_dist += matrix[(sample, other)]
                        # sum_dist += sample.compute_euclidean_distance(other)
                    dist_to_clus.append(float(sum_dist / (len(other_clus.samples))))
                sil_out = min(dist_to_clus)
                sil_dict[sample.s_id] = float((sil_out - sil_in) / (max(sil_out,sil_in)))

        return sil_dict


    def compute_summery_silhouette(self, matrix):
        samples_dict = self.compute_silhouette(matrix)
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
                            TN += 1

        return float((TP+TN)/number_of_pairs)

    def compute_dist_clusters(self, merged_id, matrix):
        dist_dict = {}
        for clus in self.clusters:
            for other_clus in self.clusters:
                if (clus.c_id == merged_id or other_clus.c_id == merged_id) or (merged_id == -1):
                    if (clus.c_id > other_clus.c_id):
                        dist_dict[(clus.c_id, other_clus.c_id)] = self.link.compute(clus, other_clus, matrix)
        return dist_dict

    def matrix_dist(self):
        matrix_dic={}
        for clus in self.clusters:
            for other_clus in self.clusters:
                if (clus.c_id > other_clus.c_id):
                    for sample in clus.samples:
                        for other_sample in other_clus.samples:
                            if (sample.s_id > other_sample.s_id):
                                matrix_dic[(sample, other_sample)] = sample.compute_euclidean_distance(other_sample)
        return matrix_dic


    def run(self, max_clusters):
        print(self.clusters[0])
        del self.clusters[0]
        print(self.clusters[0])
        sample_dist_matrix = self.matrix_dist()
        self.link.print_link()
        # merged_id = -1
        # clus_dist_matrix = self.compute_dist_clusters(merged_id, sample_dist_matrix)
        # first_id = 0
        # second_id = 0
        first_clus = self.clusters[0]
        second_clus = self.clusters[0]
        min_dist = sample_dist_matrix[list(sample_dist_matrix.keys())[0]]
        while (len(self.clusters) > max_clusters):
            for clus in self.clusters:
                for other_clus in self.clusters:
                    if (clus.c_id > other_clus.c_id):
                        clus_dist = self.link.compute(clus, other_clus, sample_dist_matrix)
                        if clus_dist < min_dist:
                            min_dist = clus_dist
                            if clus.c_id > other_clus.c_id:
                                first_clus = other_clus
                                second_clus = clus
                            else:
                                first_clus = clus
                                second_clus = other_clus
            first_clus.merge(second_clus)
            min_dist = max(sample_dist_matrix.values())

            # for sample in clus.samples:
                        #     for other_sample in other_clus.samples:
                        #         if (sample.s_id > other_sample.s_id):
                        #             if (sample_dist_matrix[(sample.s_id, other_sample.s_id)] < min_dist):
                        #                 min_dist = sample_dist_matrix[(sample.s_id, other_sample.s_id)]
                        #                 if clus.c_id > other_clus.c_id:
                        #                     other_clus.merge(clus)
                        #                     # merged_id = other_clus.c_id
                        #                 else:
                        #                     clus.merge(other_clus)
                        #                     # merged_id = clus.c_id

            # first_clus.merge(second_clus)
            # for key in clus_dist_matrix.keys():
            #     if clus_dist_matrix[key] < min_dist:
            #         first_id = key[0]
            #         second_id = key[1]
            #         min_dist = clus_dist_matrix[key]
            # for clus in self.clusters:
            #     if clus.c_id == first_id:
            #         first_clus = clus
            #     if clus.c_id == second_id:
            #         second_clus = clus
            #
            # if first_id > second_id:
            #     merged_id = second_id
            # else:
            #     merged_id = first_id
            # clus_dist_matrix = self.compute_dist_clusters(merged_id, sample_dist_matrix)

        sum_sil = self.compute_summery_silhouette(sample_dist_matrix)
        for clus in self.clusters:
            clus.print_details(sum_sil[clus.c_id])
        print(f'Whole data: silhouette = {sum_sil[0]}, RI = {self.compute_rand_index()}')
