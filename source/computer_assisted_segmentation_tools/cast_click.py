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

"""
Command line argument parser.
"""
from pathlib import Path

import click
from icecream import ic

from .configuration import CastConfig
from .clean_textgrids import remove_empty_intervals_from_textgrids
from .concatenate import concatenate_wavs
from .extract import extract_textgrids
from .textgrid_functions import add_tiers


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument(
    "config_file",
    type=click.Path(exists=True, dir_okay=False, file_okay=True), )
def add(directory: str, config_file: str) -> None:
    """
    Add the next active Tier.

    \b
    DIRECTORY contains the TextGrids to process.
    CONFIG_FILE is the configuration .yaml file.
    """
    configuration = CastConfig(Path(config_file))
    pronunciation_dict = None
    add_tiers(path=directory,
              configuration=configuration.main_config,
              pronunciation_dict=pronunciation_dict)


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument("config_file")
@click.option(
    '-a', '--add',
    type=click.Choice(['none', 'first', 'all'], case_sensitive=False))
def concatenate():
    """
    Concatenate TextGrids.

    \b
    DIRECTORY contains the .TextGrid files to process.
    CONFIG_FILE is the configuration .yaml file.

    NOT IMPLEMENTED YET.
    """
    pass
    # pronunciation_dict = None
    # concatenate_wavs(
    #     path, config, pronunciation_dict)


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument("config_file")
@click.argument("tier")
def delete():
    """
    Delete a Tier from TextGrids.

    \b
    DIRECTORY contains the .wav files to process.
    CONFIG_FILE is the configuration .yaml file.
    TIER is the name of the tier to delete.

    NOT IMPLEMENTED YET.
    """
    pass


@click.command()
@click.argument(
    "textgrid",
    type=click.Path(exists=True, dir_okay=False, file_okay=True), )
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument("config_file")
def extract():
    """
    Extract individual TextGrids from a long one.

    \b
    TEXTGRID the long TextGrid.
    DIRECTORY to extract the TextGrids to.
    CONFIG_FILE is the configuration .yaml file.

    NOT IMPLEMENTED YET.
    """
    pass
    # extract_textgrids(Path(path), Path(config['outputfile']))


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument("config_file")
@click.option(
    '-a', '--add',
    type=click.Choice(['none', 'first', 'all'], case_sensitive=False))
def init():
    """
    Create TextGrids for each .wav file. Optionally add Tiers.

    \b
    DIRECTORY contains the .wav files to process.
    CONFIG_FILE is the configuration .yaml file.

    NOT IMPLEMENTED YET.
    """
    # TODO: this is for creating empty TextGrids from wavs, or a list of begin
    # and end values, or just end values.


@click.command()
def remove_double_boundaries():
    """
    Remove double boundaries between words.

    \b
    DIRECTORY contains the .wav files to process.
    CONFIG_FILE is the configuration .yaml file.

    NOT IMPLEMENTED YET.
    """
    pass
    # if not config['output_dirname']:
    #     print(
    #         'Fatal: No output directory for new textgrids specified in '
    #         'config file.')
    # remove_empty_intervals_from_textgrids(
    #     Path(path), Path(config['output_dirname']))


@click.command()
@click.argument(
    "directory",
    type=click.Path(exists=True, dir_okay=True, file_okay=False), )
@click.argument("config_file")
@click.argument("tier")
def scramble():
    """
    Scramble an existing Tier in TextGrids.

    \b
    DIRECTORY contains the .wav files to process.
    CONFIG_FILE is the configuration .yaml file.
    TIER is the name of the tier to scramble.

    NOT IMPLEMENTED YET.
    """
    pass
