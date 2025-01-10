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

from enum import Enum
from pathlib import Path
import sys

from .aaa_meta import check_and_load_aaa_meta
from .rasl_meta import check_and_load_rasl_meta


class Datasource(Enum):
    """
    Data sources SATKIT can handle.

    Used in saving and loading to identify the data source in config, as well as
    in meta and skip the step of trying to figure the data source out from the
    type of files present.
    """
    AAA = "AAA"
    # EVA = "EVA"
    RASL = "RASL"
    CSV = "csv"


def get_token_list(config_dict: dict, directory: Path) -> dict:
    speaker_id = config_dict['speaker id']
    test = config_dict['test']

    data_source = config_dict['data source']
    if data_source is Datasource.AAA:
        table = check_and_load_aaa_meta(speaker_id, directory, test)
    elif data_source is Datasource.RASL:
        table = check_and_load_rasl_meta(speaker_id, directory, test)
    elif data_source is Datasource.CSV:
        # table = check_and_load_csv_meta(
        #     speaker_id, directory, test, csv_meta_file)
        # This was supposed to be in used in the palatalisation project.
        print(f"Unsupported data source: {data_source}. Exiting")
        sys.exit()
    else:
        print(f"Unknown data source: {data_source}. Exiting.")
        sys.exit()

    return table
