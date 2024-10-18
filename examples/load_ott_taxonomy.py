from ott_taxonomy import Dataset, DatasetSettings


def main():
    x = Dataset.load("ott2.8", verbose=True)
    print(x.get_taxonomy().head())


if __name__ == "__main__":
    main()
