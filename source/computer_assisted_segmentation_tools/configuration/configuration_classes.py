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
Classes for storing CAST configuration.
"""

from dataclasses import dataclass

from ..meta.cast_meta import (
    Datasource)
from ..pydantic_extensions import (
    UpdatableBaseModel)


class ConfigurationFlags(UpdatableBaseModel):
    detect_beep: bool | None = None
    test: bool | None = None


@dataclass
class ExclusionList:
    """
    List of files, prompts, and parts of prompts to be excluded from analysis.
    """
    files: list[str] | None = None
    prompts: list[str] | None = None
    parts_of_prompts: list[str] | None = None


class UtteranceGuess(UpdatableBaseModel):
    begin: float
    end: float


class MainConfig(UpdatableBaseModel):
    datasource: Datasource
    speaker_id: str
    flags: ConfigurationFlags
    tiers: dict[str, str]
    exclusion_list: ExclusionList | None = None
    pronunciation_dictionary: dict[str, str] | None = None
    utterance_guess: UtteranceGuess
