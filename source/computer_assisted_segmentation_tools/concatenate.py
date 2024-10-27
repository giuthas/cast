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
import pprint
import sys
from contextlib import closing
from pathlib import Path
from typing import Optional, Tuple, Union

import numpy as np
# wav file handling
import scipy.io.wavfile as sio_wavfile

from .meta.cast_meta import get_token_list

from .audio_processing import detect_beep_and_speech, high_pass
from .textgrid_functions import generate_textgrid
from .configuration import read_exclusion_list
from .csv_output import write_results

pp = pprint.PrettyPrinter(indent=4)


def process_wav_file(table_entry: dict, samplerate: float,
                     number_of_channels: int, cursor: float,
                     high_pass_filter: Optional[dict[str, np.ndarray]] = None
                     ) -> Tuple[float, np.ndarray]:
    (next_samplerate, frames) = sio_wavfile.read(table_entry['wav_path'])
    n_frames = frames.shape[0]
    if len(frames.shape) == 1:
        n_channels = 1
    else:
        n_channels = frames.shape[1]

    if next_samplerate != samplerate:
        print('Mismatched sample rates in sound files.')
        print(f"{next_samplerate} in {table_entry['wav_file']} "
              f"is not the common one: {samplerate}")
        print('Exiting.')
        sys.exit()

    if n_channels != number_of_channels:
        print('Mismatched numbers of channels in sound files.')
        print(
            f"{n_channels} in {table_entry['wav_file']} "
            f"is not the common one: {number_of_channels}")
        print('Exiting.')
        sys.exit()

    duration = n_frames / float(samplerate)

    table_entry['sliceBegin'] = cursor

    # setup the high-pass filter for removing the mains frequency (and anything
    # below it) from the recorded sound.
    if high_pass_filter:
        beep, has_speech = detect_beep_and_speech(
            frames, samplerate, high_pass_filter['b'],
            high_pass_filter['a'], table_entry['filename'])
        table_entry['beep'] = cursor + beep
        table_entry['has speech'] = has_speech
        # Start segmentation in FAV and other systems after the beep.
        table_entry['begin'] = cursor + beep + 0.05
    else:
        table_entry['begin'] = cursor
    cursor += duration
    table_entry['end'] = round(cursor, 3)
    table_entry['sliceEnd'] = cursor

    return cursor, frames


def apply_exclusion_list(table: list[dict], exclusion_path: Path) -> None:

    exclusion_list = read_exclusion_list(exclusion_path)

    if not exclusion_list:
        return

    for entry in table:
        filename = entry['filename']
        if filename in exclusion_list['files']:
            print(f'Excluding {filename}: File is in exclusion list.')
            entry['excluded'] = True

        # The first condition sees if the whole prompt is excluded,
        # the second condition checks if any parts of the prompt
        # match exclucion criteria (for example excluding 'foobar ...'
        # based on 'foobar').
        prompt = entry['prompt']
        if (prompt in exclusion_list['prompts'] or
                [element for element in exclusion_list['parts of prompts']
                 if element in prompt]):
            print(
                f'Excluding {filename}. Prompt: {prompt} matches exclusion list.')
            entry['excluded'] = True


def concatenate_wavs(directory: Union[str, Path],
                     config_dict: dict,
                     pronunciation_dict: Union[dict, None] = None,
                     only_words: bool = False):
    outputfile = config_dict['outputfile']

    if isinstance(directory, str):
        directory = Path(directory)
    if isinstance(outputfile, str):
        outputfile = Path(outputfile)

    table = get_token_list(config_dict, directory)

    apply_exclusion_list(table, Path(config_dict['exclusion list']))

    # Only add the beep entry if we are going to be using it.
    if config_dict['flags']['detect beep']:
        for entry in table:
            entry['beep'] = 'n/a'

    outwave = outputfile.with_suffix(".wav")
    outcsv = outputfile.with_suffix(".csv")
    out_textgrid = outputfile.with_suffix(".TextGrid")

    # find params from first file
    samplerate, test_data = sio_wavfile.read(table[0]['wav_path'])
    if len(test_data.shape) == 1:
        number_of_channels = 1
    else:
        number_of_channels = test_data.shape[1]

    # Read wavs and keep track of file boundaries.
    # TODO: consider moving the whole loop into processWavFile and renaming the function
    if config_dict['flags']['detect beep']:
        mains_frequency = 60
        high_pass_filter = high_pass(
            samplerate, mains_frequency)

    cursor = 0.0
    frames = None
    for entry in table:
        if entry['excluded']:
            continue
        if config_dict['flags']['detect beep']:
            cursor, new_frames = process_wav_file(
                entry, samplerate, number_of_channels, cursor,
                high_pass_filter=high_pass_filter)
        else:
            cursor, new_frames = process_wav_file(
                entry, samplerate, number_of_channels, cursor)
        if new_frames is None:
            continue
        if frames is None:
            frames = new_frames
        else:
            frames = np.concatenate([frames, new_frames], axis=0)

    # Write the concatanated wav.
    with closing(open(outwave, 'wb')) as output:
        sio_wavfile.write(output, samplerate, frames)

    # Weed out the skipped ones before writing the data out.
    table = [token for token in table if not token['excluded']]
    write_results(table, outcsv, config_dict['flags']['detect beep'])
    if only_words:
        generate_textgrid(table, out_textgrid, config_dict)
    else:
        generate_textgrid(table, out_textgrid, config_dict, pronunciation_dict)
    # pp.pprint(table)
