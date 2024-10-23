import os
from typing import Any, Dict, List, Set

import networkx as nx
import pandas as pd
from downloaders import BaseDownloader
from tqdm.auto import tqdm

from ott_taxonomy.settings.dataset_settings import DatasetSettings


class Dataset:
    """Class representing a the OTT taxonomy dataset."""

    def __init__(
        self,
        synonyms: pd.DataFrame,
        taxonomy: pd.DataFrame,
        metadata: Dict[str, Any],
    ):
        """Initialize the OTT Taxonomy Dataset."""
        self._synonyms: pd.DataFrame = synonyms
        self._taxonomy: pd.DataFrame = taxonomy
        self._metadata: Dict = metadata

    @staticmethod
    def download(settings: DatasetSettings) -> "Dataset":
        """Build a dataset from the settings."""
        assert isinstance(settings, DatasetSettings)
        downloader = BaseDownloader(
            process_number=1,
            verbose=settings.verbose,
        )
        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objectives():
            paths.append(objective.path)
            urls.append(objective.url)

        downloader.download(urls=urls, paths=paths)

        # if we build, we will only download the dataset. In order to have it, we need to load it
        # from disk
        synonyms = pd.DataFrame()
        taxonomy = pd.DataFrame()
        return Dataset(
            synonyms=synonyms,
            taxonomy=taxonomy,
            metadata=settings.into_dict(),
        )

    @staticmethod
    def load(
        version: str,
        download_directory: str = "downloads",
        verbose: bool = True,
    ) -> "Dataset":
        """Load the dataset from disk."""
        if verbose:
            settings = (
                DatasetSettings(version=version)
                .set_verbose()
                .set_downloads_directory(download_directory)
            )
        else:
            settings = DatasetSettings(version=version).set_downloads_directory(
                download_directory
            )

        paths: List[str] = []
        urls: List[str] = []

        for objective in settings.download_objectives():
            paths.append(objective.path)
            urls.append(objective.url)

        BaseDownloader(
            verbose=verbose,
        ).download(urls=urls, paths=paths)

        synonyms = pd.read_csv(
            os.path.join(download_directory, version, version, "synonyms.tsv"),
            sep="\t",
        )

        if version in [
            "ott2.6",
            "ott2.7",
        ]:  # handles corner case where the file structure is not the same for old versions
            taxonomy = pd.read_csv(
                os.path.join(download_directory, version, "ott", "taxonomy.tsv"),
                sep="\t",
            )
        else:
            taxonomy = pd.read_csv(
                os.path.join(download_directory, version, version, "taxonomy.tsv"),
                sep="\t",
            )

        # we drop all the columns that are not useful for the user in the taxonomy
        taxonomy = taxonomy.drop(
            columns=["|", "|.1", "|.2", "|.3", "|.4", "|.5", "|.6", "Unnamed: 14"]
        )

        return Dataset(
            synonyms=synonyms,
            taxonomy=taxonomy,
            metadata=settings.into_dict(),
        )

    def get_taxonomy(self) -> pd.DataFrame:
        """Return the taxonomy."""
        return self._taxonomy

    def get_synonyms(self) -> pd.DataFrame:
        """Return the synonyms."""
        return self._synonyms

    def to_networkx(self) -> nx.DiGraph:
        """Return the taxonomy as a networkx directed graph."""
        if self._taxonomy.empty:
            raise ValueError(
                "No taxonomy has been loaded. Please load a taxonomy first and then call this funciton."
            )
        graph = nx.DiGraph()

        graph.add_nodes_from(set(self._taxonomy["uid"].astype("int32").values.tolist()))

        # we add all edges except the first row of the dataframe since is the
        edges = self._taxonomy[["parent_uid", "uid"]].iloc[1:].astype("int32")
        graph.add_edges_from(edges.values.tolist())
        return graph

    def generate_subgraph_from_id(
        self, node: int, keep_subspecies: bool = True
    ) -> nx.DiGraph:
        """Generate a subgraph from a given node. This will return the node and all its children."""
        graph = self.to_networkx()
        if not keep_subspecies:
            all_species = self._taxonomy[self._taxonomy["rank"] == "species"].uid.values

            ## we do a double list comprehension to get all the children of the species
            all_subspecies = [
                child
                for species in all_species
                for child in nx.descendants(graph, species)
            ]
            graph.remove_nodes_from(all_subspecies)
            return graph.subgraph(nx.descendants(graph, node) | {node})

        return graph.subgraph(nx.descendants(graph, node) | {node})
