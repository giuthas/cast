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
Load configuration files.

File types handled by this module are strict yaml config files, different types
of exclusion lists, and pronunciation dictionaries.

A possible future addition is handling also the saving of strict yaml config
files.
"""
import csv
import sys
from contextlib import closing
from pathlib import Path

from strictyaml import (
    Bool, Float, Map, Optional, ScalarValidator, Str, YAML, YAMLError, load
)

from ..meta.cast_meta import Datasource
from ..pydantic_extensions import UpdatableBaseModel


class PathValidator(ScalarValidator):
    """
    Validate yaml representing a Path.

    Please note that empty fields are interpreted as not available and
    represented by None. If you want to specify current working directory, use
    '.'
    """

    def validate_scalar(self, chunk):
        if chunk.contents:
            return Path(chunk.contents)
        return None


_tier_schema = Map({
    Optional("label", default=""): Str(),
})


def read_config_file(filepath: Path | str | None = None) -> YAML:
    """
    Read the config file from filepath.

    If filepath is None, read from the default file 'cast_config.yml'.
    In both cases if the file does not exist, report this and exit.
    """
    if filepath is None:
        filepath = Path('cast_config.yml')
    elif isinstance(filepath, str):
        filepath = Path(filepath)

    if filepath.is_file():
        with closing(open(filepath, 'r', encoding="utf-8")) as yaml_file:
            schema = Map({
                "data_source": Str(),
                "speaker_id": Str(),
                "data_directory": PathValidator(),
                Optional("outputfile", default=None): PathValidator(),
                Optional("output_dirname"): PathValidator(),
                "flags": Map({
                    "detect_beep": Bool(),
                    "test": Bool(),
                }),
                "tiers": Map({
                    Optional("file"): _tier_schema,
                    Optional("utterance"): _tier_schema,
                    Optional("word"): _tier_schema,
                    Optional("phoneme"): _tier_schema,
                    Optional("phone"): _tier_schema
                }),
                Optional("exclusion_list", default=None): Str(),
                Optional("pronunciation_dictionary", default=None): Str(),
                Optional("word_guess"): Map({
                    "begin": Float(),
                    "end": Float()
                })
            })
            try:
                config_dict = load(yaml_file.read(), schema)
            except YAMLError as error:
                print(f"Fatal error in reading {filepath}:")
                print(error)
                sys.exit()
    else:
        print(f"Didn't find {filepath}. Exiting.")
        sys.exit()

    # data = config_dict.data
    # if "pronunciation_dictionary" in data and data["pronunciation_dictionary"]:
    #     if "[data_directory]" in data["pronunciation_dictionary"]:
    #         data["pronunciation_dictionary"].replace(
    #             "[data_directory]", data["data_directory"] + "/")
    # data["pronunciation_dictionary"] = Path(data["pronunciation_dictionary"])
    #
    # if "exclusion_list" in data and data["exclusion_list"]:
    #     if "[data_directory]" in data["exclusion_list"]:
    #         data["exclusion_list"].replace(
    #             "[data_directory]", data["data_directory"] + "/")
    # data["exclusion_list"] = Path(data["exclusion_list"])

    return config_dict


def read_exclusion_list(filepath: Path) -> dict:
    """
    Read the exclusion list from filepath.

    If no exclusion list file is present, return an empty array
    after warning the user.
    """
    if filepath.is_file():
        with closing(open(filepath, 'r', encoding="utf-8")) as yaml_file:
            yaml = load(yaml_file.read())
            exclusion_dict = yaml.data
    else:
        exclusion_dict = {}
        print(f"Did not find the exclusion list at {filepath}.")
        print("Proceeding anyhow.")
    return exclusion_dict


def read_pronunciation_dict(filepath: Path | str) -> dict:
    """
    Read the pronunciation dictionary and return it as a dict.

    The file is assumed to be in tab separated format and to 
    contain one word on each line followed by the X-SAMPA transcription
    of the expected pronunciation (phonological transcription).

    Returns a dict where each entry is a list of phonemes.
    """
    if isinstance(filepath, str):
        filepath = Path(filepath)

    pronunciation_dict = {}
    if filepath.is_file():
        with closing(open(filepath, 'r', encoding="utf-8")) as csvfile:
            reader = csv.reader(csvfile, delimiter=',')
            pronunciation_dict = {row[0]: list(filter(None, row[1:]))
                                  for row in reader}
        return pronunciation_dict
    else:
        print(f"Didn't find {pronunciation_dict}. Exiting.")
        sys.exit()
