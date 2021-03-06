import sys
import data
import agglomerative_clustering as agglo
import link

MAX_CLUSTERS = 7


def main(argv):
    path = argv[1]
    the_data = data.Data(path)  # intialize a Data instance with the data from csv file
    samples_list = the_data.create_samples()

    # initialize link and clustering instances
    single_link = link.SingleLink()
    complete_link = link.CompleteLink()
    single_agglo = agglo.AgglomerativeClustering(single_link, samples_list)
    complete_agglo = agglo.AgglomerativeClustering(complete_link, samples_list)

    # run the clustering algorithms
    single_agglo.run(MAX_CLUSTERS)
    print()
    complete_agglo.run(MAX_CLUSTERS)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)
