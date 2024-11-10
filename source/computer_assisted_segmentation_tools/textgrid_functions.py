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
Functions for generating and modifying TextGrid objects.
"""
import logging
import pprint
import shutil
import sys
from copy import deepcopy
from pathlib import Path

from icecream import ic

import numpy as np
from textgrids import TextGrid, Interval, Tier

from .configuration import ExclusionList, MainConfig
from .exclusion import apply_exclusion_list
from .meta import (
    check_and_load_aaa_meta, check_and_load_csv_meta, check_and_load_rasl_meta
)
from .meta.cast_meta import Datasource
from .wav_handling import add_begin_end_from_wav

_logger = logging.getLogger('cast.textgrid_functions')

pp = pprint.PrettyPrinter(indent=4)


def generate_textgrid(
        table: dict,
        out_textgrid: TextGrid,
        config_dict: dict,
        pronunciation_dict: dict
):
    # TODO: given the timing data in table produce a new TextGrid
    pass


def create_autosave_directory(textgrid_path: Path, config_dict: dict) -> Path:
    ic(config_dict)

    old_dir = textgrid_path.parent
    new_dir = old_dir.with_name('cast_autosave')
    if not new_dir.exists():
        new_dir.mkdir()
    else:
        _logger.critical(
            "Autosave directory: %s already exists.",
            str(new_dir))
        _logger.critical("I don't know how to solve that.")
        sys.exit()

    return new_dir


def add_tiers(
        path: Path | str,
        configuration: MainConfig,
        pronunciation_dict: dict | None = None,
        csv_meta_file: str | None = None,
) -> None:
    # TODO: check which tiers the textgrid has and which are requested. supply
    # the missing ones

    speaker_id = configuration.speaker_id
    test = configuration.flags.test

    if isinstance(path, str):
        path = Path(path)

    if path.is_file():
        if path.suffix == ".TextGrid":
            textgrid = TextGrid(str(path))
            add_tiers_to_textgrid(textgrid, configuration, pronunciation_dict)
            textgrid.write(str(path))
        else:
            print(f"Unknown file type: {path.suffix}. Exiting.")
            sys.exit()
    elif path.is_dir():
        datasource = configuration.datasource
        table = {}

        match datasource:
            case Datasource.AAA:
                table = check_and_load_aaa_meta(
                    speaker_id, path, test)
            case Datasource.RASL:
                table = check_and_load_rasl_meta(speaker_id, path, test)
            case Datasource.CSV:
                table = check_and_load_csv_meta(
                    speaker_id, path, test, csv_meta_file)
            case _:
                print(f"Unknown data source: {datasource}. Exiting.")
                sys.exit()

        apply_exclusion_list(table, configuration.exclusion_list)

        for item in table:
            item['textgrid_path'] = path / (item['filename'] + ".TextGrid")

        existing_textgrids = [item['textgrid_path'].is_file() for item in table]
        if any(existing_textgrids):
            new_dir = create_autosave_directory(
                table[0]['textgrid_path'], configuration)

            print(f"copying to {new_dir}")
            for item in table:
                shutil.copy2(item['textgrid_path'], new_dir)

        for item in table:
            if item['excluded']:
                _logger.info(
                    "File %s excluded, skipping ", item['filename'])
                continue

            add_begin_end_from_wav(item)

            if item['textgrid_path'].is_file():
                textgrid = TextGrid(item['textgrid_path'])
            else:
                textgrid = TextGrid()

            add_tiers_to_textgrid(
                textgrid, item, configuration, pronunciation_dict)
            textgrid.write(item['textgrid_path'])


def _calculate_seg_begin_end(
        begin: float,
        end: float,
        coefficients: tuple[float, float]
) -> tuple[float, float]:
    earliest_speech = begin + .058
    seg_begin = earliest_speech + (end - earliest_speech) * coefficients[0]
    seg_end = earliest_speech + (end - earliest_speech) * coefficients[1]
    return seg_begin, seg_end


def add_tiers_to_textgrid(
        textgrid: TextGrid,
        params: dict,
        configuration: MainConfig,
        pronunciation_dict: dict = None
) -> None:
    """
    Add Tiers to a TextGrid

    Parameters
    ----------
    textgrid : TextGrid
        The Tiers will be added to this TextGrid
    params : dict
        parameters for this recording
    config_dict : dict
        Configuration dictionary
    pronunciation_dict : dict, optional
        Pronunciation dictionary -- not needed if only generating to the word
        level, by default None
    """
    begin_coefficient = configuration.word_guess.begin
    end_coefficient = configuration.word_guess.end

    if pronunciation_dict:
        if params['prompt'] in pronunciation_dict:
            transcription = pronunciation_dict[params['prompt']]
            print(
                f"Generating boundaries for {params['prompt']} "
                "which is pronounced {transcription}.")
            params['transcription'] = transcription

            # Generate an evenly spaced first guess of segmentation by taking
            # the middle third of the potential speech interval and chopping it
            # up.
            (seg_begin, seg_end) = _calculate_seg_begin_end(
                begin=params['begin'],
                end=params['end'],
                coefficients=(begin_coefficient, end_coefficient))
            boundaries = np.linspace(
                seg_begin, seg_end, len(transcription) + 3)
            boundaries = boundaries[1:-1]
            params['segment boundaries'] = boundaries
        else:
            print(
                f"Word \'{params['prompt']}\' missing from pronunciation dict.")
    else:
        print(f"Generating boundaries for {params['prompt']}.")
        (seg_begin, seg_end) = _calculate_seg_begin_end(
            begin=params['begin'],
            end=params['end'],
            coefficients=(begin_coefficient, end_coefficient))
        boundaries = [seg_begin, seg_end]
        params['segment boundaries'] = boundaries

    if configuration.tiers['utterance']:
        if configuration.tier_names.utterance in textgrid:
            _logger.critical(
                "Tier %s already exists. Skipping file %s.",
                configuration.tier_names.utterance,
                textgrid.filename)
            return
        utterance = generate_utterance_dicts(params)
        textgrid.interval_tier_from_array(
            configuration.tier_names.utterance, utterance)
    if configuration.tiers['word']:
        if configuration.tier_names.word in textgrid:
            _logger.critical(
                "Tier %s already exists. Skipping file %s.",
                configuration.tier_names.utterance,
                textgrid.filename)
            return
        words = generate_word_intervals(params)
        textgrid.interval_tier_from_array(
            configuration.tier_names.word, words)
    if configuration.tiers['phoneme']:
        if configuration.tier_names.phoneme in textgrid:
            _logger.critical(
                "Tier %s already exists. Skipping file %s.",
                configuration.tier_names.utterance,
                textgrid.filename)
            return
        segments = generate_segments(params, pronunciation_dict)
        textgrid.interval_tier_from_array(
            configuration.tier_names.phoneme, segments)
    if configuration.tiers['phone']:
        if configuration.tier_names.phone in textgrid:
            _logger.critical(
                "Tier %s already exists. Skipping file %s.",
                configuration.tier_names.utterance,
                textgrid.filename)
            return
        elif configuration.tier_names.phoneme in textgrid:
            phone_tier = deepcopy(
                textgrid[configuration.tier_names.phoneme])
            textgrid[configuration.tier_names.phone] = phone_tier
        textgrid.interval_tier_from_array(
            configuration.tier_names.phone, segments)


def append_beginning_intervals(entry: dict, tier: Tier) -> None:
    """
    Add Intervals for BEEP and silence to the Tier.

    Parameters
    ----------
    entry : dict
        Metadata for the recording.
    tier : Tier
        Tier to add the Intervals to.
    """
    if 'beep' in entry:
        begin_buffer = Interval(
            '', xmin=entry['sliceBegin'], xmax=entry['beep'])
        tier.append(begin_buffer)

        beep = Interval(
            text='BEEP',
            xmin=entry['beep'],
            xmax=entry['beep'] + 0.05
        )
        tier.append(beep)

        after_beep = Interval(
            text='',
            xmin=entry['beep'] + 0.05,
            xmax=entry['segment boundaries'][0])
        tier.append(after_beep)
    else:
        begin_buffer = Interval(
            text='',
            xmin=entry['sliceBegin'],
            xmax=entry['segment boundaries'][0])
        tier.append(begin_buffer)


def append_beginning_dicts(entry: dict, intervals: list[dict]) -> None:
    """
    Append dicts for BEEP and silence to the list of dicts.

    Parameters
    ----------
    entry : dict
        Metadata for the recording.
    intervals : list[dict]
        The list of interval dicts.
    """

    if 'beep' in entry:
        ic(entry)
        begin_buffer = {
            'label': '',
            'begin': entry['begin'],
            'end': entry['beep']
        }
        intervals.append(begin_buffer)

        beep = {
            'label': 'BEEP',
            'begin': entry['beep'],
            'end': entry['beep'] + 0.05
        }
        intervals.append(beep)

        after_beep = {
            'label': '',
            'begin': entry['beep'] + 0.05,
            'end': entry['segment boundaries'][0]
        }
        intervals.append(after_beep)
    else:
        begin_buffer = {
            'label': '',
            'begin': entry['begin'],
            'end': entry['segment boundaries'][0]
        }
        intervals.append(begin_buffer)


def append_end_dict(entry: dict, intervals: list[dict]) -> None:
    """
    Append dict for silence at the end to the list of dicts.


    Parameters
    ----------
    entry : dict
        Metadata for the recording.
    intervals : list[dict]
        The list of interval dicts.
    """
    end_buffer = {
        'label': '',
        'begin': entry['segment boundaries'][-1],
        'end': entry['end']}
    intervals.append(end_buffer)


def generate_utterance_dicts(entry: dict) -> list[dict]:
    """
    Generate an utterance Tier as a list of dicts.

    Parameters
    ----------
    entry : dict
        Metadata for the recording.
    """

    intervals = []
    append_beginning_dicts(entry, intervals)

    # For intervals and utterances one long interval.
    word = {
        'label': entry['prompt'],
        'begin': entry['segment boundaries'][0],
        'end': entry['segment boundaries'][-1]
    }
    intervals.append(word)

    append_end_dict(entry, intervals)

    return intervals


def generate_word_intervals(table) -> list[Interval]:
    """
    _summary_

    Parameters
    ----------
    table : _type_
        _description_
    filename : _type_
        _description_
    config_dict : _type_
        _description_
    pronunciation_dict : _type_, optional
        _description_, by default None
    """

    intervals = []
    for entry in table:
        append_beginning_dicts(entry, intervals)

        words = entry['prompt'].split()
        boundaries = np.linspace(
            entry['segment boundaries'][0],
            entry['segment boundaries'][-1],
            len(words) + 3)
        boundaries = boundaries[1:-1]
        for i, word in enumerate(words):
            interval = {
                'label': word,
                'begin': boundaries[i + 1],
                'end': boundaries[i + 2]
            }
            intervals.append(interval)

        append_end_dict(entry, intervals)

    return intervals


def generate_file_tier(table) -> Tier:
    """
    _summary_

    Parameters
    ----------
    table : _type_
        _description_

    Returns
    -------
    Tier
        _description_
    """
    files = Tier()
    for entry in table:
        file_segment = {
            'label': entry['filename'],
            'begin': entry['sliceBegin'],
            'end': entry['sliceEnd']}
        files.append(file_segment)

    return files


def generate_segments(
        table, pronunciation_dict=None
) -> list:
    # TODO: move the tier generation from here to above and the tier content
    # generation probably to its own function
    """
    _summary_

    Parameters
    ----------
    table : _type_
        _description_
    filename : _type_
        _description_
    config_dict : _type_
        _description_
    pronunciation_dict : _type_, optional
        _description_, by default None
    """

    segments = []
    for entry in table:
        append_beginning_dicts(entry, segments)

        if pronunciation_dict:
            # For segmentation a bunch of segment intervals
            for i, label in enumerate(entry['transcription']):
                segment = {
                    'label': label,
                    'begin': entry['segment boundaries'][i],
                    'end': entry['segment boundaries'][i + 1]
                }
                segments.append(segment)

        append_end_dict(entry, segments)

    return segments
