from ott_taxonomy import Dataset


def main():
    x = Dataset.load("ott3.6", verbose=True).to_networkx()
    print(x.number_of_edges())
    print(x.number_of_nodes())


if __name__ == "__main__":
    main()
