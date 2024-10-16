"""Submodule providing the settings for constructing versions of the OTT Taxonomy dataset."""

import os
from typing import Any, Dict, List

import compress_json

from ott_taxonomy.exceptions import UnavailableEntry, VersionException
from ott_taxonomy.utils.download_objective import DownloadObjective


class DatasetSettings:
    """Class defining the settings for constructing versions of the OTT taxonomy."""

    def __init__(self, version: str):
        """Initialize the settings for constructing versions of the OTT taxonomy."""
        local_version_path = os.path.join(
            os.path.dirname(__file__), "versions", f"{version}.json"
        )
        if not os.path.exists(local_version_path):
            available_versions = os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
            raise VersionException(version, available_versions)

        self._version_metadata: Dict[str, Any] = compress_json.load(local_version_path)
        self._verbose: bool = False
        self._to_include: List[str] = ["url"]
        self._downloads_directory: str = "downloads"

    @staticmethod
    def available_versions() -> List[str]:
        """Return a list of available versions of the OTT Taxonomy."""
        return [
            version.replace(".json", "")
            for version in os.listdir(
                os.path.join(os.path.dirname(__file__), "versions")
            )
        ]

    def download_objectives(self) -> List[DownloadObjective]:
        """Return the download objectives."""
        download_objectives: List[DownloadObjective] = []
        for included in self._to_include:
            url = self._version_metadata[included]
            file_name = url.split("/")[-1]
            path = os.path.join(
                self._downloads_directory,
                file_name,
            )
            download_objectives.append(DownloadObjective(path, url))

        return download_objectives

    def into_dict(self) -> Dict[str, Any]:
        """Return the settings as a dictionary."""
        return {
            "version_metadata": self._version_metadata,
            "verbose": self._verbose,
            "to_include": self._to_include,
            "downloads_directory": self._downloads_directory,
        }

    def set_downloads_directory(self, directory: str) -> "DatasetSettings":
        """Sets the directory to download files."""
        self._downloads_directory = directory
        return self

    @property
    def verbose(self) -> bool:
        """Return whether the settings are in verbose mode."""
        return self._verbose

    def set_verbose(self) -> "DatasetSettings":
        """Sets to verbose mode."""
        self._verbose = True
        return self
