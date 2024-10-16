"""Submodule defining exceptions used across the OTT taxonomy."""

from ott_taxonomy.exceptions.unavailable_entry import UnavailableEntry
from ott_taxonomy.exceptions.version_exception import VersionException

__all__ = [
    "UnavailableEntry",
    "VersionException",
]
