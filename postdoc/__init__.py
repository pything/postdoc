#!/usr/bin/env python3
# -*- coding: utf-8 -*-

__project__ = "Postdoc"
__author__ = "Christian Heider Nielsen"
__doc__ = r"""

           Created on 09/03/2020
           """
__version__ = "0.0.4"

import os
from datetime import datetime
from logging import warning

import pkg_resources

from apppath import AppPath


# __all__ = ["PROJECT_APP_PATH", "PROJECT_NAME", "PROJECT_VERSION", "get_version"]


def dist_is_editable(dist):
    """
    Return True if given Distribution is an editable installation."""
    import sys
    from pathlib import Path

    for path_item in sys.path:
        egg_link = Path(path_item) / f"{dist.project_name}.egg-link"
        if egg_link.is_file():
            return True
    return False


PROJECT_NAME = __project__.lower().strip().replace(" ", "_")
PROJECT_YEAR = 2020
PROJECT_VERSION = __version__
PROJECT_AUTHOR = __author__.lower().strip().replace(" ", "_")
PROJECT_APP_PATH = AppPath(app_name=PROJECT_NAME, app_author=PROJECT_AUTHOR)

distributions = {v.key: v for v in pkg_resources.working_set}
if PROJECT_NAME in distributions:
    distribution = distributions[PROJECT_NAME]
    DEVELOP = dist_is_editable(distribution)
else:
    DEVELOP = True


def get_version(append_time=DEVELOP):
    """ """
    version = __version__
    if not version:
        version = os.getenv("VERSION", "0.0.0")

    if append_time:
        now = datetime.utcnow()
        date_version = now.strftime("%Y%m%d%H%M%S")
        # date_version = time.time()

        if version:
            # Most git tags are prefixed with 'v' (example: v1.2.3) this is
            # never desirable for artifact repositories, so we strip the
            # leading 'v' if it's present.
            version = (
                version[1:]
                if isinstance(version, str) and version.startswith("v")
                else version
            )
        else:
            # Default version is an ISO8601 compliant datetime. PyPI doesn't allow
            # the colon ':' character in its versions, and time is required to allow
            # for multiple publications to master in one day. This datetime string
            # uses the 'basic' ISO8601 format for both its date and time components
            # to avoid issues with the colon character (ISO requires that date and
            # time components of a date-time string must be uniformly basic or
            # extended, which is why the date component does not have dashes.
            #
            # Publications using datetime versions should only be made from master
            # to represent the HEAD moving forward.
            warning(
                f"Environment variable VERSION is not set, only using datetime: {date_version}"
            )

            # warn(f'Environment variable VERSION is not set, only using timestamp: {version}')

        version = f"{version}.{date_version}"

    return version


if __version__ is None:
    __version__ = get_version(append_time=True)

__version_info__ = tuple(int(segment) for segment in __version__.split("."))
