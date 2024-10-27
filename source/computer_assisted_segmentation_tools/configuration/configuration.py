#
# Copyright (c) 2022-2024 Pertti Palo.
#
# This file is part of Computer Assisted Segmentation Tools
# (see https://github.com/giuthas-speech-research-tools/cast/).
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
# The example data packaged with this program is licensed under the
# Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License. You should have received a
# copy of the Creative Commons Attribution-NonCommercial-ShareAlike 4.0
# International (CC BY-NC-SA 4.0) License along with the data. If not,
# see <https://creativecommons.org/licenses/by-nc-sa/4.0/> for details.
#
# When using the toolkit for scientific publications, please cite the
# articles listed in README.markdown. They can also be found in
# citations.bib in BibTeX format.
#
"""Main configuration for CAST."""

import logging
from pathlib import Path

from .configuration_parser import read_config_file
from .configuration_classes import MainConfig

_logger = logging.getLogger('cast.configuration_setup')


class CastConfig:
    """
    Main configuration class of SATKIT.
    """

    # TODO
    # - reload

    # TODO: implement an update method as well
    # as save functionality.

    # TODO: __repr__

    def __init__(
            self,
            configuration_file: Path | str | None = None
    ) -> None:
        """
        Init the main configuration object.

        Run only once. Updates should be done with methods of the class.

        Parameters
        -------
        configuration_file : Union[Path, str, None]
            Path to the main configuration file.
        """

        self._config_yaml = read_config_file(configuration_file)
        self._config = MainConfig(**self._config_yaml.data)

    @property
    def main_config(self) -> MainConfig:
        """Main config options."""
        return self._config

    def update_from_file(
            self, configuration_file: Path | str
    ) -> None:
        """
        Update the configuration from a file.

        Parameters
        ----------
        configuration_file : Union[Path, str]
            File to read the new options from.

        Raises
        ------
        NotImplementedError
            This hasn't been implemented yet.
        """
        raise NotImplementedError(
            "Updating configuration from a file has not yet been implemented.")
        # main_config.update(**config_dict)

    def save_to_file(
            self, file: Path | str
    ) -> None:
        """
        Save configuration to a file.

        Parameters
        ----------
        file : Union[Path, str]
            File to save to.

        Raises
        ------
        NotImplementedError
            This hasn't been implemented yet.
        """
        raise NotImplementedError(
            "Saving configuration to a file has not yet been implemented.")
