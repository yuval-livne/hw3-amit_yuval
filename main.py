import sys
import data


def main(argv):
    path = argv[1]
    the_data = data.Data(path)
    dict = the_data.load_data()
    print(dict["samples"])

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main(sys.argv)