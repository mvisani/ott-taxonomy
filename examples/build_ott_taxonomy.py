"""Example script to build an OTT Taxonomy version."""

import argparse

from tqdm.auto import tqdm

from ott_taxonomy import Dataset, DatasetSettings


def build_ott_taxonomy(version: str) -> Dataset:
    """Build a version of the OTT Taxonomy."""
    settings = DatasetSettings(version=version).set_verbose()
    return Dataset.download(settings)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build a version of the OTT Taxonomy.")
    parser.add_argument(
        "version",
        type=str,
        help="The version of the OTT Taxonomy to build.",
    )

    args = parser.parse_args()

    if args.version == "all":
        versions = DatasetSettings.available_versions()
    else:
        versions = [args.version]

    for v in tqdm(
        versions,
        desc="Building OTT Taxonomy",
        unit="version",
        disable=len(versions) == 1,
    ):
        _dataset: Dataset = build_ott_taxonomy(v)
